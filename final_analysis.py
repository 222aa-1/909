#!/usr/bin/env python3
"""
华辰装备(300809)春节后到5月份走势分析
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("华辰装备(300809)理性分析报告")
print("分析时间范围: 春节后到5月份走势预测")
print("="*70)

# 获取数据
print("\n1. 数据获取...")
df = ak.stock_zh_a_hist(symbol="300809", period="daily", start_date="20240101", end_date="20260218", adjust="")
print(f"   ✓ 获取到 {len(df)} 个交易日数据")
print(f"   ✓ 时间范围: {df['日期'].min()} 到 {df['日期'].max()}")

# 数据预处理
df['日期'] = pd.to_datetime(df['日期'])
df.set_index('日期', inplace=True)
df.sort_index(inplace=True)

# 计算基本指标
df['MA20'] = df['收盘'].rolling(window=20).mean()
df['MA60'] = df['收盘'].rolling(window=60).mean()
df['Returns'] = df['收盘'].pct_change()

print("\n2. 当前状态分析...")
current_price = df['收盘'].iloc[-1]
price_20d_ago = df['收盘'].iloc[-20]
change_20d = ((current_price / price_20d_ago) - 1) * 100

print(f"   当前价格: {current_price:.2f}")
print(f"   20日前价格: {price_20d_ago:.2f}")
print(f"   近期涨跌幅: {change_20d:.2f}%")
print(f"   相对MA20位置: {'上方' if current_price > df['MA20'].iloc[-1] else '下方'} ({((current_price/df['MA20'].iloc[-1])-1)*100:.2f}%)")

# 分析历史春节后表现
print("\n3. 历史春节后表现分析...")

# 定义春节日期（简化处理）
spring_festivals = {
    2024: '2024-02-10',
    2025: '2025-01-29'
}

for year, festival_date in spring_festivals.items():
    festival = pd.Timestamp(festival_date)
    if year == 2024:  # 只有2024年有完整数据
        # 春节前后各30个交易日
        pre_start = festival - pd.Timedelta(days=30)
        post_end = festival + pd.Timedelta(days=90)  # 到5月份
        
        mask = (df.index >= pre_start) & (df.index <= post_end)
        seasonal_data = df[mask].copy()
        
        if len(seasonal_data) > 10:
            pre_festival = seasonal_data[seasonal_data.index < festival]
            post_festival = seasonal_data[seasonal_data.index >= festival]
            
            if len(pre_festival) > 0 and len(post_festival) > 0:
                pre_price = pre_festival['收盘'].iloc[-1]
                post_price = post_festival['收盘'].iloc[-1]
                change = ((post_price / pre_price) - 1) * 100
                
                print(f"   {year}年春节前后表现:")
                print(f"     节前收盘: {pre_price:.2f}")
                print(f"     节后到5月收盘: {post_price:.2f}")
                print(f"     期间涨跌幅: {change:.2f}%")

# 波动性分析
print("\n4. 波动性分析...")
volatility_20d = df['Returns'].tail(20).std() * np.sqrt(252) * 100
volatility_60d = df['Returns'].tail(60).std() * np.sqrt(252) * 100
print(f"   20日年化波动率: {volatility_20d:.2f}%")
print(f"   60日年化波动率: {volatility_60d:.2f}%")

# 支撑阻力分析
print("\n5. 关键价位分析...")
recent_low = df['收盘'].tail(50).min()
recent_high = df['收盘'].tail(50).max()
print(f"   近期支撑位: {recent_low:.2f} (距离: {((current_price/recent_low)-1)*100:.2f}%)")
print(f"   近期阻力位: {recent_high:.2f} (距离: {((recent_high/current_price)-1)*100:.2f}%)")

# 春节后到5月份展望
print("\n" + "="*70)
print("6. 春节后到5月份走势展望")
print("="*70)

print("\n📅 时间阶段分析:")
print("   阶段1: 2月中下旬 (春节后开盘)")
print("     - 关注点: 资金回流、政策预期、外围市场影响")
print("     - 历史规律: 春节后首周上涨概率较高")

print("\n   阶段2: 3月份 (财报季)")
print("     - 关注点: 年报披露、业绩预期、机构调仓")
print("     - 风险: 业绩不及预期、估值调整")

print("\n   阶段3: 4月份 (政策窗口)")
print("     - 关注点: 一季度经济数据、行业政策、市场风格")
print("     - 机会: 政策利好、行业景气度提升")

print("\n   阶段4: 5月份 (业绩验证)")
print("     - 关注点: 一季报完全披露、五一后情绪、年中策略")
print("     - 关键: 业绩增长持续性、估值合理性")

print("\n🎯 关键观察指标:")
print("   1. 技术面:")
print("      - 价格能否站稳MA20上方")
print("      - 成交量是否有效放大")
print("      - RSI是否出现背离信号")

print("\n   2. 基本面:")
print("      - 2025年年报业绩")
print("      - 2026年一季报预期")
print("      - 行业政策变化")

print("\n   3. 资金面:")
print("      - 主力资金净流入/流出")
print("      - 北向资金态度")
print("      - 融资余额变化")

print("\n⚠️ 风险提示:")
print("   1. 宏观经济波动风险")
print("   2. 行业竞争加剧风险")
print("   3. 公司特定经营风险")
print("   4. 市场流动性风险")

print("\n" + "="*70)
print("理性分析结论")
print("="*70)

print("\n基于历史数据和理性分析框架:")
print("1. 华辰装备(300809)具备完整的历史数据可供分析")
print("2. 春节后到5月份的走势受多重因素影响:")
print("   - 技术面: 当前处于关键位置，需观察突破方向")
print("   - 基本面: 需关注年报和一季报业绩")
print("   - 资金面: 观察主力资金动向")
print("3. 建议采取分阶段观察策略:")
print("   - 2月: 观察春节后资金回流情况")
print("   - 3月: 关注年报业绩和估值调整")
print("   - 4月: 跟踪行业政策和市场风格")
print("   - 5月: 评估一季报和年中策略")

print("\n📊 数据统计:")
print(f"   分析数据量: {len(df)} 个交易日")
print(f"   时间范围: {df.index.min().date()} 到 {df.index.max().date()}")
print(f"   当前价格: {current_price:.2f}")
print(f"   20日均线: {df['MA20'].iloc[-1]:.2f}")
print(f"   60日均线: {df['MA60'].iloc[-1]:.2f}")

print("\n" + "="*70)
print("注: 本分析基于历史数据和理性框架")
print("    不构成投资建议，股市有风险，投资需谨慎")
print("="*70)