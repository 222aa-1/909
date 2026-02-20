#!/usr/bin/env python3
"""
金融分析模块 - 可复用组件
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockAnalyzer:
    """股票分析器类"""
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.analysis_results = {}
        
    def fetch_data(self, start_date="2024-01-01", end_date=None):
        """获取股票数据"""
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
            
        print(f"获取数据: {self.symbol} ({start_date} 到 {end_date})")
        
        try:
            df = ak.stock_zh_a_hist(
                symbol=self.symbol,
                period="daily",
                start_date=start_date.replace("-", ""),
                end_date=end_date.replace("-", ""),
                adjust=""
            )
            
            if df.empty:
                print("数据获取失败")
                return False
            
            # 数据预处理
            df['日期'] = pd.to_datetime(df['日期'])
            df.set_index('日期', inplace=True)
            df.sort_index(inplace=True)
            
            # 计算收益率
            df['Returns'] = df['收盘'].pct_change()
            df['Log_Returns'] = np.log(df['收盘'] / df['收盘'].shift(1))
            
            self.data = df
            print(f"✓ 获取到 {len(df)} 个交易日数据")
            return True
            
        except Exception as e:
            print(f"数据获取错误: {e}")
            return False
    
    def calculate_technical_indicators(self):
        """计算技术指标"""
        if self.data is None:
            print("请先获取数据")
            return
        
        df = self.data
        
        # 移动平均线
        df['MA5'] = df['收盘'].rolling(window=5).mean()
        df['MA10'] = df['收盘'].rolling(window=10).mean()
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
        
        # 成交量指标
        df['Volume_MA20'] = df['成交量'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['成交量'] / df['Volume_MA20']
        
        self.data = df
        print("✓ 技术指标计算完成")
    
    def analyze_trend(self):
        """趋势分析"""
        if self.data is None:
            return {}
        
        df = self.data
        current_price = df['收盘'].iloc[-1]
        
        trend_analysis = {
            'current_price': current_price,
            'trend_short': '上涨' if current_price > df['MA5'].iloc[-1] else '下跌',
            'trend_medium': '上涨' if current_price > df['MA20'].iloc[-1] else '下跌',
            'trend_long': '上涨' if current_price > df['MA60'].iloc[-1] else '下跌',
            'ma_alignment': self._check_ma_alignment(df),
            'rsi_status': self._get_rsi_status(df['RSI'].iloc[-1]),
            'macd_signal': '金叉' if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] else '死叉',
        }
        
        self.analysis_results['trend'] = trend_analysis
        return trend_analysis
    
    def analyze_volatility(self):
        """波动性分析"""
        if self.data is None:
            return {}
        
        df = self.data
        
        # 计算不同时间段的波动率
        volatility_analysis = {
            'volatility_20d': df['Returns'].tail(20).std() * np.sqrt(252) * 100,
            'volatility_60d': df['Returns'].tail(60).std() * np.sqrt(252) * 100,
            'volatility_120d': df['Returns'].tail(120).std() * np.sqrt(252) * 100,
            'max_drawdown': self._calculate_max_drawdown(df['收盘']),
            'sharpe_ratio': self._calculate_sharpe_ratio(df['Returns']),
        }
        
        self.analysis_results['volatility'] = volatility_analysis
        return volatility_analysis
    
    def analyze_support_resistance(self, lookback_days=50):
        """支撑阻力分析"""
        if self.data is None:
            return {}
        
        df = self.data
        recent_data = df.tail(lookback_days)
        
        support_resistance = {
            'support_level': recent_data['收盘'].min(),
            'resistance_level': recent_data['收盘'].max(),
            'current_to_support': ((df['收盘'].iloc[-1] / recent_data['收盘'].min()) - 1) * 100,
            'current_to_resistance': ((recent_data['收盘'].max() / df['收盘'].iloc[-1]) - 1) * 100,
            'bb_position': self._get_bb_position(df),
        }
        
        self.analysis_results['support_resistance'] = support_resistance
        return support_resistance
    
    def analyze_seasonality(self, year=2025):
        """季节性分析"""
        if self.data is None:
            return {}
        
        df = self.data
        
        # 假设春节日期
        spring_festival = pd.Timestamp(f'{year}-02-10')
        analysis_period = {
            'pre_festival': spring_festival - pd.Timedelta(days=30),
            'post_festival': spring_festival + pd.Timedelta(days=90),
        }
        
        mask = (df.index >= analysis_period['pre_festival']) & (df.index <= analysis_period['post_festival'])
        seasonal_data = df[mask]
        
        if len(seasonal_data) > 10:
            seasonality = {
                'period_return': ((seasonal_data['收盘'].iloc[-1] / seasonal_data['收盘'].iloc[0]) - 1) * 100,
                'avg_daily_return': seasonal_data['Returns'].mean() * 100,
                'positive_days': (seasonal_data['Returns'] > 0).sum(),
                'total_days': len(seasonal_data),
            }
        else:
            seasonality = {'error': '数据不足'}
        
        self.analysis_results['seasonality'] = seasonality
        return seasonality
    
    def generate_report(self):
        """生成分析报告"""
        if not self.analysis_results:
            print("请先进行分析")
            return
        
        report = {
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data_period': f"{self.data.index.min().date()} 到 {self.data.index.max().date()}",
            'total_days': len(self.data),
            'analysis_results': self.analysis_results
        }
        
        return report
    
    def _check_ma_alignment(self, df):
        """检查移动平均线排列"""
        ma5 = df['MA5'].iloc[-1]
        ma20 = df['MA20'].iloc[-1]
        ma60 = df['MA60'].iloc[-1]
        
        if ma5 > ma20 > ma60:
            return "多头排列"
        elif ma5 < ma20 < ma60:
            return "空头排列"
        else:
            return "震荡排列"
    
    def _get_rsi_status(self, rsi):
        """获取RSI状态"""
        if rsi > 70:
            return "超买"
        elif rsi < 30:
            return "超卖"
        else:
            return "中性"
    
    def _calculate_max_drawdown(self, prices):
        """计算最大回撤"""
        cumulative = prices / prices.cummax()
        max_drawdown = (1 - cumulative.min()) * 100
        return max_drawdown
    
    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """计算夏普比率"""
        excess_returns = returns - risk_free_rate / 252
        sharpe = np.sqrt(252) * excess_returns.mean() / returns.std()
        return sharpe
    
    def _get_bb_position(self, df):
        """获取布林带位置"""
        price = df['收盘'].iloc[-1]
        bb_upper = df['BB_upper'].iloc[-1]
        bb_lower = df['BB_lower'].iloc[-1]
        
        if price > bb_upper:
            return "上轨上方"
        elif price < bb_lower:
            return "下轨下方"
        else:
            bb_width = (bb_upper - bb_lower) / df['BB_middle'].iloc[-1]
            position = (price - bb_lower) / (bb_upper - bb_lower)
            
            if position > 0.7:
                return "上轨附近"
            elif position < 0.3:
                return "下轨附近"
            else:
                return "中轨附近"

# 使用示例
if __name__ == "__main__":
    # 创建分析器
    analyzer = StockAnalyzer("300809")
    
    # 获取数据
    if analyzer.fetch_data(start_date="2024-01-01"):
        # 计算技术指标
        analyzer.calculate_technical_indicators()
        
        # 进行分析
        analyzer.analyze_trend()
        analyzer.analyze_volatility()
        analyzer.analyze_support_resistance()
        analyzer.analyze_seasonality(year=2024)
        
        # 生成报告
        report = analyzer.generate_report()
        
        print("\n" + "="*60)
        print("分析完成!")
        print(f"股票: {report['symbol']}")
        print(f"数据期间: {report['data_period']}")
        print(f"分析时间: {report['analysis_date']}")
        print("="*60)