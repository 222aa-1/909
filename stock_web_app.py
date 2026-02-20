#!/usr/bin/env python3
"""
股票分析Web应用
基于Flask的Web界面，提供股票分析功能
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import json
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

class StockAnalyzer:
    """股票分析器核心类"""
    
    def __init__(self):
        self.cache = {}
        
    def get_stock_data(self, symbol, period="1mo", use_cache=True):
        """获取股票数据"""
        # 清理股票代码，移除特殊字符
        symbol = symbol.strip().upper()
        cache_key = f"{symbol}_{period}"
        
        if use_cache and cache_key in self.cache:
            print(f"📦 使用缓存数据: {symbol}")
            return self.cache[cache_key]
        
        print(f"📈 获取 {symbol} 股票数据 ({period})...")
        try:
            import time
            time.sleep(0.5)  # 避免频率限制
            
            # 验证股票代码格式（简单验证）
            if not symbol or len(symbol) > 10:
                raise ValueError(f"无效的股票代码: {symbol}")
            
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            
            if df.empty:
                print(f"⚠️  未找到实时数据，使用示例数据")
                df = self.get_sample_data(symbol)
            else:
                print(f"✅ 获取成功: {len(df)} 条记录")
            
            # 缓存数据
            self.cache[cache_key] = df
            return df
            
        except Exception as e:
            print(f"⚠️  获取实时数据失败: {e}")
            print("   使用示例数据...")
            df = self.get_sample_data(symbol)
            self.cache[cache_key] = df
            return df
    
    def get_sample_data(self, symbol):
        """生成示例数据"""
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        # 基础价格
        base_price = {
            'AAPL': 180.0, 'MSFT': 420.0, 'GOOGL': 150.0, 'TSLA': 180.0,
            'BABA': 80.0, 'JD': 30.0, 'NVDA': 800.0, 'AMZN': 180.0,
            'BTC-USD': 60000.0, 'ETH-USD': 3000.0, '^GSPC': 5000.0
        }.get(symbol, 100.0)
        
        np.random.seed(hash(symbol) % 10000)
        returns = np.random.normal(0.001, 0.02, 30)
        
        prices = [base_price]
        for r in returns:
            prices.append(prices[-1] * (1 + r))
        prices = prices[1:]
        
        df = pd.DataFrame({
            'Open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
            'High': [p * (1 + np.random.uniform(0, 0.03)) for p in prices],
            'Low': [p * (1 - np.random.uniform(0, 0.03)) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000000, 50000000, 30)
        }, index=dates)
        
        return df
    
    def calculate_indicators(self, df):
        """计算技术指标"""
        # 移动平均线
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_30'] = df['Close'].rolling(window=30).mean()
        
        # RSI
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
        
        # MACD (简化版)
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        return df
    
    def analyze_stock(self, symbol, period="1mo"):
        """分析股票"""
        df = self.get_stock_data(symbol, period)
        df = self.calculate_indicators(df)
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        analysis = {
            'symbol': symbol,
            'current_price': float(latest['Close']),
            'price_change': float(latest['Close'] - prev['Close']),
            'price_change_pct': float(((latest['Close'] - prev['Close']) / prev['Close']) * 100),
            'volume': int(latest['Volume']),
            'trend': '上涨' if latest['Close'] > prev['Close'] else '下跌',
            'sma_trend': '金叉' if latest['SMA_10'] > latest['SMA_30'] else '死叉',
            'rsi_level': '超买' if latest['RSI'] > 70 else '超卖' if latest['RSI'] < 30 else '正常',
            'bb_position': '上轨' if latest['Close'] > latest['BB_upper'] else '下轨' if latest['Close'] < latest['BB_lower'] else '中轨',
            'macd_signal': '买入' if latest['MACD'] > latest['MACD_signal'] else '卖出',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 准备图表数据
        chart_data = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'prices': df['Close'].tolist(),
            'sma_10': df['SMA_10'].tolist(),
            'sma_30': df['SMA_30'].tolist(),
            'rsi': df['RSI'].tolist(),
            'bb_upper': df['BB_upper'].tolist(),
            'bb_lower': df['BB_lower'].tolist(),
            'macd': df['MACD'].tolist(),
            'macd_signal': df['MACD_signal'].tolist()
        }
        
        return {
            'analysis': analysis,
            'chart_data': chart_data,
            'raw_data': df.tail(10).to_dict('records')  # 最近10条数据
        }

# 创建分析器实例
analyzer = StockAnalyzer()

# 预定义股票列表
POPULAR_STOCKS = [
    {'symbol': 'AAPL', 'name': '苹果'},
    {'symbol': 'MSFT', 'name': '微软'},
    {'symbol': 'GOOGL', 'name': '谷歌'},
    {'symbol': 'TSLA', 'name': '特斯拉'},
    {'symbol': 'NVDA', 'name': '英伟达'},
    {'symbol': 'AMZN', 'name': '亚马逊'},
    {'symbol': 'BABA', 'name': '阿里巴巴'},
    {'symbol': 'JD', 'name': '京东'},
    {'symbol': '^GSPC', 'name': '标普500'},
    {'symbol': 'BTC-USD', 'name': '比特币'}
]

@app.route('/')
def index():
    """首页"""
    return render_template('index.html', stocks=POPULAR_STOCKS)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """分析股票API"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
            
        symbol = data.get('symbol', '').strip().upper()
        period = data.get('period', '1mo')
        
        if not symbol:
            return jsonify({'error': '请输入股票代码'}), 400
        
        # 简单验证股票代码
        if len(symbol) > 20 or not any(c.isalnum() for c in symbol):
            return jsonify({'error': f'无效的股票代码格式: {symbol}'}), 400
        
        result = analyzer.analyze_stock(symbol, period)
        return jsonify(result)
        
    except Exception as e:
        error_msg = str(e)
        # 提供更友好的错误信息
        if 'pattern' in error_msg.lower():
            error_msg = f'股票代码格式错误: {symbol}，请使用如 AAPL、MSFT 等格式'
        return jsonify({'error': error_msg}), 500

@app.route('/api/stocks')
def api_stocks():
    """获取股票列表API"""
    return jsonify({'stocks': POPULAR_STOCKS})

@app.route('/api/batch_analyze', methods=['POST'])
def api_batch_analyze():
    """批量分析API"""
    try:
        data = request.json
        symbols = data.get('symbols', [])
        
        if not symbols:
            symbols = ['AAPL', 'MSFT', 'GOOGL']
        
        results = []
        for symbol in symbols[:5]:  # 最多分析5个
            try:
                result = analyzer.analyze_stock(symbol.strip().upper())
                results.append(result['analysis'])
            except Exception as e:
                results.append({
                    'symbol': symbol,
                    'error': str(e)
                })
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trending')
def api_trending():
    """热门股票分析"""
    symbols = ['AAPL', 'MSFT', 'TSLA', 'NVDA']
    results = []
    
    for symbol in symbols:
        try:
            result = analyzer.analyze_stock(symbol)
            results.append(result['analysis'])
        except:
            pass
    
    return jsonify({'trending': results})

# 创建必要的目录
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

if __name__ == '__main__':
    print("🚀 股票分析Web应用启动中...")
    print("🌐 访问地址: http://localhost:9988")
    print("📊 功能:")
    print("   - 单个股票分析")
    print("   - 批量股票分析")
    print("   - 技术指标图表")
    print("   - 实时数据更新")
    print("\n💡 按 Ctrl+C 停止服务")
    
    app.run(host='0.0.0.0', port=9988, debug=True)