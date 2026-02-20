#!/usr/bin/env python3
"""
华辰装备详细分析脚本
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac上的中文字体
plt.rcParams['axes.unicode_minus'] = False

def get_stock_data(symbol="300809", start_date="2024-01-01"):
    """获取股票历史数据"""
    print(f"获取股票数据: {symbol}，从 {start_date}")
    
    try:
        # 尝试获取数据
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date="2026-02-18", adjust="qfq")
        
        if df.empty:
            print("数据获取失败，尝试其他方法...")
            return None
        
        print(f"获取到 {len(df)} 条数据")
        print(f"时间范围: {df['日期'].min()} 到 {df['日期'].max()}")
        
        # 转换日期格式
        df['日期'] = pd.to_datetime(df['日期'])
        df.set_index('日期', inplace=True)
        
        return df
    
    except Exception as e:
        print(f"数据获取错误: {e}")
        return None

def calculate_technical_indicators(df):
    """计算技术指标"""
    print("\n计算技术指标...")
    
    # 移动平均线
    df['MA5'] = df['收盘'].rolling(window=5).mean()
    df['MA20'] = df['收盘'].rolling(window=20).mean()
    df['MA60'] = df['收盘'].rolling(window=60).mean()
    
    # RSI
    delta = df['收盘'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['收盘'].ewm(span=12, adjust=False).mean()
    exp2 = df['收盘'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    
    # 布林带
    df['BB_middle'] = df['收盘'].rolling(window=20).mean()
    bb_std = df['收盘'].rolling(window=20).std()
    df['BB_upper'] = df['BB_middle'] + 2 * bb_std
    df['BB_lower'] = df['BB_middle'] - 2 * bb_std
    
    print("技术指标计算完成")
    return df

def analyze_seasonal_pattern(df, year=2025):
    """分析季节性模式"""
    print(f"\n分析 {year} 年季节性模式...")
    
    # 提取春节前后数据（假设春节在2月10日）
    spring_festival = pd.Timestamp(f'{year}-02-10')
    pre_period = spring_festival - pd.Timedelta(days=30)
    post_period = spring_festival + pd.Timedelta(days=90)  # 到5月份
    
    mask = (df.index >= pre_period) & (df.index <= post_period)
    seasonal_data = df[mask].copy()
    
    if len(seasonal_data) > 0:
        print(f"春节前后数据: {len(seasonal_data)} 个交易日")
        print(f"价格变化: {seasonal_data['收盘'].iloc[0]:.2f} -> {seasonal_data['收盘'].iloc[-1]:.2f}")
        print(f"涨跌幅: {((seasonal_data['收盘'].iloc[-1] / seasonal_data['收盘'].iloc[0]) - 1) * 100:.2f}%")
    else:
        print("没有找到对应时间段的数据")
    
    return seasonal_data

def generate_analysis_report(df, symbol="300809"):
    """生成分析报告"""
    print("\n" + "="*60)
    print("华辰装备股票分析报告")
    print("="*60)
    
    if df is None or len(df) < 60:
        print("数据不足，无法进行详细分析")
        return
    
    # 近期表现
    recent = df.tail(20)
    current_price = df['收盘'].iloc[-1]
    price_20d_ago = df['收盘'].iloc[-20]
    change_20d = ((current_price / price_20d_ago) - 1) * 100
    
    print(f"\n1. 近期表现 (最近20个交易日):")
    print(f"   当前价格: {current_price:.2f}")
    print(f"   20日前价格: {price_20d_ago:.2f}")
    print(f"   涨跌幅: {change_20d:.2f}%")
    
    # 技术指标状态
    print(f"\n2. 技术指标状态:")
    print(f"   RSI(14): {df['RSI'].iloc[-1]:.2f} - {'超买' if df['RSI'].iloc[-1] > 70 else '超卖' if df['RSI'].iloc[-1] < 30 else '中性'}")
    print(f"   MACD: {df['MACD'].iloc[-1]:.4f} - {'看涨' if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] else '看跌'}")
    
    # 移动平均线分析
    print(f"\n3. 移动平均线分析:")
    print(f"   价格 vs MA5: {current_price:.2f} vs {df['MA5'].iloc[-1]:.2f} - {'上方' if current_price > df['MA5'].iloc[-1] else '下方'}")
    print(f"   价格 vs MA20: {current_price:.2f} vs {df['MA20'].iloc[-1]:.2f} - {'上方' if current_price > df['MA20'].iloc[-1] else '下方'}")
    print(f"   MA5 vs MA20: {df['MA5'].iloc[-1]:.2f} vs {df['MA20'].iloc[-1]:.2f} - {'金叉' if df['MA5'].iloc[-1] > df['MA20'].iloc[-1] else '死叉'}")
    
    # 波动性分析
    volatility = df['收盘'].pct_change().std() * np.sqrt(252) * 100
    print(f"\n4. 波动性分析:")
    print(f"   年化波动率: {volatility:.2f}%")
    
    # 支撑阻力位
    support = df['收盘'].tail(50).min()
    resistance = df['收盘'].tail(50).max()
    print(f"\n5. 关键价位:")
    print(f"   近期支撑位: {support:.2f}")
    print(f"   近期阻力位: {resistance:.2f}")
    print(f"   当前距离支撑: {((current_price / support) - 1) * 100:.2f}%")
    print(f"   当前距离阻力: {((resistance / current_price) - 1) * 100:.2f}%")
    
    # 春节后到5月份展望
    print(f"\n6. 春节后到5月份展望:")
    print(f"   时间框架: 2月中下旬 到 5月底 (约3个月)")
    print(f"   关键因素:")
    print(f"     - 3月: 年报披露季，关注业绩表现")
    print(f"     - 4月: 一季报披露，政策窗口期")
    print(f"     - 5月: 五一假期后，市场情绪变化")
    
    # 风险提示
    print(f"\n7. 风险提示:")
    print(f"   - 需要确认准确的股票代码")
    print(f"   - 历史表现不代表未来")
    print(f"   - 股市有风险，投资需谨慎")
    
    print("\n" + "="*60)
    print("注: 此为技术分析框架，不构成投资建议")
    print("实际投资需结合基本面、市场环境等多因素")
    print("="*60)

def plot_charts(df, symbol="300809"):
    """绘制图表"""
    if df is None or len(df) < 60:
        print("数据不足，无法绘制图表")
        return
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # 1. 价格和移动平均线
    ax1 = axes[0]
    ax1.plot(df.index, df['收盘'], label='收盘价', linewidth=1)
    ax1.plot(df.index, df['MA20'], label='MA20', linewidth=1, alpha=0.7)
    ax1.plot(df.index, df['MA60'], label='MA60', linewidth=1, alpha=0.7)
    ax1.set_title(f'{symbol} - 价格走势')
    ax1.set_ylabel('价格')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. RSI
    ax2 = axes[1]
    ax2.plot(df.index, df['RSI'], label='RSI(14)', linewidth=1, color='orange')
    ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='超买线')
    ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='超卖线')
    ax2.set_title('RSI指标')
    ax2.set_ylabel('RSI')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. MACD
    ax3 = axes[2]
    ax3.plot(df.index, df['MACD'], label='MACD', linewidth=1)
    ax3.plot(df.index, df['Signal'], label='Signal', linewidth=1)
    ax3.bar(df.index, df['Histogram'], label='Histogram', alpha=0.3, width=0.8)
    ax3.set_title('MACD指标')
    ax3.set_ylabel('MACD')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{symbol}_analysis.png', dpi=150, bbox_inches='tight')
    print(f"\n图表已保存: {symbol}_analysis.png")
    plt.show()

def main():
    print("华辰装备详细分析")
    print("="*50)
    
    # 股票代码（需要确认）
    symbol = "300809"  # 假设的代码，需要确认
    
    # 获取数据
    df = get_stock_data(symbol=symbol, start_date="2024-01-01")
    
    if df is not None:
        # 计算技术指标
        df = calculate_technical_indicators(df)
        
        # 分析季节性模式
        seasonal_2025 = analyze_seasonal_pattern(df, year=2025)
        
        # 生成报告
        generate_analysis_report(df, symbol)
        
        # 绘制图表
        plot_charts(df.tail(120), symbol)  # 最近120个交易日
        
        print(f"\n分析完成!")
        print(f"数据时间范围: {df.index.min().date()} 到 {df.index.max().date()}")
        print(f"总交易日数: {len(df)}")
    else:
        print("\n数据获取失败，可能原因:")
        print("1. 股票代码不正确")
        print("2. 网络连接问题")
        print("3. 数据源限制")
        print("\n建议:")
        print("1. 确认华辰装备的正确股票代码")
        print("2. 检查网络连接")
        print("3. 尝试其他数据源")

if __name__ == "__main__":
    main()