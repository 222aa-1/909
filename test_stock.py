import subprocess
import sys

# 安装yfinance如果不存在
try:
    import yfinance
    print('✅ yfinance已安装')
except ImportError:
    print('📦 安装yfinance...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance'])
    print('✅ yfinance安装完成')

# 测试基本功能
print('\n🧪 测试股票数据获取...')
import yfinance as yf
import pandas as pd

# 测试获取苹果股票数据
try:
    aapl = yf.Ticker('AAPL')
    hist = aapl.history(period='5d')
    print(f'✅ 成功获取AAPL数据: {len(hist)} 条记录')
    print(f'   最新收盘价: ${hist["Close"].iloc[-1]:.2f}')
    print(f'   时间范围: {hist.index[0].date()} 到 {hist.index[-1].date()}')
    
    # 显示前几行数据
    print('\n📊 数据预览:')
    print(hist[['Open', 'High', 'Low', 'Close', 'Volume']].head())
    
except Exception as e:
    print(f'❌ 测试失败: {e}')