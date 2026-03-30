#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动获取资本市场和宏观经济数据脚本
数据源：AkShare (免费开源，聚合东方财富、新浪财经等)
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import json
import os

# ============== 配置 ==============
OUTPUT_DIR = "./finance_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============== 宏观经济数据 ==============
def get_macro_data():
    """获取宏观经济指标"""
    print("📊 获取宏观经济数据...")
    
    macro = {}
    
    # GDP 数据
    try:
        gdp = ak.macro_gdp_year()
        macro['GDP'] = gdp.to_dict('records')[-5:]  # 最近 5 年
        print("  ✓ GDP 数据")
    except Exception as e:
        print(f"  ✗ GDP 获取失败：{e}")
    
    # CPI 数据
    try:
        cpi = ak.macro_cpi_year()
        macro['CPI'] = cpi.to_dict('records')[-12:]  # 最近 12 期
        print("  ✓ CPI 数据")
    except Exception as e:
        print(f"  ✗ CPI 获取失败：{e}")
    
    # PPI 数据
    try:
        ppi = ak.macro_ppi_year()
        macro['PPI'] = ppi.to_dict('records')[-12:]
        print("  ✓ PPI 数据")
    except Exception as e:
        print(f"  ✗ PPI 获取失败：{e}")
    
    # 货币供应量
    try:
        m2 = ak.macro_money_supply_month()
        macro['M2'] = m2.to_dict('records')[-12:]
        print("  ✓ M2 数据")
    except Exception as e:
        print(f"  ✗ M2 获取失败：{e}")
    
    # 社会融资规模
    try:
        shirong = ak.macro_social_finance_month()
        macro['社会融资'] = shirong.to_dict('records')[-12:]
        print("  ✓ 社会融资规模数据")
    except Exception as e:
        print(f"  ✗ 社会融资获取失败：{e}")
    
    return macro

# ============== 资本市场数据 ==============
def get_market_data():
    """获取资本市场数据"""
    print("📈 获取资本市场数据...")
    
    market = {}
    
    # 主要指数实时行情
    indices = {
        '上证指数': 'sh000001',
        '深证成指': 'sz399001',
        '创业板指': 'sz399006',
        '沪深 300': 'sh000300',
        '科创 50': 'sh000688',
    }
    
    index_data = []
    for name, code in indices.items():
        try:
            if code.startswith('sh'):
                df = ak.stock_zh_index_daily(symbol=code)
            else:
                df = ak.stock_zh_index_daily(symbol=code)
            latest = df.iloc[-1].to_dict()
            latest['指数名称'] = name
            latest['代码'] = code
            index_data.append(latest)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name} 获取失败：{e}")
    
    market['主要指数'] = index_data
    
    # 北向资金
    try:
        north = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")
        market['北向资金'] = north.tail(10).to_dict('records')
        print("  ✓ 北向资金数据")
    except Exception as e:
        print(f"  ✗ 北向资金获取失败：{e}")
    
    # 融资融券
    try:
        rzmf = ak.stock_margin_sse()
        market['融资融券'] = rzmf.tail(10).to_dict('records')
        print("  ✓ 融资融券数据")
    except Exception as e:
        print(f"  ✗ 融资融券获取失败：{e}")
    
    # 涨跌分布
    try:
        zt = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
        market['涨停池'] = len(zt) if len(zt) > 0 else 0
        print("  ✓ 涨跌停统计")
    except Exception as e:
        print(f"  ✗ 涨跌停获取失败：{e}")
    
    return market

# ============== 行业数据 ==============
def get_industry_data():
    """获取行业板块数据"""
    print("🏭 获取行业数据...")
    
    industry = {}
    
    # 申万一级行业
    try:
        sw = ak.stock_board_industry_name_em()
        industry['申万行业列表'] = sw.head(20).to_dict('records')
        print(f"  ✓ 申万行业 ({len(sw)} 个)")
    except Exception as e:
        print(f"  ✗ 申万行业获取失败：{e}")
    
    return industry

# ============== 商品期货 ==============
def get_commodity_data():
    """获取大宗商品数据"""
    print("🛢️ 获取大宗商品数据...")
    
    commodity = {}
    
    # 国内期货
    try:
        futures = ak.futures_main_sina()
        commodity['期货行情'] = futures.head(20).to_dict('records')
        print("  ✓ 期货行情")
    except Exception as e:
        print(f"  ✗ 期货获取失败：{e}")
    
    return commodity

# ============== 汇率 ==============
def get_fx_data():
    """获取汇率数据"""
    print("💱 获取汇率数据...")
    
    fx = {}
    
    try:
        usd = ak.currency_boc_sina(symbol="美元", start="20240101", end=datetime.now().strftime('%Y%m%d'))
        fx['USD/CNY'] = usd.tail(30).to_dict('records')
        print("  ✓ 美元汇率")
    except Exception as e:
        print(f"  ✗ 汇率获取失败：{e}")
    
    return fx

# ============== 主函数 ==============
def main():
    print("=" * 50)
    print(f"🚀 金融数据自动采集")
    print(f"📅 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    all_data = {
        'timestamp': datetime.now().isoformat(),
        '宏观经济': get_macro_data(),
        '资本市场': get_market_data(),
        '行业板块': get_industry_data(),
        '大宗商品': get_commodity_data(),
        '外汇汇率': get_fx_data(),
    }
    
    # 保存 JSON
    output_file = f"{OUTPUT_DIR}/finance_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 数据已保存：{output_file}")
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("📋 数据摘要")
    print("=" * 50)
    
    if '主要指数' in all_data['资本市场']:
        print("\n主要指数:")
        for idx in all_data['资本市场']['主要指数']:
            if '最新价' in idx:
                print(f"  {idx['指数名称']}: {idx['最新价']}")
    
    print(f"\n✅ 采集完成!")
    
    return all_data

if __name__ == "__main__":
    main()
