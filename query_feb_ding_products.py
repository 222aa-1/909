#!/usr/bin/env python3
"""
查询2月份带'订'字的货品详细分析
"""

import sqlite3
from datetime import datetime
import json

class FebDingProductsAnalyzer:
    def __init__(self):
        self.db_path = "/Users/imac/Library/Containers/7417035F-7752-47D3-95AF-04AB71817726/Data/Library/LocalDatabase/ShopDiary-100191173-199155610"
        self.today = datetime.now()
        
    def analyze_feb_ding_products(self):
        """分析2月份带'订'字的货品"""
        print("="*80)
        print("📊 2月份带'订'字货品详细分析")
        print("="*80)
        print(f"分析时间: {self.today.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 1. 总体统计
            print("\n📈 总体统计:")
            
            cursor.execute("SELECT COUNT(*) FROM spu;")
            total_products = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM spu WHERE name LIKE '%订%';")
            total_with_ding = cursor.fetchone()[0]
            
            print(f"   总货品数量: {total_products:,} 个")
            print(f"   带'订'字货品: {total_with_ding:,} 个")
            print(f"   占比: {(total_with_ding/total_products*100):.1f}%")
            
            # 2. 2月份统计（各年）
            print("\n📅 2月份带'订'字货品统计（按年份）:")
            
            years = [2024, 2025, 2026]
            month = 2
            
            feb_stats = {}
            for year in years:
                cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM spu 
                    WHERE name LIKE '%订%' 
                    AND strftime('%Y-%m', datetime(createdDate/1000, 'unixepoch')) = '{year:04d}-{month:02d}'
                """)
                count = cursor.fetchone()[0]
                feb_stats[year] = count
            
            # 显示各年统计
            total_feb = sum(feb_stats.values())
            for year in years:
                count = feb_stats[year]
                if count > 0:
                    percentage = (count / total_feb * 100) if total_feb > 0 else 0
                    print(f"   {year}年2月: {count:4d} 个 ({percentage:.1f}%)")
            
            print(f"   2月份总计: {total_feb:,} 个")
            
            # 3. 2026年2月详细分析（当前年）
            print(f"\n🎯 2026年2月带'订'字货品详细分析:")
            
            year = 2026
            cursor.execute(f"""
                SELECT code, name, createdDate, purPrice, stdprice1 
                FROM spu 
                WHERE name LIKE '%订%' 
                AND strftime('%Y-%m', datetime(createdDate/1000, 'unixepoch')) = '{year:04d}-{month:02d}'
                ORDER BY createdDate DESC
            """)
            feb_2026_products = cursor.fetchall()
            
            print(f"   2026年2月货品数量: {len(feb_2026_products):,} 个")
            
            if feb_2026_products:
                # 按日期分组
                daily_counts = {}
                for code, name, created_ts, pur_price, sale_price in feb_2026_products:
                    dt = datetime.fromtimestamp(int(created_ts) / 1000)
                    day = dt.day
                    daily_counts[day] = daily_counts.get(day, 0) + 1
                
                print(f"\n   📅 每日新增数量:")
                for day in sorted(daily_counts.keys()):
                    count = daily_counts[day]
                    print(f"     2月{day:2d}日: {count:3d} 个")
                
                # 价格分析
                print(f"\n   💰 价格分析:")
                
                priced_products = [p for p in feb_2026_products if p[3] and p[4]]
                if priced_products:
                    total_pur = sum(p[3] for p in priced_products)
                    total_sale = sum(p[4] for p in priced_products)
                    count_priced = len(priced_products)
                    
                    avg_pur = total_pur / count_priced
                    avg_sale = total_sale / count_priced
                    avg_margin = ((avg_sale - avg_pur) / avg_sale * 100) if avg_sale > 0 else 0
                    
                    print(f"     有价格信息的货品: {count_priced} 个")
                    print(f"     平均进价: ¥{avg_pur:.2f}")
                    print(f"     平均售价: ¥{avg_sale:.2f}")
                    print(f"     平均毛利率: {avg_margin:.1f}%")
                
                # 商品类型分析
                print(f"\n   📦 商品类型分析:")
                
                type_keywords = {
                    '裙': ['裙', 'skirt'],
                    '裤': ['裤', 'pants'],
                    '外套': ['外套', 'jacket', 'coat'],
                    '上衣': ['衣', 'shirt', 'top', '衫'],
                    '鞋': ['鞋', 'shoe'],
                    '套装': ['套装', 'set'],
                    '包': ['包', 'bag']
                }
                
                type_counts = {key: 0 for key in type_keywords}
                other_count = 0
                
                for _, name, _, _, _ in feb_2026_products:
                    matched = False
                    for type_name, keywords in type_keywords.items():
                        for keyword in keywords:
                            if keyword in name.lower():
                                type_counts[type_name] += 1
                                matched = True
                                break
                        if matched:
                            break
                    if not matched:
                        other_count += 1
                
                # 显示类型统计
                for type_name, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                    if count > 0:
                        percentage = (count / len(feb_2026_products)) * 100
                        print(f"     {type_name}: {count:3d} 个 ({percentage:.1f}%)")
                
                if other_count > 0:
                    percentage = (other_count / len(feb_2026_products)) * 100
                    print(f"     其他: {other_count:3d} 个 ({percentage:.1f}%)")
                
                # 显示最新货品
                print(f"\n   🆕 最新10个货品:")
                for i, (code, name, created_ts, pur_price, sale_price) in enumerate(feb_2026_products[:10], 1):
                    dt = datetime.fromtimestamp(int(created_ts) / 1000)
                    date_str = dt.strftime('%m-%d %H:%M')
                    
                    price_info = ""
                    if pur_price and sale_price:
                        margin = ((sale_price - pur_price) / sale_price * 100) if sale_price > 0 else 0
                        price_info = f" ¥{sale_price:.0f} (毛利{margin:.0f}%)"
                    
                    print(f"     {i:2d}. {date_str} - {name}{price_info}")
            
            # 4. 对比分析（2024-2026年2月）
            print(f"\n📊 三年2月份对比分析:")
            
            comparison_data = []
            for year in years:
                cursor.execute(f"""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(CASE WHEN purPrice > 0 AND stdprice1 > 0 THEN 1 END) as priced,
                        AVG(CASE WHEN purPrice > 0 THEN purPrice END) as avg_pur,
                        AVG(CASE WHEN stdprice1 > 0 THEN stdprice1 END) as avg_sale
                    FROM spu 
                    WHERE name LIKE '%订%' 
                    AND strftime('%Y-%m', datetime(createdDate/1000, 'unixepoch')) = '{year:04d}-{month:02d}'
                """)
                stats = cursor.fetchone()
                
                total, priced, avg_pur, avg_sale = stats
                avg_pur = avg_pur if avg_pur else 0
                avg_sale = avg_sale if avg_sale else 0
                avg_margin = ((avg_sale - avg_pur) / avg_sale * 100) if avg_sale > 0 else 0
                
                comparison_data.append({
                    'year': year,
                    'total': total,
                    'priced': priced,
                    'avg_pur': avg_pur,
                    'avg_sale': avg_sale,
                    'avg_margin': avg_margin
                })
            
            # 显示对比表格
            print(f"   {'年份':<6} {'数量':<6} {'有价格':<6} {'平均进价':<10} {'平均售价':<10} {'毛利率':<8}")
            print(f"   {'-'*6} {'-'*6} {'-'*6} {'-'*10} {'-'*10} {'-'*8}")
            
            for data in comparison_data:
                if data['total'] > 0:
                    print(f"   {data['year']:<6} {data['total']:<6} {data['priced']:<6} ¥{data['avg_pur']:<9.1f} ¥{data['avg_sale']:<9.1f} {data['avg_margin']:<7.1f}%")
            
            # 5. 保存分析结果
            self.save_analysis_results(feb_2026_products, comparison_data, feb_stats)
            
            conn.close()
            
            print(f"\n" + "="*80)
            print("🎯 分析总结")
            print("="*80)
            
            print(f"""
基于对笑铺日记数据库的分析：

1. 📊 **总体情况**:
   - 总货品: {total_products:,} 个
   - 带'订'字货品: {total_with_ding:,} 个 ({total_with_ding/total_products*100:.1f}%)
   - 2月份带'订'字货品: {total_feb:,} 个

2. 📅 **时间趋势**:
   - 2024年2月: {feb_stats[2024]:,} 个
   - 2025年2月: {feb_stats[2025]:,} 个
   - 2026年2月: {feb_stats[2026]:,} 个
   - 趋势: {'增长' if feb_stats[2026] > feb_stats[2024] else '下降'}

3. 🎯 **2026年2月特点**:
   - 货品数量: {len(feb_2026_products):,} 个
   - 主要类型: {self.get_top_types(feb_2026_products)}
   - 价格水平: 平均售价约¥{comparison_data[2]['avg_sale']:.1f}

4. 💡 **经营建议**:
   - 2月份是'预订'类商品高峰期
   - 关注裙装、裤装等春季商品
   - 优化价格策略，提高毛利率
   - 加强新品推广和库存管理
            """)
            
        except Exception as e:
            print(f"❌ 分析错误: {e}")
            import traceback
            traceback.print_exc()
    
    def get_top_types(self, products):
        """获取主要商品类型"""
        if not products:
            return "无数据"
        
        type_counts = {}
        for _, name, _, _, _ in products:
            if '裙' in name:
                type_counts['裙'] = type_counts.get('裙', 0) + 1
            elif '裤' in name:
                type_counts['裤'] = type_counts.get('裤', 0) + 1
            elif '外套' in name:
                type_counts['外套'] = type_counts.get('外套', 0) + 1
            elif '衣' in name or '衫' in name:
                type_counts['上衣'] = type_counts.get('上衣', 0) + 1
            elif '鞋' in name:
                type_counts['鞋'] = type_counts.get('鞋', 0) + 1
        
        if not type_counts:
            return "其他"
        
        top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:2]
        return "、".join([f"{name}({count})" for name, count in top_types])
    
    def save_analysis_results(self, feb_2026_products, comparison_data, feb_stats):
        """保存分析结果"""
        results = {
            'analysis_date': self.today.isoformat(),
            'summary': {
                'total_products': feb_stats,
                'feb_total': sum(feb_stats.values()),
                'comparison': comparison_data
            },
            'feb_2026_products_sample': [
                {
                    'code': code,
                    'name': name,
                    'created_date': datetime.fromtimestamp(int(created_ts) / 1000).isoformat(),
                    'pur_price': pur_price,
                    'sale_price': sale_price
                }
                for code, name, created_ts, pur_price, sale_price in feb_2026_products[:50]  # 保存前50个
            ]
        }
        
        filename = f"feb_ding_products_analysis_{self.today.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 分析结果已保存: {filename}")
        
        # 同时生成文本报告
        text_filename = f"feb_ding_products_report_{self.today.strftime('%Y%m%d')}.txt"
        self.generate_text_report(text_filename, feb_2026_products, comparison_data, feb_stats)
    
    def generate_text_report(self, filename, feb_2026_products, comparison_data, feb_stats):
        """生成文本报告"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"笑铺日记2月份带'订'字货品分析报告\n")
            f.write(f"生成时间: {self.today.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            f.write("📊 总体统计\n")
            f.write(f"总货品数量: {sum(feb_stats.values()):,} 个\n")
            f.write(f"2024年2月: {feb_stats[2024]:,} 个\n")
            f.write(f"2025年2月: {feb_stats[2025]:,} 个\n")
            f.write(f"2026年2月: {feb_stats[2026]:,} 个\n\n")
            
            f.write("📈 三年对比\n")
            f.write("年份  数量  有价格  平均进价  平均售价  毛利率\n")
            f.write("-"*50 + "\n")
            for data in comparison_data:
                if data['total'] > 0:
                    f.write(f"{data['year']}   {data['total']:<5} {data['priced']:<6} ¥{data['avg_pur']:<8.1f} ¥{data['avg_sale']:<8.1f} {data['avg_margin']:.1f}%\n")
            
            f.write("\n🎯 2026年2月最新货品（前20个）\n")
            for i, (code, name, created_ts, _, _) in enumerate(feb_2026_products[:20], 1):
                dt = datetime.fromtimestamp(int(created_ts) / 1000)
                date_str = dt.strftime('%m-%d %H:%M')
                f.write(f"{i:2d}. {date_str} - {name} ({code})\n")
            
            f.write("\n💡 经营建议\n")
            f.write("1. 2月份重点关注'预订'类商品\n")
            f.write("2. 优化春季商品（裙、裤、外套）库存\n")
            f.write("3. 分析价格策略，提高毛利率\n")
            f.write("4. 加强新品推广和客户沟通\n")
        
        print(f"📄 文本报告已保存: {filename}")

def main():
    """主函数"""
    print("🛍️ 笑铺日记2月份带'订'字货品分析系统")
    print("="*60)
    
    analyzer = FebDingProductsAnalyzer()
    analyzer.analyze_feb_ding_products()
    
    print(f"\n🚀 使用说明:")
    print(f"   1. 分析结果已保存为JSON和TXT文件")
    print(f"   2. 可以查看详细的产品列表和统计")
    print(f"   3. 建议定期运行分析跟踪趋势")

if __name__ == "__main__":
    main()