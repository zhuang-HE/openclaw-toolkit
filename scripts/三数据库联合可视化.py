#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三数据库联合可视化工具
生成三个数据库（机器人、无人机、临床试验）的趋势图表和对比分析
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path

WORKSPACE = "/home/admin/.openclaw/workspace"
VISUALIZATION_DIR = f"{WORKSPACE}/visualizations"

os.makedirs(VISUALIZATION_DIR, exist_ok=True)


def load_csv_data(filepath):
    """加载 CSV 数据"""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"加载失败 {filepath}: {e}")
        return []


def generate_text_chart(data, title, x_label, y_label, width=60, height=15):
    """生成文本图表（ASCII 艺术）"""
    if not data:
        return f"{title}\n\n数据不足\n"
    
    # 提取数据
    labels = [item.get('label', str(i)) for i, item in enumerate(data)]
    values = [item.get('value', 0) for item in data]
    
    if not values:
        return f"{title}\n\n数据不足\n"
    
    max_val = max(values)
    min_val = min(values)
    range_val = max_val - min_val if max_val != min_val else 1
    
    # 生成图表
    lines = []
    lines.append(f"{'=' * width}")
    lines.append(f"{title}")
    lines.append(f"{'=' * width}")
    lines.append("")
    
    # Y 轴刻度
    for row in range(height, -1, -1):
        threshold = min_val + (range_val * row / height)
        label = f"{threshold:>10.0f}" if row == height else f"{threshold:>10.0f}" if row == 0 else " " * 10
        line = f"{label} │"
        
        for i, val in enumerate(values):
            if val >= threshold:
                line += "█"
            else:
                line += " "
        
        lines.append(line)
    
    # X 轴
    lines.append(" " * 11 + "└" + "─" * len(values))
    lines.append(" " * 12 + " ".join(labels[:len(values)]))
    lines.append("")
    lines.append(f"X 轴：{x_label}")
    lines.append(f"Y 轴：{y_label}")
    lines.append(f"最大值：{max_val:,}  最小值：{min_val:,}")
    lines.append(f"{'=' * width}")
    
    return "\n".join(lines)


def generate_trend_report():
    """生成趋势分析报告"""
    print("生成趋势分析报告...")
    
    # 加载各数据库数据
    robot_sales = load_csv_data(f"{WORKSPACE}/robot_data/产品价格历史趋势.csv")
    drone_sales = load_csv_data(f"{WORKSPACE}/drone_data/销量历史趋势.csv")
    clinical_rates = load_csv_data(f"{WORKSPACE}/clinical_trial_data/保险费率历史趋势.csv")
    
    robot_accidents = load_csv_data(f"{WORKSPACE}/robot_data/机器人事故案例库.csv")
    drone_accidents = load_csv_data(f"{WORKSPACE}/drone_data/无人机事故案例库.csv")
    clinical_accidents = load_csv_data(f"{WORKSPACE}/clinical_trial_data/临床试验事故案例库.csv")
    
    report = []
    report.append("# 📊 三数据库联合可视化报告")
    report.append("")
    report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("---")
    report.append("")
    
    # 1. 数据规模对比
    report.append("## 📈 数据规模对比")
    report.append("")
    report.append("| 数据库 | 历史记录数 | 事故案例数 |")
    report.append("|--------|-----------|-----------|")
    report.append(f"| 机器人 | {len(robot_sales)} | {len(robot_accidents)} |")
    report.append(f"| 无人机 | {len(drone_sales)} | {len(drone_accidents)} |")
    report.append(f"| 临床试验 | {len(clinical_rates)} | {len(clinical_accidents)} |")
    report.append("")
    
    # 2. 价格/销量趋势分析
    report.append("## 💰 价格/销量趋势")
    report.append("")
    
    # 机器人价格趋势
    if robot_sales:
        robot_brands = {}
        for record in robot_sales:
            brand = record.get('品牌', 'Unknown')
            if brand not in robot_brands:
                robot_brands[brand] = []
            try:
                price = int(record.get('价格', 0))
                robot_brands[brand].append(price)
            except:
                pass
        
        report.append("### 机器人价格趋势（按品牌）")
        report.append("")
        for brand, prices in robot_brands.items():
            if prices:
                avg_price = sum(prices) / len(prices)
                report.append(f"- **{brand}**: 平均 {avg_price:,.0f} 元，记录 {len(prices)} 条")
        report.append("")
    
    # 无人机销量趋势
    if drone_sales:
        drone_brands = {}
        for record in drone_sales:
            brand = record.get('品牌', 'Unknown')
            if brand not in drone_brands:
                drone_brands[brand] = []
            try:
                sales = int(record.get('销量', 0))
                drone_brands[brand].append(sales)
            except:
                pass
        
        report.append("### 无人机销量趋势（按品牌）")
        report.append("")
        for brand, sales_list in drone_brands.items():
            if sales_list:
                total_sales = sum(sales_list)
                avg_sales = total_sales / len(sales_list)
                report.append(f"- **{brand}**: 平均 {avg_sales:,.0f} 架，总计 {total_sales:,} 架")
        report.append("")
    
    # 3. 事故案例对比
    report.append("## ⚠️ 事故案例对比")
    report.append("")
    
    # 按类型统计
    def count_by_field(cases, field):
        counts = {}
        for case in cases:
            value = case.get(field, '未知')
            counts[value] = counts.get(value, 0) + 1
        return counts
    
    if robot_accidents:
        report.append("### 机器人事故类型分布")
        report.append("")
        types = count_by_field(robot_accidents, '事故类型')
        for acc_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * count
            report.append(f"- {acc_type}: {count} {bar}")
        report.append("")
    
    if drone_accidents:
        report.append("### 无人机事故类型分布")
        report.append("")
        types = count_by_field(drone_accidents, '事故类型')
        for acc_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * count
            report.append(f"- {acc_type}: {count} {bar}")
        report.append("")
    
    if clinical_accidents:
        report.append("### 临床试验事故类型分布")
        report.append("")
        types = count_by_field(clinical_accidents, '类型')
        for acc_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * count
            report.append(f"- {acc_type}: {count} {bar}")
        report.append("")
    
    # 4. 损失金额对比
    report.append("## 💸 损失金额对比")
    report.append("")
    
    def extract_loss(cases):
        import re
        total = 0
        count = 0
        for case in cases:
            loss_str = case.get('损失', '0')
            numbers = re.findall(r'\d+(?:\.\d+)?', loss_str)
            if numbers:
                total += sum(float(n) for n in numbers)
                count += 1
        return total, count
    
    robot_loss, robot_count = extract_loss(robot_accidents)
    drone_loss, drone_count = extract_loss(drone_accidents)
    clinical_loss, clinical_count = extract_loss(clinical_accidents)
    
    report.append("| 数据库 | 总损失 (万元) | 案例数 | 案均损失 (万元) |")
    report.append("|--------|------------|--------|---------------|")
    report.append(f"| 机器人 | {robot_loss:,.1f} | {robot_count} | {robot_loss/max(robot_count,1):,.1f} |")
    report.append(f"| 无人机 | {drone_loss:,.1f} | {drone_count} | {drone_loss/max(drone_count,1):,.1f} |")
    report.append(f"| 临床试验 | {clinical_loss:,.1f} | {clinical_count} | {clinical_loss/max(clinical_count,1):,.1f} |")
    report.append("")
    
    # 5. 文本图表
    report.append("## 📊 可视化图表")
    report.append("")
    
    # 事故数量对比图
    accident_data = [
        {'label': '机器人', 'value': len(robot_accidents)},
        {'label': '无人机', 'value': len(drone_accidents)},
        {'label': '临床试验', 'value': len(clinical_accidents)},
    ]
    chart = generate_text_chart(accident_data, "事故案例数量对比", "数据库", "案例数")
    report.append(f"```\n{chart}\n```")
    report.append("")
    
    # 损失金额对比图
    loss_data = [
        {'label': '机器人', 'value': robot_loss},
        {'label': '无人机', 'value': drone_loss},
        {'label': '临床试验', 'value': clinical_loss},
    ]
    chart = generate_text_chart(loss_data, "总损失金额对比 (万元)", "数据库", "损失 (万元)")
    report.append(f"```\n{chart}\n```")
    report.append("")
    
    # 6. 洞察与建议
    report.append("## 💡 洞察与建议")
    report.append("")
    
    # 自动分析
    insights = []
    
    if robot_accidents and drone_accidents and clinical_accidents:
        max_accidents = max(len(robot_accidents), len(drone_accidents), len(clinical_accidents))
        if len(clinical_accidents) == max_accidents:
            insights.append("🔴 临床试验事故案例最多，需加强风险管控")
        elif len(drone_accidents) == max_accidents:
            insights.append("🟠 无人机事故案例最多，需关注飞行安全")
        else:
            insights.append("🟡 机器人事故案例最多，需强化操作培训")
    
    if robot_loss > drone_loss and robot_loss > clinical_loss:
        insights.append("💰 机器人事故案均损失最高，建议提高保险保额")
    
    if len(robot_accidents) > 0 and len(drone_accidents) > 0 and len(clinical_accidents) > 0:
        insights.append("📊 三数据库已建立，可进行跨领域风险对比分析")
    
    for insight in insights:
        report.append(f"- {insight}")
    
    report.append("")
    report.append("---")
    report.append("")
    report.append(f"*报告生成完成，保存至：visualizations/三数据库联合分析报告.md*")
    
    # 保存报告
    report_file = f"{VISUALIZATION_DIR}/三数据库联合分析报告.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"报告已保存：{report_file}")
    return report_file


if __name__ == "__main__":
    generate_trend_report()
    print("\n✅ 可视化报告生成完成！")
