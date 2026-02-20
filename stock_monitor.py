#!/usr/bin/env python3
"""
股票监控系统 - 定期分析和预警
"""

import json
import schedule
import time
from datetime import datetime
from financial_analyzer import StockAnalyzer
import pandas as pd

class StockMonitor:
    """股票监控器"""
    
    def __init__(self, config_file="monitor_config.json"):
        self.config_file = config_file
        self.stocks = self.load_config()
        self.analysis_history = {}
        
    def load_config(self):
        """加载监控配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('stocks', [])
        except FileNotFoundError:
            # 默认配置
            default_config = {
                'stocks': [
                    {'symbol': '300809', 'name': '华辰装备', 'alert_threshold': 5.0}
                ],
                'analysis_interval': 60,  # 分钟
                'alert_channels': ['console']
            }
            self.save_config(default_config)
            return default_config['stocks']
    
    def save_config(self, config):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def analyze_stock(self, stock_info):
        """分析单只股票"""
        symbol = stock_info['symbol']
        name = stock_info['name']
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 分析 {name}({symbol})...")
        
        analyzer = StockAnalyzer(symbol)
        
        if analyzer.fetch_data(start_date="2024-01-01"):
            analyzer.calculate_technical_indicators()
            
            # 执行分析
            trend = analyzer.analyze_trend()
            volatility = analyzer.analyze_volatility()
            support_resistance = analyzer.analyze_support_resistance()
            
            # 生成报告
            report = analyzer.generate_report()
            
            # 保存分析历史
            if symbol not in self.analysis_history:
                self.analysis_history[symbol] = []
            
            self.analysis_history[symbol].append({
                'timestamp': datetime.now().isoformat(),
                'analysis': report
            })
            
            # 检查是否需要预警
            self.check_alerts(stock_info, report)
            
            return report
        else:
            print(f"  ✗ 数据获取失败")
            return None
    
    def check_alerts(self, stock_info, report):
        """检查预警条件"""
        symbol = stock_info['symbol']
        name = stock_info['name']
        threshold = stock_info.get('alert_threshold', 5.0)
        
        analysis = report['analysis_results']
        
        alerts = []
        
        # 价格变动预警
        if 'trend' in analysis:
            current_price = analysis['trend']['current_price']
            
            # 如果有历史数据，计算变动
            if symbol in self.analysis_history and len(self.analysis_history[symbol]) > 1:
                prev_report = self.analysis_history[symbol][-2]['analysis']
                prev_price = prev_report['analysis_results']['trend']['current_price']
                price_change = ((current_price / prev_price) - 1) * 100
                
                if abs(price_change) >= threshold:
                    alerts.append(f"价格变动 {price_change:.2f}%")
        
        # RSI预警
        if 'trend' in analysis and 'rsi_status' in analysis['trend']:
            rsi_status = analysis['trend']['rsi_status']
            if rsi_status in ['超买', '超卖']:
                alerts.append(f"RSI {rsi_status}")
        
        # 波动率预警
        if 'volatility' in analysis:
            vol_20d = analysis['volatility']['volatility_20d']
            if vol_20d > 50:  # 高波动率
                alerts.append(f"高波动率: {vol_20d:.1f}%")
        
        # 输出预警
        if alerts:
            print(f"  ⚠️ 预警: {', '.join(alerts)}")
    
    def generate_daily_report(self):
        """生成日报"""
        print("\n" + "="*70)
        print(f"股票监控日报 - {datetime.now().strftime('%Y-%m-%d')}")
        print("="*70)
        
        for stock in self.stocks:
            report = self.analyze_stock(stock)
            
            if report:
                analysis = report['analysis_results']
                
                print(f"\n📊 {stock['name']}({stock['symbol']})")
                print(f"   当前价格: {analysis['trend']['current_price']:.2f}")
                print(f"   趋势: {analysis['trend']['trend_short']}/{analysis['trend']['trend_medium']}/{analysis['trend']['trend_long']}")
                print(f"   RSI: {analysis['trend']['rsi_status']}")
                print(f"   波动率: {analysis['volatility']['volatility_20d']:.1f}%")
                
                if 'support_resistance' in analysis:
                    sr = analysis['support_resistance']
                    print(f"   支撑/阻力: {sr['support_level']:.2f} / {sr['resistance_level']:.2f}")
        
        print("\n" + "="*70)
        print("日报生成完成")
        print("="*70)
    
    def run_monitoring(self, interval_minutes=60):
        """运行监控"""
        print(f"启动股票监控系统 (每{interval_minutes}分钟分析一次)")
        print(f"监控股票: {[s['name'] for s in self.stocks]}")
        
        # 立即运行一次
        self.generate_daily_report()
        
        # 设置定时任务
        schedule.every(interval_minutes).minutes.do(self.generate_daily_report)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n监控系统已停止")
    
    def add_stock(self, symbol, name, alert_threshold=5.0):
        """添加监控股票"""
        new_stock = {
            'symbol': symbol,
            'name': name,
            'alert_threshold': alert_threshold
        }
        
        # 检查是否已存在
        for stock in self.stocks:
            if stock['symbol'] == symbol:
                print(f"股票 {name}({symbol}) 已在监控列表中")
                return False
        
        self.stocks.append(new_stock)
        
        # 更新配置文件
        config = self.load_config()
        if isinstance(config, list):
            config = {'stocks': config}
        config['stocks'] = self.stocks
        self.save_config(config)
        
        print(f"✓ 已添加 {name}({symbol}) 到监控列表")
        return True

# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='股票监控系统')
    parser.add_argument('--run', action='store_true', help='运行监控')
    parser.add_argument('--report', action='store_true', help='生成日报')
    parser.add_argument('--add', nargs=2, metavar=('SYMBOL', 'NAME'), help='添加股票')
    parser.add_argument('--interval', type=int, default=60, help='分析间隔(分钟)')
    
    args = parser.parse_args()
    
    monitor = StockMonitor()
    
    if args.add:
        symbol, name = args.add
        monitor.add_stock(symbol, name)
    
    elif args.report:
        monitor.generate_daily_report()
    
    elif args.run:
        monitor.run_monitoring(interval_minutes=args.interval)
    
    else:
        # 默认生成日报
        monitor.generate_daily_report()