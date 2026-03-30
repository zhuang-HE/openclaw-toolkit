#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器人数据库销售数据合并脚本
将销售数据整合到主数据库中
"""

import csv

# 读取销售数据
sales_data = {}
with open('/home/admin/.openclaw/workspace/机器人销售数据_核心版.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        # 清理 None 键
        row = {k: v for k, v in row.items() if k is not None}
        # 使用 公司 + 品牌 + 型号 作为唯一键
        key = f"{row['公司全称']}|{row['品牌']}|{row['型号']}"
        sales_data[key] = row

print(f"已加载 {len(sales_data)} 条销售数据")

# 读取主数据库并合并
merged_rows = []
fieldnames = None

with open('/home/admin/.openclaw/workspace/机器人数据库_核心版.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=',')
    original_fieldnames = [x for x in reader.fieldnames if x is not None]
    fieldnames = original_fieldnames + [
        '2023 年销量', '2024 年销量', '2025 年销量', '累计销量', 
        '2025 年市占率', '2025 年营收 (万元)', '核心客户类型', 
        '海外销量占比', '毛利率', '销售数据来源'
    ]
    
    for row in reader:
        # 清理 None 键
        row = {k: v for k, v in row.items() if k is not None}
        
        # 构建匹配键
        key = f"{row['公司全称']}|{row['品牌']}|{row['型号']}"
        
        # 尝试匹配销售数据
        if key in sales_data:
            sales = sales_data[key]
            row['2023 年销量'] = sales.get('2023 年销量', '')
            row['2024 年销量'] = sales.get('2024 年销量', '')
            row['2025 年销量'] = sales.get('2025 年销量', '')
            row['累计销量'] = sales.get('累计销量', '')
            row['2025 年市占率'] = sales.get('2025 年市占率', '')
            row['2025 年营收 (万元)'] = sales.get('2025 年营收 (万元)', '')
            row['核心客户类型'] = sales.get('核心客户类型', '')
            row['海外销量占比'] = sales.get('海外销量占比', '')
            row['毛利率'] = sales.get('毛利率', '')
            row['销售数据来源'] = sales.get('数据来源', '')
        else:
            # 未匹配到销售数据，填充空值
            row['2023 年销量'] = ''
            row['2024 年销量'] = ''
            row['2025 年销量'] = ''
            row['累计销量'] = ''
            row['2025 年市占率'] = ''
            row['2025 年营收 (万元)'] = ''
            row['核心客户类型'] = ''
            row['海外销量占比'] = ''
            row['毛利率'] = ''
            row['销售数据来源'] = ''
        
        merged_rows.append(row)

print(f"已合并 {len(merged_rows)} 条产品数据")

# 写入合并后的数据
with open('/home/admin/.openclaw/workspace/机器人数据库_完整版.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',', extrasaction='ignore')
    writer.writeheader()
    writer.writerows(merged_rows)

# 统计匹配情况
matched = sum(1 for r in merged_rows if r.get('2025 年销量', '') != '')
print(f"匹配到销售数据的产品：{matched}/{len(merged_rows)} ({matched*100//len(merged_rows)}%)")
print(f"未匹配到销售数据的产品：{len(merged_rows)-matched}")

# 输出匹配详情
print("\n=== 已匹配销售数据的产品 (前 25 条) ===")
count = 0
for r in merged_rows:
    if r.get('2025 年销量', '') != '' and count < 25:
        print(f"  {r['公司简称']} - {r['型号']}: 2025 年销量={r['2025 年销量']}, 市占率={r['2025 年市占率']}")
        count += 1

print("\n=== 数据合并完成 ===")
print(f"输出文件：/home/admin/.openclaw/workspace/机器人数据库_完整版.csv")
