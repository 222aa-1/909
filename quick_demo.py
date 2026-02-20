#!/usr/bin/env python3
"""
快速演示笑铺日记销售分析
"""

from datetime import datetime, date
import json

def quick_demo():
    """快速演示"""
    today = date.today().strftime("%Y-%m-%d")
    
    print("="*80)
    print("📊 笑铺日记销售分析快速演示")
    print("="*80)
    print(f"📅 演示日期: {today}")
    print("="*80)
    
    # 模拟数据
    demo_data = {
        'total_amount': 8560.50,
        'order_count': 32,
        'customer_count': 28,
        'products': [
            {'name': '灰色字母加绒卫衣', 'quantity': 8, 'amount': 1272.00},
            {'name': '北面羽绒裤', 'quantity': 5, 'amount': 1345.00},
            {'name': '预订小衫', 'quantity': 12, 'amount': 828.00},
            {'name': '紫色加绒连帽卫衣', 'quantity': 6, 'amount': 1194.00},
            {'name': '防风裤时尚松紧', 'quantity': 4, 'amount': 716.00},
        ]
    }
    
    # 分析
    total = demo_data['total_amount']
    orders = demo_data['order_count']
    customers = demo_data['customer_count']
    products = demo_data['products']
    
    print(f"\n📊 销售概况:")
    print(f"  销售总额: ¥{total:,.2f}")
    print(f"  订单数量: {orders} 笔")
    print(f"  客户数量: {customers} 人")
    print(f"  平均客单价: ¥{total/orders:,.2f}")
    
    print(f"\n📦 商品销售TOP 3:")
    products_sorted = sorted(products, key=lambda x: x['amount'], reverse=True)
    for i, product in enumerate(products_sorted[:3], 1):
        print(f"  {i}. {product['name']}: {product['quantity']}件, ¥{product['amount']:,.2f}")
    
    total_quantity = sum(p['quantity'] for p in products)
    total_product_amount = sum(p['amount'] for p in products)
    
    print(f"\n📈 商品统计:")
    print(f"  销售商品种类: {len(products)} 种")
    print(f"  总销售数量: {total_quantity} 件")
    print(f"  商品销售总额: ¥{total_product_amount:,.2f}")
    
    print(f"\n🎯 业绩评估:")
    if total >= 10000:
        rating = "优秀"
    elif total >= 5000:
        rating = "良好"
    elif total >= 2000:
        rating = "中等"
    else:
        rating = "待提升"
    
    print(f"  今日表现: {rating}")
    
    # 毛利率估算
    estimated_profit = total * 0.5  # 假设50%毛利率
    profit_margin = 50.0
    
    print(f"\n💰 财务估算:")
    print(f"  估算毛利: ¥{estimated_profit:,.2f}")
    print(f"  估算毛利率: {profit_margin:.1f}%")
    
    print(f"\n💡 经营建议:")
    suggestions = [
        "1. 增加畅销商品库存",
        "2. 优化商品陈列",
        "3. 加强客户服务",
        "4. 分析销售时段",
        "5. 制定促销计划"
    ]
    
    for suggestion in suggestions:
        print(f"  {suggestion}")
    
    # 保存演示文件
    report = {
        'demo_date': today,
        'generated_at': datetime.now().isoformat(),
        'sales_data': demo_data,
        'analysis': {
            'total_amount': total,
            'order_count': orders,
            'avg_order_value': total/orders,
            'top_products': products_sorted[:3]
        }
    }
    
    filename = f"quick_demo_{today}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 演示文件已保存: {filename}")
    
    print(f"\n" + "="*80)
    print("🚀 实际使用指南")
    print("="*80)
    
    print(f"""
🎯 你的下一步:

1. 📱 **打开笑铺日记应用**
   查看今日销售报表

2. 📝 **记录关键数据**
   - 销售总额: ______ 元
   - 订单数量: ______ 笔
   - 畅销商品: ______

3. 🔧 **使用分析工具**
   运行: python3 sales_statistics_template.py

4. 📊 **生成分析报告**
   输入数据 → 自动生成报告

💡 **如果没有详细数据:**
   只需告诉我销售总额和订单数，
   我就能提供基础分析。
    """)

if __name__ == "__main__":
    quick_demo()