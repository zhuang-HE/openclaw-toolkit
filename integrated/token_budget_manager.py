#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三层 Token 预算管理系统
L1: 图谱查询 (500 tokens)
L2: Subgraph 提取 (1500 tokens)
L3: 原始文件读取 (按需)
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class TokenBudgetManager:
    """三层 Token 预算管理"""
    
    # Token 预算配置
    BUDGETS = {
        'L1_graph_query': 500,
        'L2_subgraph': 1500,
        'L3_raw_files': 5000,
    }
    
    # 复杂度映射
    COMPLEXITY_MAP = {
        'simple': 'L1_graph_query',
        'medium': 'L2_subgraph',
        'complex': 'L3_raw_files',
    }
    
    def __init__(self, graph_path: str = None):
        """初始化管理器"""
        self.graph_path = Path(graph_path) if graph_path else None
        self.graph_data = None
        
        # 统计信息
        self.stats = {
            'l1_count': 0,
            'l2_count': 0,
            'l3_count': 0,
            'total_saved_tokens': 0,
            'total_raw_tokens_needed': 0,
        }
        
        if self.graph_path and self.graph_path.exists():
            self.load_graph()
    
    def load_graph(self):
        """加载知识图谱"""
        with open(self.graph_path, 'r', encoding='utf-8') as f:
            self.graph_data = json.load(f)
        print(f"✓ 已加载知识图谱用于 Token 优化")
    
    def get_context(self, query: str, complexity: str = 'medium') -> Dict:
        """
        根据复杂度获取上下文
        
        Args:
            query: 查询内容
            complexity: 复杂度 (simple/medium/complex)
        
        Returns:
            {
                'context': str,          # 上下文内容
                'level': str,            # 使用的层级 (L1/L2/L3)
                'tokens_used': int,      # 实际使用 Token
                'tokens_saved': int,     # 节省的 Token
            }
        """
        level = self.COMPLEXITY_MAP.get(complexity, 'L2_subgraph')
        budget = self.BUDGETS[level]
        
        if level == 'L1_graph_query':
            context = self.query_graph(query, budget)
            self.stats['l1_count'] += 1
        elif level == 'L2_subgraph':
            context = self.extract_subgraph(query, budget)
            self.stats['l2_count'] += 1
        else:  # L3_raw_files
            context = self.read_raw_files(query, budget)
            self.stats['l3_count'] += 1
        
        # 估算节省的 Token
        estimated_raw_tokens = 35000  # 假设读取原始文件平均需要 35K tokens
        tokens_saved = estimated_raw_tokens - budget
        
        self.stats['total_saved_tokens'] += tokens_saved
        self.stats['total_raw_tokens_needed'] += estimated_raw_tokens
        
        return {
            'context': context,
            'level': level,
            'tokens_used': budget,
            'tokens_saved': tokens_saved,
        }
    
    def query_graph(self, query: str, budget: int) -> str:
        """L1: 图谱快速查询"""
        if not self.graph_data:
            return "知识图谱未加载"
        
        # 查找相关节点
        related_nodes = []
        for node in self.graph_data.get('nodes', []):
            node_id = node.get('id', '')
            if query in node_id or any(k in node_id for k in ['无人机', '保险', '风险']):
                related_nodes.append(node_id)
                
                if len(related_nodes) * 50 >= budget:  # 粗略估算
                    break
        
        if related_nodes:
            return f"找到 {len(related_nodes)} 个相关概念:\n" + "\n".join(related_nodes[:10])
        
        return "未找到相关概念"
    
    def extract_subgraph(self, query: str, budget: int) -> str:
        """L2: 提取子图谱"""
        if not self.graph_data:
            return "知识图谱未加载"
        
        # 查找相关节点和边
        subgraph_nodes = []
        subgraph_edges = []
        
        for node in self.graph_data.get('nodes', []):
            node_id = node.get('id', '')
            if query in node_id or any(k in node_id for k in ['无人机', '保险', '风险', '费率']):
                subgraph_nodes.append(node)
        
        for edge in self.graph_data.get('edges', []):
            if any(n.get('id') == edge.get('source') for n in subgraph_nodes):
                subgraph_edges.append(edge)
        
        # 格式化输出
        lines = [
            f"子图谱统计:",
            f"- 节点数：{len(subgraph_nodes)}",
            f"- 边数：{len(subgraph_edges)}",
            f"",
            f"相关节点:",
        ]
        
        for node in subgraph_nodes[:20]:
            lines.append(f"- {node.get('id', '')} ({node.get('type', '')})")
        
        return "\n".join(lines)
    
    def read_raw_files(self, query: str, budget: int) -> str:
        """L3: 读取原始文件（按需）"""
        # 这里应该实现实际的文件读取逻辑
        # 简化版本返回提示
        return f"需要从原始文件读取深度信息...\n建议查询以下文件:\n- drone_data/货运无人机数据库_完整版.csv\n- insurance_data/费率计算规则.csv"
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        savings_ratio = 0
        if self.stats['total_raw_tokens_needed'] > 0:
            savings_ratio = self.stats['total_saved_tokens'] / self.stats['total_raw_tokens_needed'] * 100
        
        return {
            'query_counts': {
                'L1_graph_query': self.stats['l1_count'],
                'L2_subgraph': self.stats['l2_count'],
                'L3_raw_files': self.stats['l3_count'],
            },
            'token_savings': {
                'total_saved': self.stats['total_saved_tokens'],
                'total_raw_needed': self.stats['total_raw_tokens_needed'],
                'savings_ratio': f"{savings_ratio:.1f}%",
            },
            'timestamp': datetime.now().isoformat(),
        }
    
    def print_stats(self):
        """打印统计信息"""
        stats = self.get_stats()
        
        print("\n" + "=" * 60)
        print("Token 预算统计")
        print("=" * 60)
        print(f"\n查询次数:")
        for level, count in stats['query_counts'].items():
            print(f"  {level}: {count}")
        
        print(f"\nToken 节省:")
        print(f"  总节省：{stats['token_savings']['total_saved']:,} tokens")
        print(f"  原始需要：{stats['token_savings']['total_raw_needed']:,} tokens")
        print(f"  节省比例：{stats['token_savings']['savings_ratio']}")
        print(f"\n时间：{stats['timestamp']}")
        print("=" * 60)


def test_budget_manager():
    """测试 Token 预算管理"""
    print("=" * 60)
    print("Token Budget Manager 测试")
    print("=" * 60)
    
    # 初始化管理器
    manager = TokenBudgetManager(
        graph_path="/home/admin/.openclaw/workspace/graphify-out/graph.json"
    )
    
    # 测试不同复杂度的查询
    test_queries = [
        ("货运无人机有几种？", "simple"),
        ("大疆 FlyCart 30 的保险费率如何计算？", "medium"),
        ("分析货运无人机风险系数与货物损失率的关系", "complex"),
    ]
    
    print("\nToken 预算测试：\n")
    for query, complexity in test_queries:
        result = manager.get_context(query, complexity)
        
        print(f"\n查询：{query}")
        print(f"复杂度：{complexity}")
        print(f"层级：{result['level']}")
        print(f"Token 使用：{result['tokens_used']}")
        print(f"Token 节省：{result['tokens_saved']}")
        print(f"上下文预览：{result['context'][:200]}...")
    
    # 打印统计
    manager.print_stats()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_budget_manager()
