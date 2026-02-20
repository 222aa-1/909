#!/usr/bin/env python3
"""
整理2026年2月份带'订'字的货品
按服装描述4个字相同归为一类，标记订货销售是谁
"""

import sqlite3
import json
import re
from datetime import datetime
from collections import defaultdict

class FebDingProductsAnalyzer:
    def __init__(self):
        self.db_path = "/Users/imac/Library/Containers/7417035F-7752-47D3-95AF-04AB71817726/Data/Library/LocalDatabase/ShopDiary-100191173-199155610"
        
    def analyze(self):
        """分析2026年2月带'订'字的货品"""
        print("="*80)
        print("📊 2026年2月带'订'字货品分析")
        print("="*80)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查询2026年2月所有带'订'字的货品
            cursor.execute("""
                SELECT code, name, createdDate, purPrice, stdprice1 
                FROM spu 
                WHERE name LIKE '%订%' 
                AND strftime('%Y-%m', datetime(createdDate/1000, 'unixepoch')) = '2026-02'
                ORDER BY createdDate DESC
            """)
            
            all_products = cursor.fetchall()
            
            print(f"📦 2026年2月带'订'字货品总数: {len(all_products)} 个")
            print()
            
            # 分析每个货品
            analyzed_products = []
            
            for code, name, created_ts, pur_price, sale_price in all_products:
                # 解析销售人（名称中'订'字前面的部分）
                seller = self.extract_seller(name)
                
                # 提取服装描述和分类
                category, description = self.extract_category_and_description(name)
                
                # 创建时间
                create_time = datetime.fromtimestamp(int(created_ts) / 1000)
                
                product_info = {
                    '编码': code,
                    '完整名称': name,
                    '销售人': seller,
                    '分类': category,
                    '描述': description,
                    '进价': float(pur_price) if pur_price else None,
                    '售价': float(sale_price) if sale_price else None,
                    '创建日期': create_time.strftime('%Y-%m-%d'),
                    '创建时间': create_time.strftime('%H:%M:%S'),
                    '时间戳': create_time
                }
                
                analyzed_products.append(product_info)
            
            # 按销售人分组
            products_by_seller = defaultdict(list)
            for product in analyzed_products:
                products_by_seller[product['销售人']].append(product)
            
            # 按分类分组
            products_by_category = defaultdict(list)
            for product in analyzed_products:
                products_by_category[product['分类']].append(product)
            
            # 显示统计信息
            self.display_statistics(analyzed_products, products_by_seller, products_by_category)
            
            # 生成详细报告
            self.generate_reports(analyzed_products, products_by_seller, products_by_category)
            
            conn.close()
            
            print("\n" + "="*80)
            print("✅ 分析完成！")
            print("="*80)
            
        except Exception as e:
            print(f"❌ 分析错误: {e}")
            import traceback
            traceback.print_exc()
    
    def extract_seller(self, name):
        """提取销售人"""
        if '订' in name:
            parts = name.split('订', 1)
            seller = parts[0].strip()
            # 销售人通常是1-3个中文字符
            if 0 < len(seller) <= 3 and all('\u4e00' <= char <= '\u9fff' for char in seller):
                return seller
        return '其他'
    
    def extract_category_and_description(self, name):
        """提取分类和描述"""
        # 移除销售人部分
        product_name = name
        if '订' in product_name:
            product_name = product_name.split('订', 1)[1]
        
        # 常见服装类型关键词
        clothing_keywords = {
            '短裙': ['短裙', '半裙', '迷你裙'],
            '长裙': ['长裙', '连衣裙', '裙装'],
            '短裤': ['短裤', '热裤'],
            '长裤': ['长裤', '裤子', '牛仔裤', '休闲裤', '运动裤'],
            '外套': ['外套', '夹克', 'jacket', 'coat'],
            '大衣': ['大衣', '风衣', '羽绒服'],
            '卫衣': ['卫衣', 'hoodie'],
            'T恤': ['T恤', 'T恤衫', 'tee'],
            '衬衫': ['衬衫', '衬衣', 'shirt'],
            '毛衣': ['毛衣', '针织衫', '毛衫'],
            '套装': ['套装', 'set', '套裝'],
            '鞋子': ['鞋子', '鞋', 'shoe', 'sneaker'],
            '包包': ['包包', '包', 'bag'],
            '帽子': ['帽子', '帽', 'hat', 'cap']
        }
        
        # 尝试匹配已知分类
        for category, keywords in clothing_keywords.items():
            for keyword in keywords:
                if keyword in product_name:
                    # 提取描述（去除分类关键词后的部分）
                    description = product_name.replace(keyword, '').strip()
                    # 取前4个非空字符作为简化描述
                    clean_desc = re.sub(r'[0-9\W_]', '', description)
                    if len(clean_desc) >= 4:
                        description = clean_desc[:4]
                    elif clean_desc:
                        description = clean_desc
                    else:
                        description = '其他'
                    
                    return category, description
        
        # 如果没有匹配到已知分类，使用自定义规则
        # 提取产品名中的关键部分（通常是风格或系列名）
        # 例如："Open风格G1143米杏L" -> "Open风格"
        
        # 移除尺寸和颜色信息
        size_pattern = r'[SMLXL\d]+码?'
        color_pattern = r'[黑白红蓝绿黄紫粉灰棕米咖杏银金][色]?'
        
        clean_name = re.sub(size_pattern, '', product_name)
        clean_name = re.sub(color_pattern, '', clean_name)
        clean_name = re.sub(r'[0-9]', '', clean_name)
        
        # 提取前4个中文字符或前2个英文单词
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', clean_name)
        if len(chinese_chars) >= 2:
            category = ''.join(chinese_chars[:2])
            description = clean_name.replace(category, '').strip()[:20]
        else:
            # 提取英文或混合内容
            words = clean_name.split()
            if len(words) >= 2:
                category = ' '.join(words[:2])[:4]
                description = ' '.join(words[2:])[:20] if len(words) > 2 else '其他'
            else:
                category = clean_name[:4] if clean_name else '其他'
                description = '其他'
        
        return category, description
    
    def display_statistics(self, products, products_by_seller, products_by_category):
        """显示统计信息"""
        print("👥 销售人统计:")
        print("-"*40)
        
        seller_stats = []
        for seller, items in sorted(products_by_seller.items(), key=lambda x: len(x[1]), reverse=True):
            count = len(items)
            seller_stats.append((seller, count))
            print(f"{seller:4s}: {count:3d} 个货品")
        
        print()
        
        print("📦 分类统计:")
        print("-"*40)
        
        category_stats = []
        for category, items in sorted(products_by_category.items(), key=lambda x: len(x[1]), reverse=True):
            count = len(items)
            category_stats.append((category, count))
            if count >= 3:  # 只显示数量较多的分类
                print(f"{category:8s}: {count:3d} 个货品")
        
        other_count = sum(1 for _, count in category_stats if count < 3)
        if other_count > 0:
            print(f"其他分类: {other_count} 个")
        
        print()
        
        # 显示详细列表
        print("📋 详细货品列表（按销售人分组）:")
        print("="*80)
        
        for seller, items in sorted(products_by_seller.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n🎯 销售人: {seller} ({len(items)}个)")
            print("-"*60)
            
            # 按分类分组
            items_by_category = defaultdict(list)
            for item in items:
                items_by_category[item['分类']].append(item)
            
            for category, cat_items in sorted(items_by_category.items(), key=lambda x: len(x[1]), reverse=True):
                print(f"  📁 {category} ({len(cat_items)}个):")
                for item in cat_items[:5]:  # 每个分类显示前5个
                    price_info = ""
                    if item['售价']:
                        price_info = f" [¥{item['售价']}]"
                    print(f"    • {item['完整名称']}{price_info}")
                
                if len(cat_items) > 5:
                    print(f"    ... 还有 {len(cat_items) - 5} 个")
    
    def generate_reports(self, products, products_by_seller, products_by_category):
        """生成报告文件"""
        print("\n💾 正在生成报告文件...")
        
        # 1. 生成结构化JSON报告
        json_report = {
            '分析时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '总货品数量': len(products),
            '销售人统计': [
                {
                    '销售人': seller,
                    '数量': len(items),
                    '占比': f"{(len(items)/len(products)*100):.1f}%"
                }
                for seller, items in sorted(products_by_seller.items(), key=lambda x: len(x[1]), reverse=True)
            ],
            '分类统计': [
                {
                    '分类': category,
                    '数量': len(items),
                    '占比': f"{(len(items)/len(products)*100):.1f}%"
                }
                for category, items in sorted(products_by_category.items(), key=lambda x: len(x[1]), reverse=True)
                if len(items) >= 2
            ],
            '详细货品列表': [
                {
                    '编码': p['编码'],
                    '完整名称': p['完整名称'],
                    '销售人': p['销售人'],
                    '分类': p['分类'],
                    '描述': p['描述'],
                    '进价': p['进价'],
                    '售价': p['售价'],
                    '创建日期': p['创建日期'],
                    '创建时间': p['创建时间']
                }
                for p in products
            ]
        }
        
        json_filename = '2026年2月带订字货品详细分析.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON报告已保存: {json_filename}")
        
        # 2. 生成文本格式报告
        text_lines = []
        text_lines.append("2026年2月带'订'字货品详细列表")
        text_lines.append("="*60)
        text_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        text_lines.append(f"总数量: {len(products)} 个")
        text_lines.append("")
        
        # 按销售人分组
        for seller, items in sorted(products_by_seller.items(), key=lambda x: len(x[1]), reverse=True):
            text_lines.append(f"🎯 销售人: {seller} ({len(items)}个)")
            text_lines.append("-"*40)
            
            # 按分类分组
            items_by_category = defaultdict(list)
            for item in items:
                items_by_category[item['分类']].append(item)
            
            for category, cat_items in sorted(items_by_category.items(), key=lambda x: len(x[1]), reverse=True):
                text_lines.append(f"  📁 {category} ({len(cat_items)}个):")
                for item in cat_items:
                    price_info = ""
                    if item['售价']:
                        price_info = f" [¥{item['售价']}]"
                    text_lines.append(f"    • {item['完整名称']}{price_info}")
                text_lines.append("")
            
            text_lines.append("")
        
        txt_filename = '2026年2月带订字货品列表.txt'
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text_lines))
        
        print(f"✅ 文本报告已保存: {txt_filename}")
        
        # 3. 生成CSV格式（便于导入Excel）
        csv_lines = []
        csv_lines.append("编码,完整名称,销售人,分类,描述,进价,售价,创建日期,创建时间")
        
        for product in products:
            pur_price = product['进价'] if product['进价'] else ''
            sale_price = product['售价'] if product['售价'] else ''
            
            # 处理CSV特殊字符
            name = product['完整名称'].replace(',', '，').replace('"', '""')
            
            csv_line = f"{product['编码']},\"{name}\",{product['销售人']},{product['分类']},{product['描述']},{pur_price},{sale_price},{product['创建日期']},{product['创建时间']}"
            csv_lines.append(csv_line)
        
        csv_filename = '2026年2月带订字货品.csv'
        with open(csv_filename, 'w', encoding='utf-8-sig') as f:  # utf-8-sig for Excel compatibility
            f.write('\n'.join(csv_lines))
        
        print(f"✅ CSV文件已保存: {csv_filename} (可直接用Excel打开)")
        
        # 4. 生成汇总统计
        summary_lines = []
        summary_lines.append("2026年2月带'订'字货品汇总统计")
        summary_lines.append("="*60)
        summary_lines.append(f"统计时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append(f"总货品数量: {len(products)} 个")
        summary_lines.append("")
        
        summary_lines.append("👥 销售人业绩排名:")
        summary_lines.append("-"*40)
        for i, (seller, items) in enumerate(sorted(products_by_seller.items(), key=lambda x: len(x[1]), reverse=True)[:10], 1):
            percentage = len(items) / len(products) * 100
            summary_lines.append(f"{i:2d}. {seller:4s}: {len(items):3d} 个 ({percentage:.1f}%)")
        
        summary_lines.append("")
        summary_lines.append("📦 热门分类排名:")
        summary_lines.append("-"*40)
        for i, (category, items) in enumerate(sorted(products_by_category.items(), key=lambda x: len(x[1]), reverse=True)[:10], 1):
            percentage = len(items) / len(products) * 100
            summary_lines.append(f"{i:2d}. {category:8s}: {len(items):3d} 个 ({percentage:.1f}%)")
        
        summary_filename = '2026年2月带订字货品汇总.txt'
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_lines))
        
        print(f"✅ 汇总统计已保存: {summary_filename}")
        
        print("\n📁 已生成的文件:")
        print(f"  1. {json_filename} - 结构化数据")
        print(f"  2. {txt_filename} - 文本格式列表")
        print(f"  3. {csv_filename} - CSV格式（Excel可打开）")
        print(f"  4. {summary_filename} - 汇总统计")

def main():
    """主函数"""
    print("🛍️ 2026年2月带'订'字货品分析系统")
    print("="*60)
    
    analyzer = FebDingProductsAnalyzer()
    analyzer.analyze()
    
    print("\n🚀 使用说明:")
    print("   1. CSV文件可直接用Excel打开")
    print("   2. JSON文件包含完整结构化数据")
    print("   3. 文本文件便于快速查看")
    print("   4. 汇总文件提供关键统计信息")

if __name__ == "__main__":
    main()