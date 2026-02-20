#!/usr/bin/env python3
"""
中国股票分析器 - 专门分析A股股票
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ChinaStockAnalyzer:
    """中国股票分析器"""
    
    def __init__(self):
        print("📈 中国股票分析器 v1.0")
        print("=" * 60)
        
    def get_stock_info(self, symbol):
        """获取股票基本信息"""
        # 清理股票代码
        symbol = str(symbol).strip()
        
        # 添加交易所后缀
        if symbol.startswith('6'):
            symbol = symbol + '.SH'  # 上海
        elif symbol.startswith('0') or symbol.startswith('3'):
            symbol = symbol + '.SZ'  # 深圳
        elif symbol.startswith('8'):
            symbol = symbol + '.BJ'  # 北京
        
        print(f"🔍 分析股票: {symbol}")
        
        # 模拟数据 - 实际应用中应该调用真实API
        stock_info = self.get_mock_stock_data(symbol)
        
        return stock_info
    
    def get_mock_stock_data(self, symbol):
        """生成模拟股票数据"""
        # 根据股票代码生成不同的模拟数据
        base_info = {
            'symbol': symbol,
            'name': self.get_stock_name(symbol),
            'industry': self.get_industry(symbol),
            'market_cap': np.random.uniform(20, 100),  # 亿
            'pe_ratio': np.random.uniform(15, 40),
            'pb_ratio': np.random.uniform(1.5, 5),
            'roe': np.random.uniform(8, 20),
            'revenue_growth': np.random.uniform(-5, 30),
            'profit_growth': np.random.uniform(-10, 40),
        }
        
        # 生成30天价格数据
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        base_price = np.random.uniform(10, 150)
        
        np.random.seed(hash(symbol) % 10000)
        returns = np.random.normal(0.001, 0.025, 30)
        
        prices = [base_price]
        for r in returns:
            prices.append(prices[-1] * (1 + r))
        prices = prices[1:]
        
        price_data = {
            'dates': dates.strftime('%Y-%m-%d').tolist(),
            'prices': [round(p, 2) for p in prices],
            'volumes': [int(np.random.uniform(1000000, 50000000)) for _ in range(30)],
            'current_price': round(prices[-1], 2),
            'price_change': round(prices[-1] - prices[-2], 2) if len(prices) > 1 else 0,
            'price_change_pct': round(((prices[-1] - prices[-2]) / prices[-2] * 100), 2) if len(prices) > 1 else 0,
        }
        
        return {
            'base_info': base_info,
            'price_data': price_data,
            'analysis': self.analyze_stock(base_info, price_data)
        }
    
    def get_stock_name(self, symbol):
        """根据代码获取股票名称"""
        name_map = {
            '300809.SZ': '华辰装备',
            '000001.SZ': '平安银行',
            '000002.SZ': '万科A',
            '600519.SH': '贵州茅台',
            '601318.SH': '中国平安',
            '000858.SZ': '五粮液',
            '002415.SZ': '海康威视',
            '300750.SZ': '宁德时代',
            '600036.SH': '招商银行',
            '000333.SZ': '美的集团',
        }
        return name_map.get(symbol, f'股票{symbol}')
    
    def get_industry(self, symbol):
        """根据代码获取行业"""
        industry_map = {
            '300809.SZ': '机械设备-专用设备',
            '000001.SZ': '银行',
            '600519.SH': '食品饮料-白酒',
            '601318.SH': '非银金融-保险',
            '300750.SZ': '电力设备-电池',
            '002415.SZ': '电子-安防设备',
        }
        return industry_map.get(symbol, '未知行业')
    
    def analyze_stock(self, base_info, price_data):
        """综合分析股票"""
        analysis = {}
        
        # 基本面分析
        analysis['fundamental'] = self.analyze_fundamental(base_info)
        
        # 技术面分析
        analysis['technical'] = self.analyze_technical(price_data)
        
        # 估值分析
        analysis['valuation'] = self.analyze_valuation(base_info)
        
        # 风险分析
        analysis['risk'] = self.analyze_risk(base_info, price_data)
        
        # 买入建议
        analysis['recommendation'] = self.generate_recommendation(analysis)
        
        return analysis
    
    def analyze_fundamental(self, info):
        """基本面分析"""
        score = 0
        comments = []
        
        # PE分析
        if info['pe_ratio'] < 20:
            score += 2
            comments.append(f"✅ PE较低({info['pe_ratio']:.1f})，估值合理")
        elif info['pe_ratio'] < 30:
            score += 1
            comments.append(f"⚠️ PE适中({info['pe_ratio']:.1f})")
        else:
            score -= 1
            comments.append(f"❌ PE较高({info['pe_ratio']:.1f})，估值偏高")
        
        # ROE分析
        if info['roe'] > 15:
            score += 2
            comments.append(f"✅ ROE优秀({info['roe']:.1f}%)")
        elif info['roe'] > 10:
            score += 1
            comments.append(f"⚠️ ROE一般({info['roe']:.1f}%)")
        else:
            score -= 1
            comments.append(f"❌ ROE较低({info['roe']:.1f}%)")
        
        # 增长分析
        if info['revenue_growth'] > 20:
            score += 2
            comments.append(f"✅ 营收增长强劲({info['revenue_growth']:.1f}%)")
        elif info['revenue_growth'] > 0:
            score += 1
            comments.append(f"⚠️ 营收稳定增长({info['revenue_growth']:.1f}%)")
        else:
            score -= 1
            comments.append(f"❌ 营收下滑({info['revenue_growth']:.1f}%)")
        
        return {
            'score': score,
            'rating': '优秀' if score >= 4 else '良好' if score >= 2 else '一般' if score >= 0 else '较差',
            'comments': comments
        }
    
    def analyze_technical(self, price_data):
        """技术面分析"""
        prices = price_data['prices']
        current = prices[-1]
        
        # 计算技术指标
        ma_10 = np.mean(prices[-10:]) if len(prices) >= 10 else current
        ma_30 = np.mean(prices[-30:]) if len(prices) >= 30 else current
        
        # 趋势判断
        trend = '上涨' if current > prices[-2] else '下跌'
        ma_trend = '金叉' if ma_10 > ma_30 else '死叉'
        
        # 支撑阻力
        support = min(prices[-5:]) * 0.95
        resistance = max(prices[-5:]) * 1.05
        
        return {
            'current_price': current,
            'trend': trend,
            'ma_trend': ma_trend,
            'ma_10': round(ma_10, 2),
            'ma_30': round(ma_30, 2),
            'support': round(support, 2),
            'resistance': round(resistance, 2),
            'price_change': price_data['price_change'],
            'price_change_pct': price_data['price_change_pct']
        }
    
    def analyze_valuation(self, info):
        """估值分析"""
        # 简单估值模型
        fair_value = info['pe_ratio'] * info['roe'] / 100 * 10
        
        current_price = 100  # 假设当前价格
        upside = (fair_value - current_price) / current_price * 100
        
        return {
            'fair_value': round(fair_value, 2),
            'upside_potential': round(upside, 1),
            'valuation': '低估' if upside > 20 else '合理' if upside > -10 else '高估'
        }
    
    def analyze_risk(self, info, price_data):
        """风险分析"""
        risks = []
        
        # 估值风险
        if info['pe_ratio'] > 30:
            risks.append('估值过高风险')
        
        # 增长风险
        if info['revenue_growth'] < 0:
            risks.append('增长停滞风险')
        
        # 价格波动风险
        prices = price_data['prices']
        volatility = np.std(prices[-10:]) / np.mean(prices[-10:]) * 100 if len(prices) >= 10 else 0
        if volatility > 5:
            risks.append(f'高波动风险({volatility:.1f}%)')
        
        return {
            'risk_level': '高' if len(risks) >= 2 else '中' if len(risks) >= 1 else '低',
            'risks': risks
        }
    
    def generate_recommendation(self, analysis):
        """生成买入建议"""
        fundamental = analysis['fundamental']
        technical = analysis['technical']
        valuation = analysis['valuation']
        risk = analysis['risk']
        
        # 综合评分
        total_score = fundamental['score']
        
        if technical['trend'] == '上涨':
            total_score += 1
        else:
            total_score -= 1
        
        if valuation['valuation'] == '低估':
            total_score += 2
        elif valuation['valuation'] == '高估':
            total_score -= 2
        
        # 生成建议
        if total_score >= 4:
            recommendation = '强烈推荐买入'
            buy_range = f"{technical['support']:.2f}-{technical['current_price']:.2f}"
        elif total_score >= 2:
            recommendation = '推荐买入'
            buy_range = f"{technical['support']:.2f}-{technical['current_price']*0.98:.2f}"
        elif total_score >= 0:
            recommendation = '谨慎买入'
            buy_range = f"{technical['support']:.2f}-{technical['support']*1.02:.2f}"
        else:
            recommendation = '观望'
            buy_range = '等待更好时机'
        
        return {
            'recommendation': recommendation,
            'buy_range': buy_range,
            'target_price': round(technical['resistance'] * 1.1, 2),
            'stop_loss': round(technical['support'] * 0.95, 2),
            'confidence': '高' if total_score >= 3 else '中' if total_score >= 1 else '低'
        }
    
    def generate_report(self, symbol):
        """生成完整分析报告"""
        data = self.get_stock_info(symbol)
        
        print(f"\n📋 {data['base_info']['name']}({symbol}) 分析报告")
        print("=" * 60)
        
        # 基本信息
        print(f"\n📊 基本信息:")
        print(f"   股票代码: {data['base_info']['symbol']}")
        print(f"   股票名称: {data['base_info']['name']}")
        print(f"   所属行业: {data['base_info']['industry']}")
        print(f"   市值: {data['base_info']['market_cap']:.1f}亿元")
        
        # 财务指标
        print(f"\n💰 财务指标:")
        print(f"   市盈率(PE): {data['base_info']['pe_ratio']:.1f}")
        print(f"   市净率(PB): {data['base_info']['pb_ratio']:.1f}")
        print(f"   净资产收益率(ROE): {data['base_info']['roe']:.1f}%")
        print(f"   营收增长率: {data['base_info']['revenue_growth']:.1f}%")
        print(f"   利润增长率: {data['base_info']['profit_growth']:.1f}%")
        
        # 价格数据
        print(f"\n📈 价格数据:")
        print(f"   当前价格: ¥{data['price_data']['current_price']:.2f}")
        print(f"   涨跌幅: {data['price_data']['price_change_pct']:+.2f}%")
        print(f"   趋势: {data['analysis']['technical']['trend']}")
        print(f"   MA趋势: {data['analysis']['technical']['ma_trend']}")
        
        # 分析结果
        print(f"\n🎯 分析结果:")
        print(f"   基本面评级: {data['analysis']['fundamental']['rating']}")
        for comment in data['analysis']['fundamental']['comments']:
            print(f"     {comment}")
        
        print(f"\n   技术面分析:")
        print(f"     支撑位: ¥{data['analysis']['technical']['support']:.2f}")
        print(f"     阻力位: ¥{data['analysis']['technical']['resistance']:.2f}")
        print(f"     10日均线: ¥{data['analysis']['technical']['ma_10']:.2f}")
        print(f"     30日均线: ¥{data['analysis']['technical']['ma_30']:.2f}")
        
        print(f"\n   估值分析:")
        print(f"     合理价值: ¥{data['analysis']['valuation']['fair_value']:.2f}")
        print(f"     上涨空间: {data['analysis']['valuation']['upside_potential']:+.1f}%")
        print(f"     估值状态: {data['analysis']['valuation']['valuation']}")
        
        print(f"\n⚠️  风险提示:")
        print(f"     风险等级: {data['analysis']['risk']['risk_level']}")
        for risk in data['analysis']['risk']['risks']:
            print(f"     • {risk}")
        
        # 买入建议
        print(f"\n💡 买入建议:")
        print(f"     推荐: {data['analysis']['recommendation']['recommendation']}")
        print(f"     买入区间: ¥{data['analysis']['recommendation']['buy_range']}")
        print(f"     目标价格: ¥{data['analysis']['recommendation']['target_price']:.2f}")
        print(f"     止损价格: ¥{data['analysis']['recommendation']['stop_loss']:.2f}")
        print(f"     信心程度: {data['analysis']['recommendation']['confidence']}")
        
        print(f"\n⏰ 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return data

def main():
    """主函数"""
    analyzer = ChinaStockAnalyzer()
    
    print("📋 可分析股票示例:")
    stocks = ['300809', '000001', '600519', '300750', '002415']
    for i, stock in enumerate(stocks, 1):
        print(f"   {i}. {stock}")
    
    print("\n💡 提示: 可以输入其他A股代码，如 '000002' (万科A)")
    
    while True:
        symbol = input("\n请输入股票代码 (或输入 'quit' 退出): ").strip()
        
        if symbol.lower() == 'quit':
            print("👋 退出程序")
            break
            
        if not symbol:
            print("⚠️  请输入有效的股票代码")
            continue
        
        # 生成分析报告
        analyzer.generate_report(symbol)
        
        print(f"\n✅ {symbol} 分析完成！")

if __name__ == "__main__":
    main()