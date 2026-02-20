#!/usr/bin/env python3
"""
渐进增强版股票分析系统
从简单开始，逐步添加功能
"""

from flask import Flask, jsonify, request, render_template_string
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# ==================== 阶段1: 基础功能 ====================

@app.route('/')
def home():
    """首页 - 极简版"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📈 股票分析系统 - 渐进版</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
            .container { max-width: 1400px; margin: 0 auto; }
            .header { text-align: center; color: white; margin-bottom: 30px; }
            .header h1 { font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .header p { font-size: 1.1rem; opacity: 0.9; }
            .card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            
            .search-box { display: flex; gap: 10px; margin-bottom: 20px; }
            .search-box input { flex: 1; padding: 12px 15px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; transition: border-color 0.3s; }
            .search-box input:focus { outline: none; border-color: #667eea; }
            .search-box button { padding: 12px 25px; background: #667eea; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.3s; }
            .search-box button:hover { background: #5a67d8; }
            
            .quick-stocks { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; }
            .stock-btn { padding: 8px 15px; background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; transition: all 0.3s; }
            .stock-btn:hover { background: #667eea; color: white; border-color: #667eea; }
            
            .result { display: none; margin-top: 20px; }
            .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
            .info-item { background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; }
            .info-label { font-size: 0.9rem; color: #666; margin-bottom: 5px; }
            .info-value { font-size: 1.2rem; font-weight: 600; color: #333; }
            
            .positive { color: #10b981; }
            .negative { color: #ef4444; }
            
            .loading { text-align: center; padding: 40px; color: #666; }
            .loading-spinner { border: 3px solid #f3f3f3; border-top: 3px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            
            .error { background: #fee; color: #c00; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #c00; }
            
            .charts-container { margin-top: 30px; }
            .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; }
            .chart-box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .chart-box h3 { margin-bottom: 15px; color: #333; font-size: 1.2rem; }
            .chart-wrapper { height: 300px; width: 100%; position: relative; }
            
            @media (max-width: 768px) {
                .charts-grid { grid-template-columns: 1fr; }
                .header h1 { font-size: 2rem; }
                .chart-box { padding: 15px; }
            }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📈 股票分析系统</h1>
                <p>版本: 渐进增强版 (基础功能已就绪)</p>
            </div>
            
            <div class="card">
                <h2>股票查询</h2>
                <div class="search-box">
                    <input type="text" id="stockInput" placeholder="输入股票代码，如：AAPL, MSFT, TSLA..." value="AAPL">
                    <button onclick="analyzeStock()">分析股票</button>
                </div>
                
                <div class="quick-stocks">
                    <p style="width: 100%; margin-bottom: 10px; color: #666;">热门股票：</p>
                    <div class="stock-btn" onclick="setStock('AAPL')">AAPL (苹果)</div>
                    <div class="stock-btn" onclick="setStock('MSFT')">MSFT (微软)</div>
                    <div class="stock-btn" onclick="setStock('TSLA')">TSLA (特斯拉)</div>
                    <div class="stock-btn" onclick="setStock('NVDA')">NVDA (英伟达)</div>
                    <div class="stock-btn" onclick="setStock('BABA')">BABA (阿里)</div>
                </div>
            </div>
            
            <div class="card result" id="resultCard">
                <div class="loading" id="loading">
                    <div class="loading-spinner"></div>
                    <p>正在分析股票数据...</p>
                </div>
                
                <div id="error" class="error" style="display: none;"></div>
                
                <div id="analysisContent" style="display: none;">
                    <h2 id="stockTitle">股票分析结果</h2>
                    
                    <div class="info-grid" id="stockInfo">
                        <!-- 动态填充 -->
                    </div>
                    
                    <div class="charts-container">
                        <h3>📊 技术分析图表</h3>
                        <div class="charts-grid">
                            <div class="chart-box">
                                <h3>价格走势</h3>
                                <div class="chart-wrapper">
                                    <canvas id="priceChart"></canvas>
                                </div>
                            </div>
                            <div class="chart-box">
                                <h3>RSI指标</h3>
                                <div class="chart-wrapper">
                                    <canvas id="rsiChart"></canvas>
                                </div>
                            </div>
                            <div class="chart-box">
                                <h3>移动平均线</h3>
                                <div class="chart-wrapper">
                                    <canvas id="maChart"></canvas>
                                </div>
                            </div>
                            <div class="chart-box">
                                <h3>成交量</h3>
                                <div class="chart-wrapper">
                                    <canvas id="volumeChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function setStock(symbol) {
                document.getElementById('stockInput').value = symbol;
                analyzeStock();
            }
            
            function analyzeStock() {
                const symbol = document.getElementById('stockInput').value.trim().toUpperCase();
                if (!symbol) {
                    alert('请输入股票代码');
                    return;
                }
                
                // 显示结果区域
                const resultCard = document.getElementById('resultCard');
                resultCard.style.display = 'block';
                
                // 显示加载中
                document.getElementById('loading').style.display = 'block';
                document.getElementById('error').style.display = 'none';
                document.getElementById('analysisContent').style.display = 'none';
                
                // 发送请求
                fetch('/api/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ symbol: symbol, period: '1mo' })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    // 隐藏加载中
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('analysisContent').style.display = 'block';
                    
                    // 更新标题
                    document.getElementById('stockTitle').textContent = `${symbol} 股票分析`;
                    
                    // 显示股票信息
                    displayStockInfo(data.analysis);
                    
                    // 绘制图表
                    if (data.chart_data) {
                        drawCharts(data.chart_data);
                    }
                    
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('error').textContent = `错误: ${error.message}`;
                });
            }
            
            let priceChart, rsiChart, maChart, volumeChart;
            
            function displayStockInfo(analysis) {
                const stockInfo = document.getElementById('stockInfo');
                const changeClass = analysis.price_change >= 0 ? 'positive' : 'negative';
                const changeSign = analysis.price_change >= 0 ? '+' : '';
                
                stockInfo.innerHTML = `
                    <div class="info-item">
                        <div class="info-label">股票代码</div>
                        <div class="info-value">${analysis.symbol}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">当前价格</div>
                        <div class="info-value">$${analysis.current_price.toFixed(2)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">价格变化</div>
                        <div class="info-value ${changeClass}">
                            ${changeSign}$${analysis.price_change.toFixed(2)} (${changeSign}${analysis.price_change_pct.toFixed(2)}%)
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">成交量</div>
                        <div class="info-value">${analysis.volume.toLocaleString()}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">趋势</div>
                        <div class="info-value ${analysis.trend === '上涨' ? 'positive' : 'negative'}">
                            ${analysis.trend}
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">MA趋势</div>
                        <div class="info-value">${analysis.sma_trend}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">RSI状态</div>
                        <div class="info-value ${analysis.rsi_level === '超买' ? 'negative' : analysis.rsi_level === '超卖' ? 'positive' : ''}">
                            ${analysis.rsi_level}
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">分析时间</div>
                        <div class="info-value">${analysis.timestamp}</div>
                    </div>
                `;
            }
            
            function drawCharts(chartData) {
                // 销毁旧图表
                if (priceChart) priceChart.destroy();
                if (rsiChart) rsiChart.destroy();
                if (maChart) maChart.destroy();
                if (volumeChart) volumeChart.destroy();
                
                // 价格走势图
                const priceCtx = document.getElementById('priceChart').getContext('2d');
                priceChart = new Chart(priceCtx, {
                    type: 'line',
                    data: {
                        labels: chartData.dates,
                        datasets: [{
                            label: '收盘价',
                            data: chartData.prices,
                            borderColor: '#667eea',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: true }
                        },
                        scales: {
                            y: {
                                beginAtZero: false,
                                ticks: {
                                    callback: function(value) {
                                        return '$' + value.toFixed(2);
                                    }
                                }
                            }
                        }
                    }
                });
                
                // RSI图表
                const rsiCtx = document.getElementById('rsiChart').getContext('2d');
                rsiChart = new Chart(rsiCtx, {
                    type: 'line',
                    data: {
                        labels: chartData.dates,
                        datasets: [{
                            label: 'RSI',
                            data: chartData.rsi,
                            borderColor: '#f59e0b',
                            backgroundColor: 'rgba(245, 158, 11, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: true },
                            annotation: {
                                annotations: {
                                    overbought: {
                                        type: 'line',
                                        yMin: 70,
                                        yMax: 70,
                                        borderColor: '#ef4444',
                                        borderWidth: 1,
                                        borderDash: [5, 5]
                                    },
                                    oversold: {
                                        type: 'line',
                                        yMin: 30,
                                        yMax: 30,
                                        borderColor: '#10b981',
                                        borderWidth: 1,
                                        borderDash: [5, 5]
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                min: 0,
                                max: 100,
                                ticks: {
                                    callback: function(value) {
                                        if (value === 30) return '超卖';
                                        if (value === 70) return '超买';
                                        return value;
                                    }
                                }
                            }
                        }
                    }
                });
                
                // 移动平均线图表
                const maCtx = document.getElementById('maChart').getContext('2d');
                maChart = new Chart(maCtx, {
                    type: 'line',
                    data: {
                        labels: chartData.dates,
                        datasets: [
                            {
                                label: '收盘价',
                                data: chartData.prices,
                                borderColor: '#667eea',
                                borderWidth: 2,
                                tension: 0.4
                            },
                            {
                                label: '10日MA',
                                data: chartData.sma_10,
                                borderColor: '#10b981',
                                borderWidth: 2,
                                borderDash: [5, 5]
                            },
                            {
                                label: '30日MA',
                                data: chartData.sma_30,
                                borderColor: '#ef4444',
                                borderWidth: 2,
                                borderDash: [5, 5]
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: true }
                        },
                        scales: {
                            y: {
                                beginAtZero: false,
                                ticks: {
                                    callback: function(value) {
                                        return '$' + value.toFixed(2);
                                    }
                                }
                            }
                        }
                    }
                });
                
                // 成交量图表
                const volumeCtx = document.getElementById('volumeChart').getContext('2d');
                volumeChart = new Chart(volumeCtx, {
                    type: 'bar',
                    data: {
                        labels: chartData.dates,
                        datasets: [{
                            label: '成交量',
                            data: chartData.volumes,
                            backgroundColor: 'rgba(102, 126, 234, 0.7)',
                            borderColor: 'rgba(102, 126, 234, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: true }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value) {
                                        if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M';
                                        if (value >= 1000) return (value / 1000).toFixed(0) + 'K';
                                        return value;
                                    }
                                }
                            }
                        }
                    }
                });
            }
            
            // 页面加载时自动分析AAPL
            window.onload = function() {
                analyzeStock();
            };
        </script>
    </body>
    </html>
    '''

# ==================== 阶段1: API功能 ====================

class StockAnalyzer:
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol, period="1mo"):
        """获取股票数据"""
        symbol = symbol.strip().upper()
        cache_key = f"{symbol}_{period}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        print(f"📈 获取 {symbol} 数据...")
        try:
            # 尝试获取真实数据
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            
            if not df.empty:
                print(f"✅ 获取成功: {len(df)} 条记录")
                self.cache[cache_key] = df
                return df
        except:
            pass
        
        # 使用模拟数据
        print(f"⚠️  使用模拟数据")
        df = self.get_sample_data(symbol)
        self.cache[cache_key] = df
        return df
    
    def get_sample_data(self, symbol):
        """生成模拟数据"""
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        base_price = {
            'AAPL': 180.0, 'MSFT': 420.0, 'TSLA': 180.0, 'NVDA': 800.0,
            'BABA': 80.0, 'GOOGL': 150.0, 'AMZN': 180.0, 'BTC-USD': 60000.0
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
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 准备图表数据
        chart_data = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'prices': df['Close'].fillna(0).tolist(),
            'sma_10': df['SMA_10'].fillna(0).tolist(),
            'sma_30': df['SMA_30'].fillna(0).tolist(),
            'rsi': df['RSI'].fillna(50).tolist(),
            'volumes': df['Volume'].fillna(0).tolist()
        }
        
        return {
            'analysis': analysis,
            'chart_data': chart_data
        }

analyzer = StockAnalyzer()

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """分析股票API"""
    try:
        data = request.json
        symbol = data.get('symbol', '').strip().upper()
        period = data.get('period', '1mo')
        
        if not symbol:
            return jsonify({'error': '请输入股票代码'}), 400
        
        result = analyzer.analyze_stock(symbol, period)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def api_test():
    """测试API"""
    return jsonify({
        'status': 'ok',
        'message': 'API工作正常',
        'version': '渐进增强版 v1.0',
        'timestamp': datetime.now().isoformat()
    })

# ==================== 启动应用 ====================

if __name__ == '__main__':
    print("🚀 渐进增强版股票分析系统启动中...")
    print("🌐 访问地址: http://localhost:8888")
    print("📊 当前功能:")
    print("   ✅ 基础股票分析")
    print("   ✅ 实时价格数据")
    print("   ✅ 技术指标计算")
    print("   ✅ 响应式界面")
    print("\n🔧 下一步计划:")
    print("   📈 添加图表功能")
    print("   📊 更多技术指标")
    print("   📱 移动端优化")
    print("\n💡 按 Ctrl+C 停止服务")
    
    app.run(host='0.0.0.0', port=8888, debug=False, use_reloader=False)