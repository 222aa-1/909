#!/usr/bin/env python3
"""
查找笑铺日记销售数据
"""

import os
import json
import re
from datetime import datetime, date

def search_sales_data():
    """搜索销售数据"""
    base_path = "/Users/imac/Library/Containers/7417035F-7752-47D3-95AF-04AB71817726"
    
    print("🔍 搜索笑铺日记销售数据...")
    print("="*60)
    
    # 今天日期
    today = date.today().strftime("%Y-%m-%d")
    print(f"📅 查询日期: {today}")
    
    # 搜索销售相关文件
    sales_files = []
    
    # 1. 检查RCTAsyncLocalStorage文件
    rct_path = os.path.join(base_path, "Data/Library/Application Support/com.ecool.shopdiary/RCTAsyncLocalStorage_V1")
    if os.path.exists(rct_path):
        print(f"\n📁 检查RCTAsyncLocalStorage目录...")
        for file in os.listdir(rct_path):
            if file != "manifest.json":
                file_path = os.path.join(rct_path, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(5000)  # 只读取前5000字符
                        
                        # 搜索销售相关关键词
                        sales_keywords = ['sale', 'order', 'bill', '销售', '订单', '流水', '营业额']
                        found_keywords = []
                        
                        for keyword in sales_keywords:
                            if keyword.lower() in content.lower():
                                found_keywords.append(keyword)
                        
                        if found_keywords:
                            print(f"  找到销售数据: {file}")
                            print(f"    包含关键词: {', '.join(found_keywords)}")
                            
                            # 尝试解析JSON
                            try:
                                f.seek(0)
                                data = json.load(f)
                                if isinstance(data, dict) and 'rawData' in data:
                                    raw_data = data['rawData']
                                    if isinstance(raw_data, list) and len(raw_data) > 0:
                                        print(f"    数据条数: {len(raw_data)}")
                                        # 显示第一条数据
                                        if isinstance(raw_data[0], dict):
                                            print(f"    示例字段: {list(raw_data[0].keys())[:5]}")
                            except:
                                pass
                            
                            sales_files.append(file_path)
                except Exception as e:
                    pass
    
    # 2. 检查数据库文件
    print(f"\n📊 检查数据库文件...")
    db_path = os.path.join(base_path, "Data/Library/LocalDatabase/ShopDiary-100191173-199155610")
    if os.path.exists(db_path):
        print(f"  找到主数据库: {db_path}")
        
        import sqlite3
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 检查表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"  数据库表: {[t[0] for t in tables]}")
            
            # 检查spu表数据
            cursor.execute("SELECT COUNT(*) as count, MAX(updatedDate) as last_update FROM spu;")
            spu_info = cursor.fetchone()
            if spu_info:
                print(f"  商品数量: {spu_info[0]}, 最后更新: {spu_info[1]}")
            
            # 检查是否有今天的数据
            cursor.execute("SELECT COUNT(*) FROM spu WHERE updatedDate LIKE ?;", (f"%{today}%",))
            today_spu = cursor.fetchone()[0]
            print(f"  今天更新的商品: {today_spu}")
            
            conn.close()
        except Exception as e:
            print(f"  数据库查询错误: {e}")
    
    # 3. 检查Documents目录
    print(f"\n📄 检查Documents目录...")
    docs_path = os.path.join(base_path, "Data/Documents")
    if os.path.exists(docs_path):
        for file in os.listdir(docs_path):
            if file.endswith(('.json', '.txt', '.log')):
                file_path = os.path.join(docs_path, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)
                        if any(keyword in content.lower() for keyword in ['sale', '销售', 'order', '订单']):
                            print(f"  找到销售相关文件: {file}")
                            sales_files.append(file_path)
                except:
                    pass
    
    # 总结
    print(f"\n" + "="*60)
    print("📋 搜索结果总结")
    print("="*60)
    
    if sales_files:
        print(f"✅ 找到 {len(sales_files)} 个销售相关文件")
        print(f"\n💡 建议:")
        print(f"  1. 直接打开笑铺日记应用查看今日销售")
        print(f"  2. 使用应用的'销售报表'功能")
        print(f"  3. 导出销售数据为Excel或CSV")
    else:
        print(f"❌ 未找到销售数据文件")
        print(f"\n💡 可能的原因:")
        print(f"  1. 销售数据存储在云端")
        print(f"  2. 需要登录应用才能查看")
        print(f"  3. 数据格式为二进制或加密")
    
    print(f"\n🎯 推荐操作:")
    print(f"  1. 打开笑铺日记应用")
    print(f"  2. 进入'销售'或'报表'模块")
    print(f"  3. 选择今天日期查看销售详情")
    print(f"  4. 使用导出功能获取数据")
    
    return sales_files

def analyze_today_sales():
    """分析今日销售"""
    print(f"\n" + "="*60)
    print("📈 今日销售分析框架")
    print("="*60)
    
    # 模拟分析框架
    analysis_framework = {
        "销售统计": [
            "今日销售总额",
            "销售订单数量", 
            "平均客单价",
            "最畅销商品",
            "销售时间段分布"
        ],
        "商品分析": [
            "销售商品种类",
            "库存变化情况",
            "毛利率分析",
            "退货率统计"
        ],
        "客户分析": [
            "新老客户比例",
            "客户消费频次",
            "客户偏好分析"
        ],
        "趋势分析": [
            "环比昨日销售",
            "周销售趋势",
            "月销售目标完成度"
        ]
    }
    
    for category, items in analysis_framework.items():
        print(f"\n📊 {category}:")
        for item in items:
            print(f"  • {item}")
    
    print(f"\n🔧 需要的数据:")
    print(f"  1. 销售订单明细")
    print(f"  2. 商品信息表")
    print(f"  3. 客户信息表")
    print(f"  4. 库存变动记录")

def main():
    """主函数"""
    print("笑铺日记销售数据查询工具")
    print("="*60)
    
    # 搜索销售数据
    sales_files = search_sales_data()
    
    # 提供分析框架
    analyze_today_sales()
    
    print(f"\n🚀 下一步操作:")
    print(f"  1. 手动打开笑铺日记查看销售")
    print(f"  2. 截图销售报表发给我分析")
    print(f"  3. 导出销售数据文件")
    print(f"  4. 告诉我具体需要什么统计")

if __name__ == "__main__":
    main()