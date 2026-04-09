#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Knowledge Graph Builder
简化版 Graphify - 为 OpenClaw 工作空间构建知识图谱
"""

import json
import csv
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
# import networkx as nx  # 简化版不使用 networkx

# 配置
WORKSPACE = "/home/admin/.openclaw/workspace"
OUTPUT_DIR = f"{WORKSPACE}/graphify-out"
CACHE_DIR = f"{OUTPUT_DIR}/cache"

class KnowledgeGraphBuilder:
    """知识图谱构建器（简化版，不使用 networkx）"""
    
    def __init__(self, root_dir: str = WORKSPACE):
        self.root_dir = Path(root_dir)
        self.nodes = {}  # node_id -> node_data
        self.edges = []  # (source, target, relation)
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict[str, str]:
        """加载 SHA256 缓存"""
        cache_file = Path(CACHE_DIR) / "sha256_cache.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """保存 SHA256 缓存"""
        os.makedirs(CACHE_DIR, exist_ok=True)
        cache_file = Path(CACHE_DIR) / "sha256_cache.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def _compute_sha256(self, file_path: Path) -> str:
        """计算文件 SHA256"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _should_process(self, file_path: Path) -> bool:
        """检查文件是否需要处理（增量更新）"""
        current_hash = self._compute_sha256(file_path)
        cached_hash = self.cache.get(str(file_path))
        return current_hash != cached_hash
    
    def _extract_csv_metadata(self, file_path: Path) -> Dict:
        """从 CSV 文件提取元数据"""
        metadata = {
            'type': 'dataset',
            'columns': [],
            'rows': 0,
            'concepts': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader)
                metadata['columns'] = headers
                metadata['rows'] = sum(1 for _ in reader)
                
                # 提取关键列作为概念
                key_columns = ['品牌', '型号', '风险等级', '主要用途', '保险费率']
                metadata['concepts'] = [col for col in headers if any(k in col for k in key_columns)]
        except Exception as e:
            print(f"  ⚠️ 读取 CSV 失败：{e}")
        
        return metadata
    
    def _extract_md_metadata(self, file_path: Path) -> Dict:
        """从 Markdown 文件提取概念"""
        metadata = {
            'type': 'document',
            'headings': [],
            'concepts': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 提取标题
                for line in content.split('\n'):
                    if line.startswith('#'):
                        metadata['headings'].append(line.strip('#').strip())
                    
                    # 提取粗体概念
                    import re
                    bold_matches = re.findall(r'\*\*(.+?)\*\*', line)
                    metadata['concepts'].extend(bold_matches)
        except Exception as e:
            print(f"  ⚠️ 读取 MD 失败：{e}")
        
        return metadata
    
    def build_graph(self, include_patterns: List[str] = None, exclude_patterns: List[str] = None):
        """构建知识图谱"""
        print(f"🔍 开始构建知识图谱...")
        print(f"📂 根目录：{self.root_dir}")
        
        # 默认包含的模式
        if include_patterns is None:
            include_patterns = ['*.csv', '*.md', '*.py', '*.json']
        
        # 默认排除的模式
        if exclude_patterns is None:
            exclude_patterns = ['node_modules', 'logs', 'cache', 'graphify-out', '*.backup.*']
        
        files_processed = 0
        files_skipped = 0
        
        # 遍历文件
        for pattern in include_patterns:
            for file_path in self.root_dir.rglob(pattern):
                # 检查排除
                if any(excl in str(file_path) for excl in exclude_patterns):
                    files_skipped += 1
                    continue
                
                # 检查是否需要处理（增量更新）
                if not self._should_process(file_path):
                    files_skipped += 1
                    continue
                
                # 提取元数据
                rel_path = str(file_path.relative_to(self.root_dir))
                print(f"📄 处理：{rel_path}")
                
                if file_path.suffix == '.csv':
                    metadata = self._extract_csv_metadata(file_path)
                    node_id = f"dataset:{rel_path}"
                    
                    # 添加数据集节点
                    self.nodes[node_id] = {
                        'type': 'dataset',
                        'path': rel_path,
                        'columns': metadata['columns'],
                        'rows': metadata['rows'],
                        'concepts': metadata['concepts']
                    }
                    
                    # 添加列概念节点
                    for col in metadata['concepts']:
                        col_node_id = f"concept:{col}"
                        if col_node_id not in self.nodes:
                            self.nodes[col_node_id] = {'type': 'concept', 'name': col}
                        self.edges.append((node_id, col_node_id, 'contains_concept'))
                
                elif file_path.suffix == '.md':
                    metadata = self._extract_md_metadata(file_path)
                    node_id = f"document:{rel_path}"
                    
                    # 添加文档节点
                    self.nodes[node_id] = {
                        'type': 'document',
                        'path': rel_path,
                        'headings': metadata['headings'],
                        'concepts': metadata['concepts']
                    }
                    
                    # 添加概念节点
                    for concept in metadata['concepts'][:10]:
                        concept_node_id = f"concept:{concept}"
                        if concept_node_id not in self.nodes:
                            self.nodes[concept_node_id] = {'type': 'concept', 'name': concept}
                        self.edges.append((node_id, concept_node_id, 'mentions'))
                
                # 更新缓存
                self.cache[str(file_path)] = self._compute_sha256(file_path)
                files_processed += 1
        
        # 保存缓存
        self._save_cache()
        
        print(f"\n✅ 图谱构建完成！")
        print(f"   处理文件：{files_processed}")
        print(f"   跳过文件：{files_skipped}")
        print(f"   节点数：{len(self.nodes)}")
        print(f"   边数：{len(self.edges)}")
        
        return self
    
    def find_god_nodes(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """查找上帝节点（最高度数）- 简化版"""
        degree_count = {}
        for source, target, _ in self.edges:
            degree_count[source] = degree_count.get(source, 0) + 1
            degree_count[target] = degree_count.get(target, 0) + 1
        
        sorted_nodes = sorted(degree_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:top_n]
    
    def find_communities(self) -> List[Set[str]]:
        """查找社区 - 简化版（按类型分组）"""
        communities = {}
        for node_id, node_data in self.nodes.items():
            node_type = node_data.get('type', 'unknown')
            if node_type not in communities:
                communities[node_type] = set()
            communities[node_type].add(node_id)
        
        return list(communities.values())
    
    def save_graph(self):
        """保存图谱"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # 保存为 JSON
        graph_file = Path(OUTPUT_DIR) / "graph.json"
        graph_data = {
            'nodes': [{'id': k, **v} for k, v in self.nodes.items()],
            'edges': [{'source': s, 'target': t, 'relation': r} for s, t, r in self.edges]
        }
        with open(graph_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2, default=str)
        
        # 生成报告
        self._generate_report()
        
        print(f"📁 图谱已保存到：{OUTPUT_DIR}")
    
    def _generate_report(self):
        """生成图谱报告"""
        report_file = Path(OUTPUT_DIR) / "GRAPH_REPORT.md"
        
        god_nodes = self.find_god_nodes()
        communities = self.find_communities()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Knowledge Graph Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            
            f.write("## 📊 Graph Statistics\n\n")
            f.write(f"- **Nodes:** {len(self.nodes)}\n")
            f.write(f"- **Edges:** {len(self.edges)}\n\n")
            
            f.write("## 🎯 God Nodes (Top 10)\n\n")
            f.write("| Node | Degree | Type |\n")
            f.write("|------|--------|------|\n")
            for node_id, degree in god_nodes:
                node_data = self.nodes.get(node_id, {})
                node_type = node_data.get('type', 'unknown')
                node_name = node_id.split(':')[-1]
                f.write(f"| {node_name} | {degree} | {node_type} |\n")
            
            f.write("\n## 🏘️ Communities\n\n")
            for i, community in enumerate(communities[:5]):
                f.write(f"### Community {i+1} ({len(community)} nodes)\n\n")
                members = list(community)[:10]
                for member in members:
                    member_data = self.nodes.get(member, {})
                    member_name = member.split(':')[-1]
                    member_type = member_data.get('type', 'unknown')
                    f.write(f"- {member_name} ({member_type})\n")
                f.write("\n")
            
            f.write("## 💡 Suggested Questions\n\n")
            f.write("1. 哪些数据集包含'风险等级'概念？\n")
            f.write("2. '保险费率'与哪些概念相关？\n")
            f.write("3. 货运无人机和消费级无人机的数据结构有何不同？\n")
            f.write("4. 哪些文档提到了'货物损失'？\n")
            f.write("5. 性能规格字段如何关联到保险费率？\n")


def main():
    """主函数"""
    print("=" * 60)
    print("OpenClaw Knowledge Graph Builder")
    print("=" * 60)
    
    builder = KnowledgeGraphBuilder(WORKSPACE)
    
    # 构建图谱
    builder.build_graph(
        include_patterns=['*.csv', '*.md'],
        exclude_patterns=['node_modules', 'logs', 'graphify-out', 'memory', 'reports']
    )
    
    # 保存图谱
    builder.save_graph()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
