#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphify 增强的 Agent 路由系统
基于知识图谱将查询路由到最合适的 Agent
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

class GraphifyAgentRouter:
    """基于知识图谱的 Agent 路由"""
    
    # Agent 映射配置
    AGENT_MAPPING = {
        # 保险/风险相关 → security-reviewer
        '保险': 'security-reviewer',
        '风险': 'security-reviewer',
        '费率': 'security-reviewer',
        '理赔': 'security-reviewer',
        '核保': 'security-reviewer',
        
        # 性能/架构相关 → architect
        '性能': 'architect',
        '架构': 'architect',
        '规格': 'architect',
        '设计': 'architect',
        
        # 数据/统计相关 → researcher
        '数据': 'researcher',
        '统计': 'researcher',
        '分析': 'researcher',
        '趋势': 'researcher',
        
        # 代码/实现相关 → code-reviewer
        '代码': 'code-reviewer',
        '实现': 'code-reviewer',
        '脚本': 'code-reviewer',
        '程序': 'code-reviewer',
        
        # 规划/计划相关 → planner
        '计划': 'planner',
        '规划': 'planner',
        '方案': 'planner',
        '步骤': 'planner',
        
        # 文档相关 → documentation-writer
        '文档': 'documentation-writer',
        '报告': 'documentation-writer',
        '说明': 'documentation-writer',
    }
    
    def __init__(self, graph_path: str = None):
        """初始化路由"""
        self.graph_path = Path(graph_path) if graph_path else None
        self.graph_data = None
        self.communities = None
        
        if self.graph_path and self.graph_path.exists():
            self.load_graph()
            self.identify_communities()
    
    def load_graph(self):
        """加载知识图谱"""
        with open(self.graph_path, 'r', encoding='utf-8') as f:
            self.graph_data = json.load(f)
        print(f"✓ 已加载知识图谱：{len(self.graph_data.get('nodes', []))} 节点")
    
    def identify_communities(self):
        """识别社区（简化版：按类型分组）"""
        communities = {}
        for node in self.graph_data.get('nodes', []):
            node_type = node.get('type', 'unknown')
            if node_type not in communities:
                communities[node_type] = []
            communities[node_type].append(node.get('id', ''))
        
        self.communities = communities
        print(f"✓ 已识别 {len(communities)} 个社区")
    
    def route_query(self, query: str) -> str:
        """根据查询内容路由到最合适的 Agent"""
        # 1. 关键词匹配
        for keyword, agent in self.AGENT_MAPPING.items():
            if keyword in query:
                print(f"🎯 路由：'{query}' → {agent} (关键词：{keyword})")
                return agent
        
        # 2. 如果没有关键词匹配，使用图谱语义搜索
        if self.graph_data:
            agent = self.route_by_graph(query)
            if agent:
                return agent
        
        # 3. 默认路由到 planner
        print(f"🎯 路由：'{query}' → planner (默认)")
        return 'planner'
    
    def route_by_graph(self, query: str) -> str:
        """基于图谱语义路由"""
        # 查找查询中提到的概念
        query_concepts = self.extract_concepts(query)
        
        # 统计各社区的匹配度
        community_scores = {}
        for node in self.graph_data.get('nodes', []):
            node_id = node.get('id', '')
            for concept in query_concepts:
                if concept in node_id:
                    node_type = node.get('type', 'unknown')
                    community_scores[node_type] = community_scores.get(node_type, 0) + 1
        
        # 选择匹配度最高的社区
        if community_scores:
            best_community = max(community_scores, key=community_scores.get)
            
            # 社区到 Agent 的映射
            community_agent_map = {
                'concept': 'researcher',
                'dataset': 'security-reviewer',
                'document': 'documentation-writer',
            }
            
            agent = community_agent_map.get(best_community, 'planner')
            print(f"🎯 路由：'{query}' → {agent} (图谱社区：{best_community})")
            return agent
        
        return None
    
    def extract_concepts(self, query: str) -> List[str]:
        """提取查询中的概念（简化版：分词）"""
        # 中文分词（简化实现）
        concepts = []
        
        # 无人机相关
        if '无人机' in query:
            concepts.append('无人机')
        if '货运' in query:
            concepts.append('货运')
        if '机型' in query or '型号' in query:
            concepts.append('型号')
        
        # 保险相关
        if '保险' in query:
            concepts.append('保险')
        if '费率' in query:
            concepts.append('费率')
        if '风险' in query:
            concepts.append('风险')
        
        # 性能相关
        if '性能' in query:
            concepts.append('性能')
        if '载荷' in query:
            concepts.append('载荷')
        if '航程' in query:
            concepts.append('航程')
        
        return concepts
    
    def get_context(self, query: str, budget: int = 1500) -> str:
        """从图谱提取上下文（控制 Token 预算）"""
        if not self.graph_data:
            return ""
        
        # 1. 查找相关节点
        related_nodes = []
        query_concepts = self.extract_concepts(query)
        
        for node in self.graph_data.get('nodes', []):
            node_id = node.get('id', '')
            for concept in query_concepts:
                if concept in node_id:
                    related_nodes.append(node)
                    break
        
        # 2. 格式化输出（控制 Token）
        context_lines = []
        token_count = 0
        
        for node in related_nodes[:20]:  # 限制节点数
            line = f"- {node.get('id', '')}: {node.get('type', '')}"
            context_lines.append(line)
            token_count += len(line) // 4  # 粗略估算 Token
            
            if token_count >= budget:
                break
        
        if context_lines:
            return "相关概念:\n" + "\n".join(context_lines)
        
        return ""


def test_router():
    """测试路由功能"""
    print("=" * 60)
    print("Graphify Agent Router 测试")
    print("=" * 60)
    
    # 初始化路由
    router = GraphifyAgentRouter(
        graph_path="/home/admin/.openclaw/workspace/graphify-out/graph.json"
    )
    
    # 测试查询
    test_queries = [
        "货运无人机的保险费率如何计算？",
        "大疆 FlyCart 30 的性能规格是什么？",
        "帮我分析一下事故数据趋势",
        "这段代码如何实现核保逻辑？",
        "制定一个无人机数据收集计划",
        "写一份保险理赔报告",
    ]
    
    print("\n路由测试：\n")
    for query in test_queries:
        agent = router.route_query(query)
        context = router.get_context(query, budget=500)
        
        print(f"\n查询：{query}")
        print(f"路由：{agent}")
        if context:
            print(f"上下文：{context[:200]}...")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_router()
