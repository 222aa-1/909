#!/usr/bin/env python3
"""
快速股票分析器 - 简化版
基于yfinance和pandas实现基本股票分析功能
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class QuickStockAnalyzer:
    """快速股票分析器"""
    
    def __init__(self):
        print("🚀 快速股票分析器 v1.0")
        print("=" * 50)
        
    def get_stock_data(self, symbol, period="1mo"):
        """获取股票数据"""
        print(f"📈 获取 {symbol} 股票数据 ({period})...")
        try:
            import time
            # 添加延迟避免频率限制
            time.sleep(1)
            
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            
            if df.empty:
                # 尝试其他数据源或本地缓存
                print(f"⚠️  未找到实时数据，使用示例数据演示")
                return self.get_sample_data(symbol)
            
            print(f"✅ 获取成功: {len(df)} 条记录")
            print(f"   时间范围: {df.index[0].date()} 到 {df.index[-1].date()}")
            return df
        except Exception as e:
            print(f"⚠️  获取实时数据失败: {e}")
            print("   使用示例数据演示功能...")
            return self.get_sample_data(symbol)
    
    def get_sample_data(self, symbol):
        """生成示例数据（当API受限时使用）"""
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        print(f"📊 为 {symbol} 生成示例数据...")
        
        # 生成30天的示例数据
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        # 基础价格（模拟不同股票）
        base_price = {
            'AAPL': 180.0, 'MSFT': 420.0, 'GOOGL': 150.0, 'TSLA': 180.0,
            'BABA': 80.0, 'JD': 30.0, 'NVDA': 800.0, 'AMZN': 180.0
        }.get(symbol, 100.0)
        
        # 生成随机但合理的价格序列
        np.random.seed(hash(symbol) % 10000)  # 使用股票代码作为随机种子
        returns = np.random.normal(0.001, 0.02, 30)  # 每日收益率
        
        prices = [base_price]
        for r in returns:
            prices.append(prices[-1] * (1 + r))
        prices = prices[1:]  # 去掉初始值
        
        # 创建DataFrame
        df = pd.DataFrame({
            'Open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
            'High': [p * (1 + np.random.uniform(0, 0.03)) for p in prices],
            'Low': [p * (1 - np.random.uniform(0, 0.03)) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000000, 50000000, 30)
        }, index=dates)
        
        print(f"✅ 示例数据生成完成: {len(df)} 条记录")
        print(f"   模拟价格范围: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
        return df
    
    def calculate_indicators(self, df):
        """计算技术指标"""
        print("📊 计算技术指标...")
        
        # 简单移动平均线
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_30'] = df['Close'].rolling(window=30).mean()
        
        # 相对强弱指数 (RSI)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 布林带
        df['BB_middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        
        print("✅ 技术指标计算完成")
        return df
    
    def analyze_trend(self, df):
        """分析趋势"""
        print("📈 分析趋势...")
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        analysis = {
            'current_price': latest['Close'],
            'price_change': latest['Close'] - prev['Close'],
            'price_change_pct': ((latest['Close'] - prev['Close']) / prev['Close']) * 100,
            'volume': latest['Volume'],
            'trend': '上涨' if latest['Close'] > prev['Close'] else '下跌',
            'sma_trend': '金叉' if latest['SMA_10'] > latest['SMA_30'] else '死叉',
            'rsi_level': '超买' if latest['RSI'] > 70 else '超卖' if latest['RSI'] < 30 else '正常',
            'bb_position': '上轨' if latest['Close'] > latest['BB_upper'] else '下轨' if latest['Close'] < latest['BB_lower'] else '中轨'
        }
        
        return analysis
    
    def generate_report(self, symbol, df, analysis):
        """生成分析报告"""
        print("\n" + "=" * 50)
        print(f"📋 {symbol} 股票分析报告")
        print("=" * 50)
        
        print(f"\n📊 基本信息:")
        print(f"   当前价格: ${analysis['current_price']:.2f}")
        print(f"   价格变化: ${analysis['price_change']:.2f} ({analysis['price_change_pct']:.2f}%)")
        print(f"   成交量: {analysis['volume']:,.0f}")
        print(f"   趋势: {analysis['trend']}")
        
        print(f"\n📈 技术指标:")
        print(f"   MA趋势: {analysis['sma_trend']} (10日: ${df['SMA_10'].iloc[-1]:.2f}, 30日: ${df['SMA_30'].iloc[-1]:.2f})")
        print(f"   RSI: {df['RSI'].iloc[-1]:.2f} - {analysis['rsi_level']}")
        print(f"   布林带位置: {analysis['bb_position']}")
        
        print(f"\n💡 交易建议:")
        if analysis['rsi_level'] == '超买':
            print("   ⚠️  RSI显示超买，考虑减仓或观望")
        elif analysis['rsi_level'] == '超卖':
            print("   💡  RSI显示超卖，可能有机会")
        
        if analysis['sma_trend'] == '金叉':
            print("   📈  短期均线上穿长期均线，可能上涨")
        elif analysis['sma_trend'] == '死叉':
            print("   📉  短期均线下穿长期均线，可能下跌")
            
        print(f"\n⏰ 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
    
    def plot_chart(self, symbol, df):
        """绘制图表"""
        try:
            plt.figure(figsize=(12, 8))
            
            # 价格和移动平均线
            plt.subplot(2, 1, 1)
            plt.plot(df.index, df['Close'], label='收盘价', linewidth=2)
            plt.plot(df.index, df['SMA_10'], label='10日MA', linestyle='--')
            plt.plot(df.index, df['SMA_30'], label='30日MA', linestyle='--')
            plt.title(f'{symbol} 价格走势')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # RSI
            plt.subplot(2, 1, 2)
            plt.plot(df.index, df['RSI'], label='RSI', color='orange', linewidth=2)
            plt.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='超买线')
            plt.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='超卖线')
            plt.title('RSI指标')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # 保存图表
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_analysis_{timestamp}.png"
            plt.savefig(filename, dpi=100)
            print(f"📊 图表已保存: {filename}")
            plt.close()
            
        except Exception as e:
            print(f"❌ 绘制图表失败: {e}")

def main():
    """主函数"""
    analyzer = QuickStockAnalyzer()
    
    # 示例股票代码
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    
    print("📋 可用股票代码示例:")
    for i, stock in enumerate(stocks, 1):
        print(f"   {i}. {stock}")
    
    print("\n💡 提示: 可以输入其他股票代码，如 'BABA' (阿里巴巴), 'JD' (京东)")
    
    while True:
        symbol = input("\n请输入股票代码 (或输入 'quit' 退出): ").strip().upper()
        
        if symbol.lower() == 'quit':
            print("👋 退出程序")
            break
            
        if not symbol:
            print("⚠️  请输入有效的股票代码")
            continue
        
        # 获取数据
        df = analyzer.get_stock_data(symbol, period="3mo")
        if df is None or df.empty:
            print(f"❌ 无法获取 {symbol} 的数据，请检查股票代码")
            continue
        
        # 计算指标
        df = analyzer.calculate_indicators(df)
        
        # 分析趋势
        analysis = analyzer.analyze_trend(df)
        
        # 生成报告
        analyzer.generate_report(symbol, df, analysis)
        
        # 绘制图表
        analyzer.plot_chart(symbol, df)
        
        print(f"\n✅ {symbol} 分析完成！")

if __name__ == "__main__":
    main()