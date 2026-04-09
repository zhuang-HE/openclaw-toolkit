#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自适应解析器 - 网站变化后自动重新定位元素

功能:
1. 保存元素特征
2. 相似度算法匹配
3. 自动适应网站改版
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any

# 配置
WORKSPACE = "/home/admin/.openclaw/workspace"
ELEMENT_CACHE = f"{WORKSPACE}/.element_cache"

class AdaptiveParser:
    """自适应解析器"""
    
    def __init__(self):
        self.cache_dir = Path(ELEMENT_CACHE)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def save_element(self, url: str, selector: str, elements: List[Dict], 
                     features: Dict = None):
        """
        保存元素特征
        
        Args:
            url: 页面 URL
            selector: CSS/XPath 选择器
            elements: 元素列表
            features: 额外特征（标签、类名、文本模式等）
        """
        cache_key = f"{url}_{selector}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_hash}.json"
        
        cache_data = {
            'url': url,
            'selector': selector,
            'elements': elements,
            'features': features or {},
            'timestamp': str(Path(url).stat().st_mtime) if Path(url).exists() else None
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 元素特征已保存：{selector}")
        return cache_file
    
    def find_similar(self, page, selector: str, url: str = None) -> List:
        """
        查找相似元素
        
        Args:
            page: 页面对象
            selector: 原始选择器
            url: 页面 URL
        
        Returns:
            相似元素列表
        """
        # 加载缓存
        cache_key = f"{url}_{selector}" if url else selector
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_hash}.json"
        
        if not cache_file.exists():
            print(f"⚠️  无缓存，使用原始选择器")
            return page.css(selector).getall() if hasattr(page, 'css') else []
        
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached_data = json.load(f)
        
        saved_features = cached_data.get('features', {})
        saved_selector = cached_data.get('selector', selector)
        
        # 尝试原始选择器
        elements = page.css(saved_selector).getall() if hasattr(page, 'css') else []
        
        if elements:
            print(f"✅ 原始选择器仍然有效")
            return elements
        
        # 原始选择器失效，使用自适应查找
        print(f"⚠️  原始选择器失效，启动自适应查找...")
        
        # 尝试变体选择器
        variants = self._generate_selector_variants(saved_selector)
        
        for variant in variants:
            elements = page.css(variant).getall() if hasattr(page, 'css') else []
            if elements:
                print(f"✅ 找到替代选择器：{variant}")
                # 更新缓存
                cached_data['selector'] = variant
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cached_data, f, ensure_ascii=False, indent=2)
                return elements
        
        # 所有选择器都失效，使用特征匹配
        print(f"⚠️  选择器都失效，使用特征匹配...")
        return self._match_by_features(page, saved_features)
    
    def _generate_selector_variants(self, selector: str) -> List[str]:
        """生成选择器变体"""
        variants = []
        
        # 基础变体
        variants.append(selector)
        
        # 类名变体
        if '.' in selector:
            # 移除部分类名
            parts = selector.split('.')
            for i in range(1, len(parts)):
                variants.append('.'.join(parts[:i]))
        
        # 标签变体
        if '::' in selector:
            # 移除伪元素
            variants.append(selector.split('::')[0])
        
        # 属性变体
        if '[' in selector:
            # 移除属性
            variants.append(selector.split('[')[0])
        
        # 去重
        return list(set(variants))
    
    def _match_by_features(self, page, features: Dict) -> List:
        """通过特征匹配元素"""
        # 这是一个简化实现
        # 实际应该使用更复杂的相似度算法
        
        matched = []
        
        # 尝试通过类名匹配
        if 'class' in features:
            class_name = features['class']
            elements = page.css(f'.{class_name}').getall() if hasattr(page, 'css') else []
            if elements:
                matched.extend(elements)
        
        # 尝试通过标签匹配
        if 'tag' in features:
            tag = features['tag']
            elements = page.css(tag).getall() if hasattr(page, 'css') else []
            if elements:
                matched.extend(elements)
        
        # 尝试通过文本模式匹配
        if 'text_pattern' in features:
            import re
            pattern = features['text_pattern']
            # 这里需要更复杂的实现
            pass
        
        return matched
    
    def auto_save(self, page, selector: str, url: str = None) -> List:
        """
        自动保存并提取元素
        
        Args:
            page: 页面对象
            selector: CSS/XPath 选择器
            url: 页面 URL
        
        Returns:
            元素列表
        """
        # 提取元素
        elements = page.css(selector).getall() if hasattr(page, 'css') else []
        
        if not elements:
            print(f"⚠️  未找到元素：{selector}")
            return []
        
        # 提取特征
        features = self._extract_features(elements[0]) if elements else {}
        
        # 保存
        self.save_element(url or 'unknown', selector, elements, features)
        
        return elements
    
    def _extract_features(self, element: str) -> Dict:
        """提取元素特征"""
        features = {}
        
        # 简化实现
        # 实际应该解析 HTML 提取标签、类名、属性等
        
        if 'class="' in element:
            start = element.find('class="') + 7
            end = element.find('"', start)
            if end > start:
                features['class'] = element[start:end].split()[0]
        
        if element.startswith('<'):
            end = element.find('>')
            tag_end = element.find(' ') if ' ' in element[:end] else end
            features['tag'] = element[1:tag_end]
        
        return features


# 使用示例
def demo():
    """演示自适应解析器"""
    print("=" * 60)
    print("自适应解析器演示")
    print("=" * 60)
    
    parser = AdaptiveParser()
    
    # 示例 1: 保存元素
    print("\n1. 保存元素特征")
    sample_elements = [
        '<div class="product"><h2>Product 1</h2><span class="price">$10</span></div>',
        '<div class="product"><h2>Product 2</h2><span class="price">$20</span></div>',
    ]
    
    parser.save_element(
        url='https://example.com/products',
        selector='.product',
        elements=sample_elements,
        features={'tag': 'div', 'class': 'product'}
    )
    
    # 示例 2: 查找相似元素
    print("\n2. 查找相似元素")
    # 这里需要实际的页面对象
    # elements = parser.find_similar(page, '.product', 'https://example.com/products')
    
    print("\n✅ 演示完成")
    print(f"缓存目录：{parser.cache_dir}")


if __name__ == '__main__':
    demo()
