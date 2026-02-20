#!/usr/bin/env python3
"""
测试多种数据获取方法
"""

import akshare as ak
import pandas as pd

def test_methods(symbol="300809"):
    print(f"测试股票代码: {symbol}")
    
    methods = [
        ("stock_zh_a_hist", {"symbol": symbol, "period": "daily", "start_date": "20240101", "end_date": "20260218", "adjust": ""}),
        ("stock_zh_a_daily", {"symbol": f"sz{symbol}" if symbol.startswith('30') else f"sh{symbol}"}),
        ("stock_zh_a_spot", {}),
    ]
    
    for method_name, params in methods:
        print(f"\n尝试方法: {method_name}")
        try:
            if method_name == "stock_zh_a_hist":
                df = ak.stock_zh_a_hist(**params)
            elif method_name == "stock_zh_a_daily":
                df = ak.stock_zh_a_daily(**params)
            elif method_name == "stock_zh_a_spot":
                df = ak.stock_zh_a_spot()
                # 过滤出目标股票
                df = df[df['代码'] == symbol]
            else:
                continue
            
            if not df.empty:
                print(f"成功! 获取到 {len(df)} 条数据")
                print(f"列名: {list(df.columns)}")
                if '日期' in df.columns:
                    print(f"时间范围: {df['日期'].min()} 到 {df['日期'].max()}")
                return df
            else:
                print("数据为空")
                
        except Exception as e:
            print(f"错误: {e}")
    
    return None

def get_basic_info(symbol="300809"):
    """获取股票基本信息"""
    print(f"\n获取 {symbol} 基本信息...")
    
    try:
        # 获取实时行情
        df = ak.stock_zh_a_spot()
        stock_info = df[df['代码'] == symbol]
        
        if not stock_info.empty:
            print("实时行情:")
            print(f"  名称: {stock_info['名称'].iloc[0]}")
            print(f"  最新价: {stock_info['最新价'].iloc[0]}")
            print(f"  涨跌幅: {stock_info['涨跌幅'].iloc[0]}%")
            print(f"  成交量: {stock_info['成交量'].iloc[0]}")
            print(f"  成交额: {stock_info['成交额'].iloc[0]}")
            return stock_info
        else:
            print("未找到该股票")
    except Exception as e:
        print(f"获取基本信息错误: {e}")
    
    return None

if __name__ == "__main__":
    symbol = "300809"
    
    print("="*50)
    print("华辰装备数据获取测试")
    print("="*50)
    
    # 测试各种方法
    df = test_methods(symbol)
    
    # 获取基本信息
    info = get_basic_info(symbol)
    
    if df is None and info is None:
        print("\n所有方法都失败了，可能原因:")
        print("1. AKShare数据源暂时不可用")
        print("2. 需要更新AKShare版本")
        print("3. 网络连接问题")
        print("\n替代方案:")
        print("1. 使用其他数据源（如Tushare、Baostock）")
        print("2. 手动从财经网站获取数据")
        print("3. 使用浏览器自动化工具")