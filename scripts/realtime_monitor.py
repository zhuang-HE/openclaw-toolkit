#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时数据监控 - 异常检测和告警

功能:
1. 实时监控数据变化
2. 异常检测（价格波动、销量异常等）
3. 自动告警（飞书推送）
4. 趋势分析
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
import requests

# 配置
WORKSPACE = "/home/admin/.openclaw/workspace"
LOG_DIR = f"{WORKSPACE}/logs"
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/587f3c74-4345-4fc6-98b3-b2a935f6787e"

class RealtimeMonitor:
    """实时数据监控"""
    
    def __init__(self):
        self.alerts = []
        self.log_dir = Path(LOG_DIR)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 监控历史
        self.history_file = self.log_dir / 'monitor_history.json'
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """加载监控历史"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_history(self):
        """保存监控历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_alert_rule(self, name: str, condition: Dict, action: Callable = None):
        """
        添加告警规则
        
        Args:
            name: 规则名称
            condition: 条件配置
                {
                    'source': 'drone_prices',
                    'field': 'price',
                    'operator': 'change_percent',
                    'threshold': 10,  # 变化超过 10%
                    'comparison': 'gt'  # gt/lt/eq
                }
            action: 触发动作（默认发送飞书通知）
        """
        self.alerts.append({
            'name': name,
            'condition': condition,
            'action': action or self._default_action,
            'enabled': True,
            'last_triggered': None
        })
        
        print(f"✅ 告警规则已添加：{name}")
    
    def _default_action(self, alert_name: str, message: str):
        """默认动作：发送飞书通知"""
        self.send_feishu_alert(alert_name, message)
    
    def check_alerts(self, current_data: Dict) -> List:
        """检查告警"""
        triggered = []
        
        for alert in self.alerts:
            if not alert['enabled']:
                continue
            
            condition = alert['condition']
            
            # 检查条件
            if self._check_condition(current_data, condition):
                message = f"🚨 告警：{alert['name']}\n\n{condition}"
                
                # 触发动作
                alert['action'](alert['name'], message)
                alert['last_triggered'] = datetime.now().isoformat()
                
                triggered.append(alert['name'])
                
                # 记录历史
                self._record_alert(alert['name'], current_data)
        
        return triggered
    
    def _check_condition(self, data: Dict, condition: Dict) -> bool:
        """检查条件是否满足"""
        source = condition.get('source')
        field = condition.get('field')
        operator = condition.get('operator')
        threshold = condition.get('threshold')
        
        if source not in data:
            return False
        
        current_value = data[source].get(field)
        if current_value is None:
            return False
        
        # 获取历史值
        history = self.history.get(source, {}).get(field, [])
        if not history:
            return False
        
        previous_value = history[-1]
        
        # 计算变化
        if operator == 'change_percent':
            change = ((current_value - previous_value) / previous_value) * 100
            return abs(change) > threshold
        
        elif operator == 'change_absolute':
            change = current_value - previous_value
            return abs(change) > threshold
        
        return False
    
    def _record_alert(self, alert_name: str, data: Dict):
        """记录告警历史"""
        timestamp = datetime.now().isoformat()
        
        if alert_name not in self.history:
            self.history[alert_name] = []
        
        self.history[alert_name].append({
            'timestamp': timestamp,
            'data': data
        })
        
        # 保留最近 100 条
        self.history[alert_name] = self.history[alert_name][-100:]
        
        self._save_history()
    
    def send_feishu_alert(self, alert_name: str, message: str):
        """发送飞书告警"""
        payload = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        
        try:
            response = requests.post(FEISHU_WEBHOOK, json=payload)
            response.raise_for_status()
            print(f"✅ 飞书告警已发送：{alert_name}")
        except Exception as e:
            print(f"❌ 飞书发送失败：{e}")
    
    def analyze_trend(self, data_source: str, field: str, days: int = 30) -> Dict:
        """
        分析趋势
        
        Args:
            data_source: 数据源名称
            field: 字段名
            days: 分析天数
        
        Returns:
            {
                'direction': 'up'/'down'/'stable',
                'change_percent': float,
                'avg_value': float,
                'volatility': float
            }
        """
        history = self.history.get(data_source, {}).get(field, [])
        
        if len(history) < 2:
            return {
                'direction': 'unknown',
                'change_percent': 0,
                'avg_value': 0,
                'volatility': 0
            }
        
        # 计算趋势
        first_value = history[0]
        last_value = history[-1]
        change_percent = ((last_value - first_value) / first_value) * 100
        
        if change_percent > 5:
            direction = 'up'
        elif change_percent < -5:
            direction = 'down'
        else:
            direction = 'stable'
        
        # 计算波动率
        import statistics
        volatility = statistics.stdev(history) if len(history) > 1 else 0
        
        return {
            'direction': direction,
            'change_percent': round(change_percent, 2),
            'avg_value': round(statistics.mean(history), 2),
            'volatility': round(volatility, 2)
        }
    
    def start_monitoring(self, interval: int = 300):
        """
        启动监控
        
        Args:
            interval: 检查间隔（秒），默认 5 分钟
        """
        print(f"🔍 开始监控（间隔：{interval}秒）")
        
        try:
            while True:
                # 这里应该从数据源获取最新数据
                # 简化示例
                current_data = {}
                
                # 检查告警
                triggered = self.check_alerts(current_data)
                
                if triggered:
                    print(f"🚨 触发告警：{triggered}")
                else:
                    print(f"✅ 监控正常 ({datetime.now().strftime('%H:%M:%S')})")
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n⏹️  监控已停止")
    
    def get_status(self) -> Dict:
        """获取监控状态"""
        return {
            'total_rules': len(self.alerts),
            'enabled_rules': sum(1 for a in self.alerts if a['enabled']),
            'alerts': [
                {
                    'name': a['name'],
                    'enabled': a['enabled'],
                    'last_triggered': a['last_triggered']
                }
                for a in self.alerts
            ]
        }


# CLI 接口
def main():
    import sys
    
    monitor = RealtimeMonitor()
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("实时数据监控")
        print("=" * 60)
        print("用法:")
        print("  python realtime_monitor.py add <name> <source> <field> <threshold>")
        print("  python realtime_monitor.py status")
        print("  python realtime_monitor.py trend <source> <field>")
        print("  python realtime_monitor.py start [interval]")
        return
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 6:
            print("❌ 缺少参数")
            print("用法：python realtime_monitor.py add <name> <source> <field> <threshold>")
            return
        
        name = sys.argv[2]
        source = sys.argv[3]
        field = sys.argv[4]
        threshold = float(sys.argv[5])
        
        monitor.add_alert_rule(
            name=name,
            condition={
                'source': source,
                'field': field,
                'operator': 'change_percent',
                'threshold': threshold
            }
        )
    
    elif command == 'status':
        status = monitor.get_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    
    elif command == 'trend':
        if len(sys.argv) < 4:
            print("❌ 缺少参数")
            return
        
        source = sys.argv[2]
        field = sys.argv[3]
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        
        trend = monitor.analyze_trend(source, field, days)
        print(json.dumps(trend, ensure_ascii=False, indent=2))
    
    elif command == 'start':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        monitor.start_monitoring(interval)
    
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == '__main__':
    main()
