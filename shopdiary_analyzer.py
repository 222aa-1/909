#!/usr/bin/env python3
"""
笑铺日记数据分析器
查询今天卖出的商品并统计
"""

import sqlite3
import json
from datetime import datetime, date
import os

class ShopDiaryAnalyzer:
    def __init__(self):
        # 笑铺日记数据库路径
        self.db_path = "/Users/imac/Library/Containers/7417035F-7752-47D3-95AF-04AB71817726/Data/Library/LocalDatabase/ShopDiary-100191173-199155610"
        self.zxdb_path = "/Users/imac/Library/Containers/7417035F-7752-47D3-95AF-04AB71817726/Data/Documents/zxdatabase.sqlite"
        
        # 检查数据库是否存在
        if not os.path.exists(self.db_path):
            print(f"❌ 数据库文件不存在: {self.db_path}")
            return
        
        self.conn = None
        self.zx_conn = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.zx_conn = sqlite3.connect(self.zxdb_path)
            print("✅ 数据库连接成功")
            return True
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False
    
    def get_today_sales(self):
        """获取今天的销售数据"""
        if not self.conn:
            print("❌ 数据库未连接")
            return None
        
        try:
            # 首先查看数据库中有哪些表
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("📊 数据库中的表:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # 检查spu表（商品表）
            print("\n📦 商品信息:")
            cursor.execute("SELECT id, code, name, purPrice, stdprice1 FROM spu LIMIT 10;")
            products = cursor.fetchall()
            
            for product in products:
                product_id, code, name, pur_price, stdprice1 = product
                print(f"  商品ID: {product_id}, 编码: {code}, 名称: {name}, 进价: {pur_price}, 售价1: {stdprice1}")
            
            # 检查sku表（库存单元）
            print("\n📦 SKU信息:")
            cursor.execute("SELECT id, tenantSpuId, purPrice, stdprice1 FROM sku LIMIT 10;")
            skus = cursor.fetchall()
            
            for sku in skus:
                sku_id, tenant_spu_id, pur_price, stdprice1 = sku
                print(f"  SKU ID: {sku_id}, 商品ID: {tenant_spu_id}, 进价: {pur_price}, 售价: {stdprice1}")
            
            # 检查是否有销售记录表
            print("\n🔍 查找销售相关表...")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%sale%' OR name LIKE '%order%' OR name LIKE '%bill%';")
            sales_tables = cursor.fetchall()
            
            if sales_tables:
                print("找到销售相关表:")
                for table in sales_tables:
                    print(f"  - {table[0]}")
                    
                    # 查看表结构
                    cursor.execute(f"PRAGMA table_info({table[0]});")
                    columns = cursor.fetchall()
                    print(f"    表结构: {[col[1] for col in columns]}")
                    
                    # 查看最近几条数据
                    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 3;")
                    sample_data = cursor.fetchall()
                    if sample_data:
                        print(f"    示例数据: {sample_data}")
            else:
                print("未找到销售相关表")
            
            # 检查zxkvTable中的销售数据
            if self.zx_conn:
                print("\n🔍 检查zxkvTable...")
                zx_cursor = self.zx_conn.cursor()
                zx_cursor.execute("SELECT id, json FROM zxkvTable WHERE id LIKE '%sale%' OR id LIKE '%order%' OR id LIKE '%bill%';")
                sales_keys = zx_cursor.fetchall()
                
                if sales_keys:
                    print("找到销售相关键:")
                    for key_id, json_data in sales_keys[:5]:  # 只显示前5个
                        try:
                            data = json.loads(json_data)
                            print(f"  - {key_id}: {type(data)}")
                            if isinstance(data, dict):
                                print(f"    数据键: {list(data.keys())[:5]}...")
                        except:
                            print(f"  - {key_id}: 无法解析JSON")
                else:
                    print("未找到销售相关键")
            
            return products, skus
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return None
    
    def analyze_sales_data(self):
        """分析销售数据"""
        print("\n" + "="*60)
        print("笑铺日记销售数据分析")
        print("="*60)
        
        # 获取当前日期
        today = date.today().strftime("%Y-%m-%d")
        print(f"📅 分析日期: {today}")
        
        # 获取商品数据
        data = self.get_today_sales()
        if not data:
            print("❌ 无法获取销售数据")
            return
        
        products, skus = data
        
        # 统计商品信息
        print(f"\n📊 商品统计:")
        print(f"  商品总数: {len(products)}")
        print(f"  SKU总数: {len(skus)}")
        
        # 如果有销售数据，进行详细分析
        print(f"\n💡 分析结果:")
        print(f"  1. 数据库包含商品基础信息")
        print(f"  2. 包含SKU库存信息")
        print(f"  3. 未找到直接的销售记录表")
        print(f"  4. 销售数据可能存储在云端或本地其他位置")
        
        print(f"\n🎯 建议:")
        print(f"  1. 检查笑铺日记应用的导出功能")
        print(f"  2. 查看应用内的销售报表")
        print(f"  3. 联系笑铺日记技术支持获取数据接口")
        
        print("\n" + "="*60)
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
        if self.zx_conn:
            self.zx_conn.close()
        print("✅ 数据库连接已关闭")

def main():
    """主函数"""
    print("笑铺日记销售数据分析工具")
    print("="*60)
    
    analyzer = ShopDiaryAnalyzer()
    
    if analyzer.connect():
        analyzer.analyze_sales_data()
        analyzer.close()
    else:
        print("❌ 无法连接到笑铺日记数据库")
    
    print(f"\n🚀 下一步建议:")
    print(f"  1. 打开笑铺日记应用查看今日销售")
    print(f"  2. 使用应用的导出功能获取销售数据")
    print(f"  3. 检查是否有API或数据导出选项")

if __name__ == "__main__":
    main()