#!/usr/bin/env python3
"""
股票分析器测试脚本
自动测试几个主要股票，然后退出
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from quick_stock_analyzer import QuickStockAnalyzer

def test_stocks():
    """测试几个主要股票"""
    analyzer = QuickStockAnalyzer()
    
    # 要测试的股票列表
    test_stocks = ['AAPL', 'MSFT', 'TSLA', 'BABA']
    
    print("🧪 开始测试股票分析器...")
    print("=" * 60)
    
    for i, symbol in enumerate(test_stocks, 1):
        print(f"\n📊 测试 {i}/{len(test_stocks)}: {symbol}")
        print("-" * 40)
        
        # 获取数据
        df = analyzer.get_stock_data(symbol, period="1mo")
        if df is None:
            print(f"❌ 无法获取 {symbol} 数据")
            continue
        
        # 计算指标
        df = analyzer.calculate_indicators(df)
        
        # 分析趋势
        analysis = analyzer.analyze_trend(df)
        
        # 生成报告
        analyzer.generate_report(symbol, df, analysis)
        
        # 绘制图表
        analyzer.plot_chart(symbol, df)
        
        print(f"✅ {symbol} 测试完成")
    
    print("\n" + "=" * 60)
    print("🎉 所有股票测试完成！")
    print("\n📁 生成的文件:")
    
    # 列出生成的文件
    import glob
    png_files = glob.glob("*_analysis_*.png")
    for file in png_files:
        print(f"   📄 {file}")
    
    print("\n💡 下一步:")
    print("   1. 运行 'python3 quick_stock_analyzer.py' 进行交互式分析")
    print("   2. 查看生成的图表文件")
    print("   3. 可以添加更多股票代码进行分析")

if __name__ == "__main__":
    test_stocks()