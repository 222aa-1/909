#!/usr/bin/env python3
"""
简单测试应用 - 排除复杂JavaScript问题
"""

from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# 读取简单测试HTML
with open('simple_test.html', 'r', encoding='utf-8') as f:
    SIMPLE_HTML = f.read()

@app.route('/test')
def test_page():
    """简单测试页面"""
    return render_template_string(SIMPLE_HTML)

@app.route('/api/simple_analyze', methods=['POST'])
def simple_analyze():
    """简化版分析API"""
    try:
        data = request.json
        symbol = data.get('symbol', '').strip().upper()
        
        if not symbol:
            return jsonify({'error': '请输入股票代码'}), 400
        
        # 生成模拟数据
        np.random.seed(hash(symbol) % 10000)
        
        analysis = {
            'symbol': symbol,
            'current_price': round(100 + np.random.uniform(-20, 50), 2),
            'price_change': round(np.random.uniform(-5, 5), 2),
            'price_change_pct': round(np.random.uniform(-3, 3), 2),
            'volume': np.random.randint(1000000, 50000000),
            'trend': '上涨' if np.random.random() > 0.5 else '下跌',
            'sma_trend': '金叉' if np.random.random() > 0.5 else '死叉',
            'rsi_level': np.random.choice(['超买', '正常', '超卖']),
            'macd_signal': '买入' if np.random.random() > 0.5 else '卖出',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 计算价格变化百分比
        analysis['price_change_pct'] = round((analysis['price_change'] / 
                                            (analysis['current_price'] - analysis['price_change'])) * 100, 2)
        
        return jsonify({'analysis': analysis})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/simple_stocks')
def simple_stocks():
    """简化版股票列表"""
    stocks = [
        {'symbol': 'AAPL', 'name': '苹果'},
        {'symbol': 'MSFT', 'name': '微软'},
        {'symbol': 'TSLA', 'name': '特斯拉'},
        {'symbol': 'NVDA', 'name': '英伟达'},
        {'symbol': 'BABA', 'name': '阿里巴巴'},
        {'symbol': 'JD', 'name': '京东'}
    ]
    return jsonify({'stocks': stocks})

if __name__ == '__main__':
    print("🚀 简单测试应用启动中...")
    print("🌐 测试页面: http://localhost:9999/test")
    print("💡 这个版本排除了复杂JavaScript问题")
    
    app.run(host='0.0.0.0', port=9999, debug=False)