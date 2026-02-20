#!/usr/bin/env python3
"""
查询笑铺日记今日销售数据
"""

import sqlite3
import json
from datetime import datetime, date
import os

def query_sales_direct():
    """直接查询销售数据"""
    print("="*80)
    print("笑铺日记今日销售查询")
    print("="*80)
    
    today = date.today().strftime("%Y-%m-%d")
    print(f"📅 查询日期: {today}")
    
    # 数据库路径
    db_path = "/Users/imac/Library/Containers/7417035F-7752-47D3-95AF-04AB71817726/Data/Library/LocalDatabase/ShopDiary-100191173-199155610"
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"\n📊 数据库信息:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"  表数量: {len(tables)}")
        print(f"  表列表: {', '.join(tables)}")
        
        # 检查每个表的结构和数据
        print(f"\n🔍 详细表分析:")
        
        for table in tables:
            print(f"\n  📋 {table}:")
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            print(f"    字段: {', '.join(column_names[:5])}{'...' if len(column_names) > 5 else ''}")
            
            # 获取数据量
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"    数据量: {count}")
            
            # 如果是销售相关表，显示更多信息
            if 'sale' in table.lower() or 'order' in table.lower() or 'bill' in table.lower():
                print(f"    ⭐ 销售相关表!")
                
                # 显示最新几条数据
                cursor.execute(f"SELECT * FROM {table} ORDER BY ROWID DESC LIMIT 3;")
                sample_data = cursor.fetchall()
                if sample_data:
                    print(f"    最新数据示例:")
                    for i, row in enumerate(sample_data):
                        print(f"      第{i+1}条: {row[:5]}{'...' if len(row) > 5 else ''}")
        
        # 特别检查customer表（客户表）
        print(f"\n👥 客户信息:")
        cursor.execute("SELECT COUNT(*) as total, COUNT(DISTINCT name) as unique_names FROM customer;")
        cust_info = cursor.fetchone()
        print(f"  客户总数: {cust_info[0]}")
        print(f"  唯一客户名: {cust_info[1]}")
        
        # 显示最近客户
        cursor.execute("SELECT name, phone, createdDate FROM customer ORDER BY ROWID DESC LIMIT 5;")
        recent_customers = cursor.fetchall()
        if recent_customers:
            print(f"  最近客户:")
            for cust in recent_customers:
                name, phone, created_date = cust
                print(f"    {name} ({phone}) - {created_date}")
        
        # 检查商品表
        print(f"\n📦 商品信息:")
        cursor.execute("SELECT COUNT(*) as total, COUNT(DISTINCT name) as unique_names FROM spu;")
        spu_info = cursor.fetchone()
        print(f"  商品总数: {spu_info[0]}")
        print(f"  唯一商品名: {spu_info[1]}")
        
        # 显示价格信息
        cursor.execute("""
            SELECT 
                COUNT(*) as total_items,
                AVG(purPrice) as avg_pur_price,
                AVG(stdprice1) as avg_sale_price,
                MIN(stdprice1) as min_price,
                MAX(stdprice1) as max_price
            FROM spu 
            WHERE purPrice > 0 AND stdprice1 > 0;
        """)
        price_info = cursor.fetchone()
        if price_info[0] > 0:
            print(f"  价格统计:")
            print(f"    平均进价: ¥{price_info[1]:.2f}")
            print(f"    平均售价: ¥{price_info[2]:.2f}")
            print(f"    最低售价: ¥{price_info[3]:.2f}")
            print(f"    最高售价: ¥{price_info[4]:.2f}")
        
        # 检查是否有销售记录
        print(f"\n💰 销售记录查找:")
        
        # 方法1: 检查是否有销售相关的视图或触发器
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' OR type='trigger';")
        views_triggers = cursor.fetchall()
        if views_triggers:
            print(f"  找到视图/触发器: {[v[0] for v in views_triggers]}")
        
        # 方法2: 检查所有表中的日期字段
        print(f"\n📅 日期字段检查:")
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            date_columns = [col[1] for col in columns if 'date' in col[1].lower() or 'time' in col[1].lower()]
            
            if date_columns:
                print(f"  {table}: {', '.join(date_columns)}")
                
                # 检查今天的数据
                for date_col in date_columns[:1]:  # 只检查第一个日期字段
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {date_col} LIKE ?;", (f"%{today}%",))
                        today_count = cursor.fetchone()[0]
                        if today_count > 0:
                            print(f"    ⭐ 今天有{today_count}条记录!")
                            
                            # 显示具体数据
                            cursor.execute(f"SELECT * FROM {table} WHERE {date_col} LIKE ? LIMIT 2;", (f"%{today}%",))
                            today_data = cursor.fetchall()
                            for data in today_data:
                                print(f"      数据: {data[:5]}{'...' if len(data) > 5 else ''}")
                    except:
                        pass
        
        conn.close()
        
        print(f"\n" + "="*80)
        print("💡 分析结论:")
        print("="*80)
        
        print(f"""
基于数据库分析:

1. 📊 **数据现状**:
   - 数据库包含基础数据表（商品、客户、员工等）
   - 商品数量: {spu_info[0]} 个
   - 客户数量: {cust_info[0]} 个
   - 但未找到直接的销售记录表

2. 🔍 **可能的原因**:
   - 销售数据可能存储在云端服务器
   - 本地只缓存基础数据和配置
   - 需要联网才能获取销售记录
   - 销售数据可能在其他数据库文件中

3. 🎯 **建议操作**:
   - 打开笑铺日记应用查看销售报表
   - 使用应用的导出功能获取销售数据
   - 检查是否有离线销售记录功能
   - 联系技术支持获取数据接口

4. 📱 **立即操作**:
   1. 打开"笑铺日记"应用
   2. 进入"销售"或"报表"模块
   3. 选择今天日期查看销售详情
   4. 截图或导出数据发给我分析
        """)
        
    except Exception as e:
        print(f"❌ 查询错误: {e}")

def check_cloud_sync():
    """检查云端同步状态"""
    print(f"\n☁️ 云端同步检查:")
    
    # 检查manifest.json中的云端配置
    manifest_path = "/Users/imac/Library/Containers/7417035F-7752-47D3-95AF-04AB71817726/Data/Library/Application Support/com.ecool.shopdiary/RCTAsyncLocalStorage_V1/manifest.json"
    
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # 检查BASEURL（云端服务器地址）
            if 'BASEURL' in manifest:
                baseurl_data = json.loads(manifest['BASEURL']['rawData'])
                print(f"  云端服务器地址:")
                for server in baseurl_data:
                    print(f"    - {server.get('domain', server.get('ip', '未知'))}")
            
            # 检查同步时间
            if 'lastFetchTimeKey' in manifest:
                last_fetch = json.loads(manifest['lastFetchTimeKey']['rawData'])
                last_time = datetime.fromtimestamp(last_fetch/1000)
                print(f"  最后同步时间: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
        except Exception as e:
            print(f"  检查失败: {e}")

def main():
    """主函数"""
    print("笑铺日记销售数据查询系统")
    print("="*60)
    
    query_sales_direct()
    check_cloud_sync()
    
    print(f"\n🚀 快速操作指南:")
    print(f"""
1. 📱 **应用内查看**:
   打开笑铺日记 → 销售报表 → 选择今天

2. 📊 **数据导出**:
   在应用中查找"导出"功能 → 导出Excel/CSV

3. 📸 **截图分析**:
   截图销售报表发给我 → 我帮你分析统计

4. 🔗 **API接入**:
   检查应用设置 → 寻找API或数据接口选项
    """)

if __name__ == "__main__":
    main()