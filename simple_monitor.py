#!/usr/bin/env python3
"""
简化版股票监控系统
"""

import json
from datetime import datetime
from financial_analyzer import StockAnalyzer

def load_stocks():
    """加载股票列表"""
    try:
        with open('monitor_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('stocks', [])
    except FileNotFoundError:
        return [
            {'symbol': '300809', 'name': '华辰装备', 'alert_threshold': 5.0}
        ]

def analyze_all_stocks():
    """分析所有股票"""
    stocks = load_stocks()
    
    print("\n" + "="*70)
    print(f"股票分析报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    results = []
    
    for stock in stocks:
        symbol = stock['symbol']
        name = stock['name']
        
        print(f"\n📈 分析 {name}({symbol})...")
        
        analyzer = StockAnalyzer(symbol)
        
        if analyzer.fetch_data(start_date="2024-01-01"):
            analyzer.calculate_technical_indicators()
            
            # 执行分析
            trend = analyzer.analyze_trend()
            volatility = analyzer.analyze_volatility()
            support_resistance = analyzer.analyze_support_resistance()
            seasonality = analyzer.analyze_seasonality(year=2024)
            
            # 生成报告
            report = analyzer.generate_report()
            results.append(report)
            
            # 显示关键信息
            analysis = report['analysis_results']
            
            print(f"   当前价格: {analysis['trend']['current_price']:.2f}")
            print(f"   趋势状态: {analysis['trend']['trend_short']} | {analysis['trend']['trend_medium']} | {analysis['trend']['trend_long']}")
            print(f"   MA排列: {analysis['trend']['ma_alignment']}")
            print(f"   RSI: {analysis['trend']['rsi_status']}")
            print(f"   MACD: {analysis['trend']['macd_signal']}")
            print(f"   波动率: {analysis['volatility']['volatility_20d']:.1f}%")
            
            if 'support_resistance' in analysis:
                sr = analysis['support_resistance']
                print(f"   支撑位: {sr['support_level']:.2f} (+{sr['current_to_support']:.1f}%)")
                print(f"   阻力位: {sr['resistance_level']:.2f} (-{sr['current_to_resistance']:.1f}%)")
            
            # 春节后展望
            print(f"\n   🎯 春节后到5月份展望:")
            print(f"     当前处于: {analysis['trend']['trend_medium']}趋势")
            print(f"     关键技术位: MA20 = {analyzer.data['MA20'].iloc[-1]:.2f}")
            print(f"     建议观察: 价格能否突破关键技术位")
            
        else:
            print(f"  ✗ 数据获取失败")
    
    print("\n" + "="*70)
    print("分析完成")
    print("="*70)
    
    return results

def generate_insights_report(results):
    """生成洞察报告"""
    print("\n" + "="*70)
    print("投资洞察报告")
    print("="*70)
    
    for report in results:
        symbol = report['symbol']
        analysis = report['analysis_results']
        
        print(f"\n📊 {symbol} 投资洞察:")
        
        # 趋势判断
        trend = analysis['trend']
        if trend['ma_alignment'] == "多头排列" and trend['macd_signal'] == "金叉":
            print(f"   ✅ 技术面偏多: 均线多头排列 + MACD金叉")
        elif trend['ma_alignment'] == "空头排列" and trend['macd_signal'] == "死叉":
            print(f"   ⚠️ 技术面偏空: 均线空头排列 + MACD死叉")
        else:
            print(f"   🔄 技术面震荡: 等待方向选择")
        
        # 风险提示
        volatility = analysis['volatility']['volatility_20d']
        if volatility > 40:
            print(f"   ⚠️ 高风险: 波动率较高 ({volatility:.1f}%)")
        
        # 操作建议框架
        print(f"\n   🎯 操作框架:")
        print(f"     1. 关键观察: 价格与MA20的关系")
        print(f"     2. 入场时机: RSI超卖区域 + 价格接近支撑位")
        print(f"     3. 止损位置: 跌破近期支撑位")
        print(f"     4. 目标位置: 接近近期阻力位")
    
    print("\n" + "="*70)
    print("风险提示: 股市有风险，投资需谨慎")
    print("本报告仅为技术分析框架，不构成投资建议")
    print("="*70)

if __name__ == "__main__":
    # 分析所有股票
    results = analyze_all_stocks()
    
    # 生成洞察报告
    if results:
        generate_insights_report(results)
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"analysis_report_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'stocks_analyzed': len(results),
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 分析报告已保存: {output_file}")