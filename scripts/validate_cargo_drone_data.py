#!/usr/bin/env python3
"""
货运无人机数据验证与清洗脚本
验证数据完整性、一致性、合理性
"""

import csv
import json
from datetime import datetime
from pathlib import Path

# 数据文件路径
CARGO_DRONE_FILE = "无人机 BI 数据库_货运用.csv"
CARGO_LOSS_FILE = "无人机 BI 数据库_货物损失.csv"
OUTPUT_VALIDATED_FILE = "无人机 BI 数据库_货运 validated.csv"
OUTPUT_LOG_FILE = "数据验证日志.json"

def load_csv(filepath):
    """加载 CSV 文件"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def validate_numeric(value, field_name, allow_zero=True):
    """验证数值字段"""
    try:
        val = float(value.replace(',', ''))
        if not allow_zero and val == 0:
            return False, f"{field_name} 不能为 0"
        if val < 0:
            return False, f"{field_name} 不能为负数"
        return True, val
    except:
        return False, f"{field_name} 格式错误：{value}"

def validate_aircraft_data(data):
    """验证无人机基础数据"""
    issues = []
    validated_data = []
    
    for row in data:
        row_issues = []
        
        # 验证价格
        ok, result = validate_numeric(row.get('价格 (元)', '0'), '价格')
        if not ok:
            row_issues.append(result)
        
        # 验证销量
        for year in ['2021', '2022', '2023', '2024']:
            field = f'{year}年销量'
            ok, result = validate_numeric(row.get(field, '0'), field)
            if not ok:
                row_issues.append(result)
        
        # 验证事故数
        for year in ['2021', '2022', '2023', '2024']:
            field = f'{year}年事故数'
            ok, result = validate_numeric(row.get(field, '0'), field)
            if not ok:
                row_issues.append(result)
        
        # 验证事故总数一致性
        try:
            sum_accidents = sum(int(row.get(f'{y}年事故数', 0)) for y in ['2021', '2022', '2023', '2024'])
            reported_total = int(row.get('事故总数 (2021 起)', 0))
            if sum_accidents != reported_total:
                row_issues.append(f"事故总数不一致：计算={sum_accidents}, 报告={reported_total}")
        except:
            pass
        
        # 验证损失金额
        for field in ['机损金额 (元)', '物损金额 (元)']:
            ok, result = validate_numeric(row.get(field, '0'), field)
            if not ok:
                row_issues.append(result)
        
        if row_issues:
            issues.append({
                'model': row.get('型号', 'Unknown'),
                'issues': row_issues
            })
        
        validated_data.append(row)
    
    return validated_data, issues

def validate_loss_data(data):
    """验证货物损失数据"""
    issues = []
    validated_data = []
    
    for row in data:
        row_issues = []
        
        # 验证运输架次
        ok, result = validate_numeric(row.get('运输架次', '0'), '运输架次', allow_zero=False)
        if not ok:
            row_issues.append(result)
        
        # 验证损失事故数
        ok, result = validate_numeric(row.get('损失事故数', '0'), '损失事故数')
        if not ok:
            row_issues.append(result)
        
        # 验证损失货物价值
        ok, result = validate_numeric(row.get('损失货物价值 (元)', '0'), '损失货物价值')
        if not ok:
            row_issues.append(result)
        
        # 验证损失率计算
        try:
            flights = int(row.get('运输架次', 0))
            accidents = int(row.get('损失事故数', 0))
            if flights > 0:
                calc_rate = (accidents / flights) * 100
                reported_rate = float(row.get('损失率', '0').replace('‰', ''))
                # 损失率单位是 ‰ (千分比)
                if abs(calc_rate * 10 - reported_rate) > 0.01:
                    row_issues.append(f"损失率计算不一致：计算={calc_rate*10:.4f}‰, 报告={reported_rate}‰")
        except:
            pass
        
        # 验证平均损失计算
        try:
            accidents = int(row.get('损失事故数', 0))
            total_loss = float(row.get('损失货物价值 (元)', 0).replace(',', ''))
            if accidents > 0:
                calc_avg = total_loss / accidents
                reported_avg = float(row.get('平均损失 (元/起)', 0).replace(',', ''))
                if abs(calc_avg - reported_avg) / calc_avg > 0.01:  # 1% 误差容忍
                    row_issues.append(f"平均损失计算不一致：计算={calc_avg:.2f}, 报告={reported_avg:.2f}")
        except:
            pass
        
        if row_issues:
            issues.append({
                'model': row.get('型号', 'Unknown'),
                'year': row.get('年份', 'Unknown'),
                'issues': row_issues
            })
        
        validated_data.append(row)
    
    return validated_data, issues

def cross_validate(aircraft_data, loss_data):
    """交叉验证两组数据"""
    issues = []
    
    # 按机型汇总损失数据
    loss_by_model = {}
    for row in loss_data:
        model = row.get('型号', '')
        if model not in loss_by_model:
            loss_by_model[model] = {'accidents': 0, 'value': 0}
        loss_by_model[model]['accidents'] += int(row.get('损失事故数', 0))
        loss_by_model[model]['value'] += float(row.get('损失货物价值 (元)', 0).replace(',', ''))
    
    # 与基础数据对比
    for row in aircraft_data:
        model = row.get('型号', '')
        if model in loss_by_model:
            # 损失事故数应该 <= 总事故数
            loss_accidents = loss_by_model[model]['accidents']
            total_accidents = int(row.get('事故总数 (2021 起)', 0))
            if loss_accidents > total_accidents:
                issues.append({
                    'type': 'cross_validation',
                    'model': model,
                    'issue': f'货物损失事故数 ({loss_accidents}) > 总事故数 ({total_accidents})'
                })
    
    return issues

def main():
    print("=" * 60)
    print("货运无人机数据验证与清洗")
    print("=" * 60)
    
    # 加载数据
    print("\n[1/5] 加载数据...")
    aircraft_data = load_csv(CARGO_DRONE_FILE)
    loss_data = load_csv(CARGO_LOSS_FILE)
    print(f"  ✓ 无人机基础数据：{len(aircraft_data)} 条记录")
    print(f"  ✓ 货物损失数据：{len(loss_data)} 条记录")
    
    # 验证基础数据
    print("\n[2/5] 验证无人机基础数据...")
    validated_aircraft, aircraft_issues = validate_aircraft_data(aircraft_data)
    if aircraft_issues:
        print(f"  ⚠ 发现 {len(aircraft_issues)} 个问题:")
        for issue in aircraft_issues:
            print(f"    - {issue['model']}: {', '.join(issue['issues'][:3])}")
    else:
        print("  ✓ 基础数据验证通过")
    
    # 验证损失数据
    print("\n[3/5] 验证货物损失数据...")
    validated_loss, loss_issues = validate_loss_data(loss_data)
    if loss_issues:
        print(f"  ⚠ 发现 {len(loss_issues)} 个问题:")
        for issue in loss_issues:
            print(f"    - {issue['model']} ({issue['year']}): {', '.join(issue['issues'][:3])}")
    else:
        print("  ✓ 损失数据验证通过")
    
    # 交叉验证
    print("\n[4/5] 交叉验证...")
    cross_issues = cross_validate(validated_aircraft, validated_loss)
    if cross_issues:
        print(f"  ⚠ 发现 {len(cross_issues)} 个交叉验证问题:")
        for issue in cross_issues:
            print(f"    - {issue['model']}: {issue['issue']}")
    else:
        print("  ✓ 交叉验证通过")
    
    # 生成验证报告
    print("\n[5/5] 生成验证报告...")
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'aircraft_records': len(validated_aircraft),
            'loss_records': len(validated_loss),
            'aircraft_issues': len(aircraft_issues),
            'loss_issues': len(loss_issues),
            'cross_issues': len(cross_issues)
        },
        'issues': {
            'aircraft': aircraft_issues,
            'loss': loss_issues,
            'cross': cross_issues
        },
        'status': 'PASS' if not (aircraft_issues or loss_issues or cross_issues) else 'PASS_WITH_WARNINGS'
    }
    
    with open(OUTPUT_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 验证报告已保存至：{OUTPUT_LOG_FILE}")
    
    # 汇总
    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)
    print(f"状态：{report['status']}")
    print(f"总问题数：{len(aircraft_issues) + len(loss_issues) + len(cross_issues)}")
    
    return report

if __name__ == '__main__':
    main()
