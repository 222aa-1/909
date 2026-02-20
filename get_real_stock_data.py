#!/usr/bin/env python3
"""
获取华辰装备真实股票数据
使用多个数据源确保准确性
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time

def get_huachen_real_data():
    """获取华辰装备真实数据"""
    print("🔍 获取华辰装备(300809)真实数据...")
    print("=" * 60)
    
    results = {}
    
    # 方法1: 使用东方财富API
    print("\n1. 尝试东方财富API...")
    try:
        # 东方财富实时行情API
        url = "http://push2.eastmoney.com/api/qt/stock/get"
        params = {
            'secid': '0.300809',  # 0表示深交所，300809是股票代码
            'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f60,f84,f85,f86,f169,f170',
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'invt': '2',
            'fltt': '2'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('rc') == 0:
            stock_data = data.get('data', {})
            results['eastmoney'] = {
                '最新价': stock_data.get('f43', 0) / 100,  # 最新价，单位：分
                '涨跌幅': stock_data.get('f170', 0) / 100,  # 涨跌幅，单位：%
                '涨跌额': stock_data.get('f169', 0) / 100,  # 涨跌额，单位：分
                '成交量': stock_data.get('f47', 0),  # 成交量，单位：手
                '成交额': stock_data.get('f48', 0) / 10000,  # 成交额，单位：万元
                '最高价': stock_data.get('f44', 0) / 100,
                '最低价': stock_data.get('f45', 0) / 100,
                '开盘价': stock_data.get('f46', 0) / 100,
                '昨收': stock_data.get('f60', 0) / 100,
                '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print("✅ 东方财富数据获取成功")
        else:
            print("❌ 东方财富API返回错误")
    except Exception as e:
        print(f"❌ 东方财富API失败: {e}")
    
    # 方法2: 使用新浪财经API
    print("\n2. 尝试新浪财经API...")
    try:
        url = "http://hq.sinajs.cn/list=sz300809"
        headers = {
            'Referer': 'http://finance.sina.com.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        content = response.text
        
        # 解析新浪数据格式
        if 'var hq_str_sz300809' in content:
            data_str = content.split('="')[1].split('";')[0]
            data_list = data_str.split(',')
            
            if len(data_list) >= 32:
                results['sina'] = {
                    '股票名称': data_list[0],
                    '今日开盘价': float(data_list[1]),
                    '昨日收盘价': float(data_list[2]),
                    '当前价格': float(data_list[3]),
                    '今日最高价': float(data_list[4]),
                    '今日最低价': float(data_list[5]),
                    '竞买价': float(data_list[6]),
                    '竞卖价': float(data_list[7]),
                    '成交股数': int(data_list[8]),
                    '成交金额': float(data_list[9]),
                    '买一量': int(data_list[10]),
                    '买一价': float(data_list[11]),
                    '买二量': int(data_list[12]),
                    '买二价': float(data_list[13]),
                    '买三量': int(data_list[14]),
                    '买三价': float(data_list[15]),
                    '买四量': int(data_list[16]),
                    '买四价': float(data_list[17]),
                    '买五量': int(data_list[18]),
                    '买五价': float(data_list[19]),
                    '卖一量': int(data_list[20]),
                    '卖一价': float(data_list[21]),
                    '卖二量': int(data_list[22]),
                    '卖二价': float(data_list[23]),
                    '卖三量': int(data_list[24]),
                    '卖三价': float(data_list[25]),
                    '卖四量': int(data_list[26]),
                    '卖四价': float(data_list[27]),
                    '卖五量': int(data_list[28]),
                    '卖五价': float(data_list[29]),
                    '日期': data_list[30],
                    '时间': data_list[31],
                    '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                print("✅ 新浪财经数据获取成功")
            else:
                print("❌ 新浪数据格式错误")
        else:
            print("❌ 新浪API返回异常")
    except Exception as e:
        print(f"❌ 新浪财经API失败: {e}")
    
    # 方法3: 使用腾讯财经API
    print("\n3. 尝试腾讯财经API...")
    try:
        url = "http://qt.gtimg.cn/q=sz300809"
        response = requests.get(url, timeout=10)
        content = response.text
        
        if 'v_sz300809' in content:
            data_str = content.split('="')[1].split('";')[0]
            data_list = data_str.split('~')
            
            if len(data_list) >= 50:
                results['tencent'] = {
                    '股票名称': data_list[1],
                    '股票代码': data_list[2],
                    '当前价格': float(data_list[3]),
                    '昨收': float(data_list[4]),
                    '今开': float(data_list[5]),
                    '成交量': int(data_list[6]),
                    '外盘': int(data_list[7]),
                    '内盘': int(data_list[8]),
                    '买一价': float(data_list[9]),
                    '买一量': int(data_list[10]),
                    '买二价': float(data_list[11]),
                    '买二量': int(data_list[12]),
                    '买三价': float(data_list[13]),
                    '买三量': int(data_list[14]),
                    '买四价': float(data_list[15]),
                    '买四量': int(data_list[16]),
                    '买五价': float(data_list[17]),
                    '买五量': int(data_list[18]),
                    '卖一价': float(data_list[19]),
                    '卖一量': int(data_list[20]),
                    '卖二价': float(data_list[21]),
                    '卖二量': int(data_list[22]),
                    '卖三价': float(data_list[23]),
                    '卖三量': int(data_list[24]),
                    '卖四价': float(data_list[25]),
                    '卖四量': int(data_list[26]),
                    '卖五价': float(data_list[27]),
                    '卖五量': int(data_list[28]),
                    '最近逐笔成交': data_list[29],
                    '时间': data_list[30],
                    '涨跌': float(data_list[31]),
                    '涨跌幅': float(data_list[32]),
                    '最高': float(data_list[33]),
                    '最低': float(data_list[34]),
                    '价格/成交量(手)/成交额': data_list[35],
                    '成交量(手)': int(data_list[36]),
                    '成交额(万)': float(data_list[37]),
                    '换手率': float(data_list[38]),
                    '市盈率': float(data_list[39]),
                    '振幅': float(data_list[43]),
                    '流通市值': float(data_list[44]),
                    '总市值': float(data_list[45]),
                    '市净率': float(data_list[46]),
                    '涨停价': float(data_list[47]),
                    '跌停价': float(data_list[48]),
                    '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                print("✅ 腾讯财经数据获取成功")
            else:
                print("❌ 腾讯数据格式错误")
        else:
            print("❌ 腾讯API返回异常")
    except Exception as e:
        print(f"❌ 腾讯财经API失败: {e}")
    
    # 显示结果
    print("\n" + "=" * 60)
    print("📊 华辰装备(300809)真实数据汇总")
    print("=" * 60)
    
    if results:
        # 优先使用新浪数据（最稳定）
        if 'sina' in results:
            sina_data = results['sina']
            print(f"\n📈 来自新浪财经:")
            print(f"   股票名称: {sina_data['股票名称']}")
            print(f"   当前价格: ¥{sina_data['当前价格']:.2f}")
            print(f"   涨跌额: ¥{sina_data['当前价格'] - sina_data['昨日收盘价']:.2f}")
            print(f"   涨跌幅: {(sina_data['当前价格'] - sina_data['昨日收盘价']) / sina_data['昨日收盘价'] * 100:.2f}%")
            print(f"   今日开盘: ¥{sina_data['今日开盘价']:.2f}")
            print(f"   今日最高: ¥{sina_data['今日最高价']:.2f}")
            print(f"   今日最低: ¥{sina_data['今日最低价']:.2f}")
            print(f"   昨日收盘: ¥{sina_data['昨日收盘价']:.2f}")
            print(f"   成交量: {sina_data['成交股数']:,}股")
            print(f"   成交金额: ¥{sina_data['成交金额']:,.2f}")
            print(f"   更新时间: {sina_data['日期']} {sina_data['时间']}")
        
        # 腾讯数据提供更多财务指标
        if 'tencent' in results:
            tencent_data = results['tencent']
            print(f"\n💰 来自腾讯财经:")
            print(f"   市盈率(PE): {tencent_data['市盈率']:.2f}")
            print(f"   市净率(PB): {tencent_data['市净率']:.2f}")
            print(f"   换手率: {tencent_data['换手率']:.2f}%")
            print(f"   振幅: {tencent_data['振幅']:.2f}%")
            print(f"   总市值: {tencent_data['总市值']/10000:.2f}亿元")
            print(f"   流通市值: {tencent_data['流通市值']/10000:.2f}亿元")
            print(f"   涨停价: ¥{tencent_data['涨停价']:.2f}")
            print(f"   跌停价: ¥{tencent_data['跌停价']:.2f}")
        
        # 东方财富数据
        if 'eastmoney' in results:
            em_data = results['eastmoney']
            print(f"\n📊 来自东方财富:")
            print(f"   最新价: ¥{em_data['最新价']:.2f}")
            print(f"   涨跌幅: {em_data['涨跌幅']:.2f}%")
            print(f"   成交量: {em_data['成交量']:,}手")
            print(f"   成交额: ¥{em_data['成交额']:,.2f}万元")
        
        print(f"\n⏰ 数据获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 保存到文件
        with open('huachen_real_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 数据已保存到: huachen_real_data.json")
        
    else:
        print("❌ 所有数据源都失败了，无法获取真实数据")
        print("💡 建议:")
        print("   1. 检查网络连接")
        print("   2. 稍后重试")
        print("   3. 使用券商交易软件查看实时数据")
    
    print("\n" + "=" * 60)
    return results

def analyze_buy_price(real_data):
    """基于真实数据分析买入价格"""
    print("\n🎯 基于真实数据的年后买入价格分析")
    print("=" * 60)
    
    if 'sina' not in real_data:
        print("❌ 缺少核心价格数据，无法进行分析")
        return
    
    sina_data = real_data['sina']
    current_price = sina_data['当前价格']
    yesterday_close = sina_data['昨日收盘价']
    
    print(f"\n📊 当前市场数据:")
    print(f"   当前价格: ¥{current_price:.2f}")
    print(f"   昨日收盘: ¥{yesterday_close:.2f}")
    print(f"   今日开盘: ¥{sina_data['今日开盘价']:.2f}")
    print(f"   今日最高: ¥{sina_data['今日最高价']:.2f}")
    print(f"   今日最低: ¥{sina_data['今日最低价']:.2f}")
    
    # 技术分析
    print(f"\n📈 技术分析:")
    
    # 计算支撑阻力位
    today_range = sina_data['今日最高价'] - sina_data['今日最低价']
    support_1 = sina_data['今日最低价'] - today_range * 0.1
    support_2 = sina_data['今日最低价'] - today_range * 0.2
    resistance_1 = sina_data['今日最高价'] + today_range * 0.1
    resistance_2 = sina_data['今日最高价'] + today_range * 0.2
    
    print(f"   第一支撑位: ¥{support_1:.2f}")
    print(f"   第二支撑位: ¥{support_2:.2f}")
    print(f"   第一阻力位: ¥{resistance_1:.2f}")
    print(f"   第二阻力位: ¥{resistance_2:.2f}")
    
    # 买入建议
    print(f"\n💡 年后买入价格建议:")
    
    if current_price < yesterday_close:
        print(f"   当前处于下跌状态，建议等待更好买点")
        print(f"   保守买入区间: ¥{support_2:.2f} - ¥{support_1:.2f}")
        print(f"   适中买入区间: ¥{support_1:.2f} - ¥{current_price:.2f}")
    else:
        print(f"   当前处于上涨状态，可考虑分批买入")
        print(f"   保守买入区间: ¥{current_price*0.98:.2f} - ¥{current_price:.2f}")
        print(f"   适中买入区间: ¥{current_price:.2f} - ¥{resistance_1:.2f}")
    
    # 风险提示
    print(f"\n⚠️  风险提示:")
    print(f"   1. 春节后市场波动可能加大")
    print(f"   2. 关注成交量变化")
    print(f"   3. 设置止损位: ¥{support_2:.2f}")
    
    # 操作策略
    print(f"\n📋 操作策略:")
    print(f"   1. 分批建仓，不要一次性全仓")
    print(f"   2. 首次买入: 30%仓位")
    print(f"   3. 回调加仓: 40%仓位")
    print(f"   4. 突破加仓: 30%仓位")
    print(f"   5. 止损位: ¥{support_2:.2f}")
    print(f"   6. 目标位: ¥{resistance_2:.2f}")
    
    print(f"\n⏰ 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    print("🚀 华辰装备真实数据分析系统")
    print("=" * 60)
    
    # 获取真实数据
    real_data = get_huachen_real_data()
    
    # 分析买入价格
    if real_data:
        analyze_buy_price(real_data)
    
    print("\n✅ 分析完成！")
    print("💡 提示: 投资有风险，入市需谨慎")