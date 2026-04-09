#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据融合中心 - 跨数据源查询和分析

功能:
1. 多数据源融合（无人机/临床/保险/机器人）
2. 自动关联和连接
3. 自然语言查询
4. 智能推荐图表
"""

import json
import pandas as pd
from typing import Dict, List, Optional, Any
from pathlib import Path

# 配置
WORKSPACE = "/home/admin/.openclaw/workspace"
DATA_DIR = f"{WORKSPACE}/collected_data"

class DataFusionCenter:
    """数据融合中心"""
    
    def __init__(self):
        self.sources = {}
        self.fused_data = {}
        self.data_dir = Path(DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 注册默认数据源
        self._register_default_sources()
    
    def _register_default_sources(self):
        """注册默认数据源"""
        self.sources = {
            'drone_db': {
                'name': '无人机数据库',
                'type': 'csv',
                'path': f"{WORKSPACE}/无人机 BI 数据库_货运完整版_含规格.csv",
                'status': 'active'
            },
            'clinical_db': {
                'name': '临床试验数据库',
                'type': 'csv',
                'path': f"{WORKSPACE}/clinical_trial_data/临床试验事故案例库.csv",
                'status': 'active'
            },
            'insurance_db': {
                'name': '保险产品数据库',
                'type': 'csv',
                'path': f"{WORKSPACE}/insurance-data-summary.md",
                'status': 'active'
            },
            'robot_db': {
                'name': '机器人数据库',
                'type': 'csv',
                'path': f"{WORKSPACE}/机器人数据库_完整版.csv",
                'status': 'active'
            },
            'token_stats': {
                'name': 'Token 统计',
                'type': 'json',
                'path': f"{WORKSPACE}/logs/token_stats.json",
                'status': 'active'
            }
        }
    
    def load_data(self, source_name: str) -> pd.DataFrame:
        """加载数据源"""
        if source_name not in self.sources:
            raise ValueError(f"未知数据源：{source_name}")
        
        source = self.sources[source_name]
        path = Path(source['path'])
        
        if not path.exists():
            print(f"⚠️  数据文件不存在：{path}")
            return pd.DataFrame()
        
        try:
            if source['type'] == 'csv':
                df = pd.read_csv(path)
            elif source['type'] == 'json':
                df = pd.read_json(path)
            elif source['type'] == 'excel':
                df = pd.read_excel(path)
            else:
                raise ValueError(f"不支持的文件类型：{source['type']}")
            
            print(f"✅ 加载数据源：{source_name} ({len(df)} 条记录)")
            return df
        
        except Exception as e:
            print(f"❌ 加载失败：{e}")
            return pd.DataFrame()
    
    def query(self, natural_language: str) -> Dict:
        """
        自然语言查询
        
        Args:
            natural_language: 自然语言查询
        
        Returns:
            {
                'success': bool,
                'data': DataFrame,
                'chart_type': str,
                'recommendation': str
            }
        """
        # 解析查询意图
        intent = self._parse_intent(natural_language)
        
        # 路由到数据源
        source_names = intent.get('sources', list(self.sources.keys()))
        
        # 加载数据
        dataframes = {}
        for source_name in source_names:
            df = self.load_data(source_name)
            if not df.empty:
                dataframes[source_name] = df
        
        # 融合数据
        if len(dataframes) > 1:
            fused_df = self._fuse_dataframes(dataframes, intent)
        else:
            fused_df = list(dataframes.values())[0] if dataframes else pd.DataFrame()
        
        # 应用过滤
        if 'filters' in intent:
            fused_df = self._apply_filters(fused_df, intent['filters'])
        
        # 推荐图表
        chart_type = self._recommend_chart(fused_df, intent)
        
        return {
            'success': True,
            'data': fused_df,
            'chart_type': chart_type,
            'recommendation': self._generate_recommendation(fused_df, intent)
        }
    
    def _parse_intent(self, query: str) -> Dict:
        """解析查询意图"""
        intent = {
            'sources': [],
            'filters': {},
            'aggregations': [],
            'output': 'table'
        }
        
        # 简单关键词匹配（实际应该用 NLP）
        if '无人机' in query:
            intent['sources'].append('drone_db')
        if '临床' in query or '试验' in query:
            intent['sources'].append('clinical_db')
        if '保险' in query:
            intent['sources'].append('insurance_db')
        if '机器人' in query:
            intent['sources'].append('robot_db')
        if 'Token' in query or 'token' in query:
            intent['sources'].append('token_stats')
        
        # 默认使用所有数据源
        if not intent['sources']:
            intent['sources'] = list(self.sources.keys())
        
        # 检测时间范围
        if '近 7 天' in query or '最近一周' in query:
            intent['filters']['days'] = 7
        elif '近 30 天' in query or '最近一月' in query:
            intent['filters']['days'] = 30
        
        # 检测图表类型
        if '趋势' in query or '变化' in query:
            intent['output'] = 'line'
        elif '对比' in query or '比较' in query:
            intent['output'] = 'bar'
        elif '占比' in query or '分布' in query:
            intent['output'] = 'pie'
        elif '关系' in query or '相关' in query:
            intent['output'] = 'scatter'
        
        return intent
    
    def _fuse_dataframes(self, dataframes: Dict[str, pd.DataFrame], intent: Dict) -> pd.DataFrame:
        """融合多个数据框"""
        if len(dataframes) == 1:
            return list(dataframes.values())[0]
        
        # 简单融合（实际应该更复杂）
        # 这里只是示例
        first_key = list(dataframes.keys())[0]
        return dataframes[first_key]
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """应用过滤器"""
        if 'days' in filters:
            # 时间过滤
            pass
        return df
    
    def _recommend_chart(self, df: pd.DataFrame, intent: Dict) -> str:
        """推荐图表类型"""
        if intent.get('output'):
            return intent['output']
        
        # 根据数据特征推荐
        if len(df) == 0:
            return 'table'
        
        columns = df.columns.tolist()
        
        # 有时间列 → 折线图
        if any('date' in col.lower() or 'time' in col.lower() for col in columns):
            return 'line'
        
        # 有分类列和数值列 → 柱状图
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            return 'bar'
        
        return 'table'
    
    def _generate_recommendation(self, df: pd.DataFrame, intent: Dict) -> str:
        """生成分析建议"""
        if len(df) == 0:
            return "无数据"
        
        recommendations = []
        
        # 基本统计
        recommendations.append(f"数据量：{len(df)} 条")
        
        # 数值列统计
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols[:3]:
            mean_val = df[col].mean()
            recommendations.append(f"{col} 平均值：{mean_val:.2f}")
        
        return "\n".join(recommendations)
    
    def join(self, left: str, right: str, on: str):
        """连接两个数据源"""
        left_df = self.load_data(left.split('.')[0])
        right_df = self.load_data(right.split('.')[0])
        
        if left_df.empty or right_df.empty:
            print("⚠️  数据源为空，无法连接")
            return
        
        # 执行连接
        fused = pd.merge(left_df, right_df, on=on, how='inner')
        
        fusion_key = f"{left}_joined_{right}"
        self.fused_data[fusion_key] = fused
        
        print(f"✅ 数据连接完成：{fusion_key} ({len(fused)} 条记录)")
        return fused
    
    def get_sources(self) -> List[Dict]:
        """获取所有数据源"""
        return [
            {
                'name': name,
                'display_name': info['name'],
                'type': info['type'],
                'status': info['status']
            }
            for name, info in self.sources.items()
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = {
            'total_sources': len(self.sources),
            'active_sources': sum(1 for s in self.sources.values() if s['status'] == 'active'),
            'fused_datasets': len(self.fused_data),
            'data_files': []
        }
        
        for name, info in self.sources.items():
            path = Path(info['path'])
            if path.exists():
                stats['data_files'].append({
                    'name': name,
                    'size_mb': round(path.stat().st_size / 1024 / 1024, 2)
                })
        
        return stats


# CLI 接口
def main():
    import sys
    
    fusion = DataFusionCenter()
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("数据融合中心")
        print("=" * 60)
        print("用法:")
        print("  python data_fusion.py sources")
        print("  python data_fusion.py query \"<自然语言查询>\"")
        print("  python data_fusion.py join <left> <right> <on>")
        print("  python data_fusion.py stats")
        return
    
    command = sys.argv[1]
    
    if command == 'sources':
        sources = fusion.get_sources()
        print(json.dumps(sources, ensure_ascii=False, indent=2))
    
    elif command == 'query':
        if len(sys.argv) < 3:
            print("❌ 缺少查询语句")
            return
        query = sys.argv[2]
        result = fusion.query(query)
        print(f"图表类型：{result['chart_type']}")
        print(f"建议：{result['recommendation']}")
        print(f"\n数据预览:")
        print(result['data'].head())
    
    elif command == 'join':
        if len(sys.argv) < 5:
            print("❌ 缺少参数")
            return
        left = sys.argv[2]
        right = sys.argv[3]
        on = sys.argv[4]
        fusion.join(left, right, on)
    
    elif command == 'stats':
        stats = fusion.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == '__main__':
    main()
