#!/usr/bin/env python3
"""
超简单股票测试 - 确保能正常工作
"""

from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """首页"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>股票测试 - 极简版</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .box { border: 1px solid #ccc; padding: 20px; margin: 10px 0; }
            .success { background: #dfd; }
            .error { background: #fdd; }
            button { padding: 10px; margin: 5px; }
            input { padding: 10px; width: 200px; }
        </style>
    </head>
    <body>
        <h1>📈 股票测试 - 极简版</h1>
        
        <div class="box">
            <h3>测试连接</h3>
            <button onclick="testConnection()">测试服务器连接</button>
            <div id="connection"></div>
        </div>
        
        <div class="box">
            <h3>分析股票</h3>
            <input type="text" id="symbol" value="AAPL" placeholder="股票代码">
            <button onclick="analyze()">分析</button>
            <div id="result"></div>
        </div>
        
        <div class="box">
            <h3>直接API测试</h3>
            <button onclick="testAPI()">测试 /api/test</button>
            <div id="api"></div>
        </div>
        
        <script>
            async function testConnection() {
                const div = document.getElementById('connection');
                div.innerHTML = '测试中...';
                
                try {
                    const response = await fetch('/');
                    if (response.ok) {
                        div.innerHTML = '<div class="success">✅ 服务器连接正常</div>';
                    } else {
                        div.innerHTML = '<div class="error">❌ 连接失败: ' + response.status + '</div>';
                    }
                } catch (e) {
                    div.innerHTML = '<div class="error">❌ 连接异常: ' + e.message + '</div>';
                }
            }
            
            async function analyze() {
                const symbol = document.getElementById('symbol').value.trim().toUpperCase();
                const div = document.getElementById('result');
                
                if (!symbol) {
                    div.innerHTML = '<div class="error">❌ 请输入股票代码</div>';
                    return;
                }
                
                div.innerHTML = '分析中...';
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({symbol: symbol})
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        div.innerHTML = `
                            <div class="success">
                                <h4>✅ ${symbol} 分析结果</h4>
                                <p>价格: $${data.price.toFixed(2)}</p>
                                <p>变化: ${data.change > 0 ? '+' : ''}${data.change.toFixed(2)}%</p>
                                <p>趋势: ${data.trend}</p>
                                <p>时间: ${data.time}</p>
                            </div>
                        `;
                    } else {
                        div.innerHTML = '<div class="error">❌ 分析失败: ' + (data.error || '未知错误') + '</div>';
                    }
                } catch (e) {
                    div.innerHTML = '<div class="error">❌ 请求异常: ' + e.message + '</div>';
                }
            }
            
            async function testAPI() {
                const div = document.getElementById('api');
                div.innerHTML = '测试中...';
                
                try {
                    const response = await fetch('/api/test');
                    const data = await response.json();
                    
                    if (response.ok) {
                        div.innerHTML = `
                            <div class="success">
                                ✅ API测试成功<br>
                                消息: ${data.message}<br>
                                状态: ${data.status}
                            </div>
                        `;
                    } else {
                        div.innerHTML = '<div class="error">❌ API测试失败: ' + response.status + '</div>';
                    }
                } catch (e) {
                    div.innerHTML = '<div class="error">❌ API测试异常: ' + e.message + '</div>';
                }
            }
            
            // 页面加载时自动测试连接
            window.onload = testConnection;
        </script>
    </body>
    </html>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    """分析股票"""
    try:
        data = request.json
        symbol = data.get('symbol', 'AAPL').upper()
        
        # 生成模拟数据
        price = 100 + random.uniform(-20, 50)
        change = random.uniform(-5, 5)
        
        return jsonify({
            'symbol': symbol,
            'price': round(price, 2),
            'change': round(change, 2),
            'trend': '上涨' if change > 0 else '下跌',
            'time': datetime.now().strftime('%H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def api_test():
    """测试API"""
    return jsonify({
        'message': 'API工作正常',
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 极简股票测试启动...")
    print("🌐 访问: http://localhost:7777")
    print("💡 这个版本绝对能工作！")
    
    app.run(host='0.0.0.0', port=7777, debug=False, use_reloader=False)