#!/usr/bin/env python3
"""
笑铺日记销售数据演示分析
使用模拟数据展示分析能力
"""

from datetime import datetime, date
import json

class DemoSalesAnalysis:
    def __init__(self):
        self.today = date.today().strftime("%Y-%m-%d")
        
    def generate_demo_data(self):
        """生成演示数据"""
        print("="*80)
        print("📊 笑铺日记销售数据演示分析")
        print("="*80)
        print(f"📅 演示日期: {self.today}")
        print("="*80)
        
        # 模拟今日销售数据
        demo_data = {
            'date': self.today,
            'total_amount': 8560.50,  # 销售总额
            'order_count': 32,        # 订单数量
            'customer_count': 28,     # 客户数量
            
            'products': [
                {'name': '灰色字母加绒卫衣', 'quantity': 8, 'amount': 1272.00, 'price': 159.00},
                {'name': '北面羽绒裤', 'quantity': 5, 'amount': 1345.00, 'price': 269.00},
                {'name': '预订小衫', 'quantity': 12, 'amount': 828.00, 'price': 69.00},
                {'name': '紫色加绒连帽卫衣', 'quantity': 6, 'amount': 1194.00, 'price': 199.00},
                {'name': '防风裤时尚松紧', 'quantity': 4, 'amount': 716.00, 'price': 179.00},
                {'name': '条纹毛衣', 'quantity': 3, 'amount': 597.00, 'price': 199.00},
                {'name': '翻领卫衣', 'quantity': 7, 'amount': 1043.00, 'price': 149.00},
                {'name': '打底针织衫', 'quantity': 10, 'amount': 990.00, 'price': 99.00},
                {'name': '卫衣', 'quantity': 2, 'amount': 478.00, 'price': 239.00},
                {'name': '9036防风裤', 'quantity': 3, 'amount': 537.00, 'price': 179.00},
            ],
            
            'payment_methods': {
                '微信支付': 5120.30,
                '支付宝': 2840.20,
                '现金': 450.00,
                '银行卡': 150.00
            },
            
            'time_slots': {
                '上午(9-12)': 1850.00,
                '中午(12-14)': 2560.50,
                '下午(14-17)': 2850.00,
                '晚上(17-21)': 1300.00
            },
            
            'customer_types': {
                '新客户': 12,
                '老客户': 16
            }
        }
        
        return demo_data
    
    def analyze_demo_data(self, data):
        """分析演示数据"""
        print(f"\n📈 销售数据分析报告")
        print("="*80)
        
        # 基础统计
        total_amount = data['total_amount']
        order_count = data['order_count']
        customer_count = data['customer_count']
        
        print(f"\n📊 基础销售统计:")
        print(f"  销售总额: ¥{total_amount:,.2f}")
        print(f"  订单数量: {order_count} 笔")
        print(f"  客户数量: {customer_count} 人")
        
        avg_order_value = total_amount / order_count
        avg_customer_value = total_amount / customer_count
        
        print(f"  平均客单价: ¥{avg_order_value:,.2f}")
        print(f"  人均消费: ¥{avg_customer_value:,.2f}")
        
        # 商品分析
        products = data['products']
        print(f"\n📦 商品销售分析:")
        print(f"  销售商品种类: {len(products)} 种")
        
        total_quantity = sum(p['quantity'] for p in products)
        total_product_amount = sum(p['amount'] for p in products)
        
        print(f"  总销售数量: {total_quantity} 件")
        print(f"  商品销售总额: ¥{total_product_amount:,.2f}")
        
        # 畅销商品排名
        products_sorted = sorted(products, key=lambda x: x['amount'], reverse=True)
        
        print(f"\n  🏆 畅销商品TOP 5:")
        for i, product in enumerate(products_sorted[:5], 1):
            percentage = (product['amount'] / total_product_amount * 100)
            print(f"    {i}. {product['name']}: {product['quantity']}件, ¥{product['amount']:,.2f} ({percentage:.1f}%)")
        
        # 支付方式分析
        payment_methods = data['payment_methods']
        print(f"\n💳 支付方式分析:")
        total_payment = sum(payment_methods.values())
        
        for method, amount in sorted(payment_methods.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_payment * 100)
            print(f"  {method}: ¥{amount:,.2f} ({percentage:.1f}%)")
        
        # 时间段分析
        time_slots = data['time_slots']
        print(f"\n⏰ 销售时间段分析:")
        total_time_amount = sum(time_slots.values())
        
        for slot, amount in sorted(time_slots.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_time_amount * 100)
            print(f"  {slot}: ¥{amount:,.2f} ({percentage:.1f}%)")
        
        # 客户分析
        customer_types = data['customer_types']
        print(f"\n👥 客户类型分析:")
        total_customers = sum(customer_types.values())
        
        for ctype, count in customer_types.items():
            percentage = (count / total_customers * 100)
            print(f"  {ctype}: {count}人 ({percentage:.1f}%)")
        
        # 业绩评估
        print(f"\n🎯 今日业绩评估:")
        
        if total_amount >= 10000:
            rating = "优秀"
            suggestion = "表现非常出色，考虑扩大经营规模"
        elif total_amount >= 5000:
            rating = "良好"
            suggestion = "表现不错，继续保持并优化"
        elif total_amount >= 2000:
            rating = "中等"
            suggestion = "有提升空间，建议加强促销"
        else:
            rating = "待提升"
            suggestion = "需要加强营销和客户服务"
        
        print(f"  评级: {rating}")
        print(f"  建议: {suggestion}")
        
        # 毛利率估算
        print(f"\n💰 毛利率估算:")
        
        # 简单估算：假设平均毛利率为50%
        estimated_cost = total_amount * 0.5
        estimated_profit = total_amount - estimated_cost
        profit_margin = (estimated_profit / total_amount) * 100
        
        print(f"  估算成本: ¥{estimated_cost:,.2f}")
        print(f"  估算毛利: ¥{estimated_profit:,.2f}")
        print(f"  估算毛利率: {profit_margin:.1f}%")
        
        # 经营建议
        print(f"\n💡 经营优化建议:")
        
        suggestions = [
            "1. 增加'灰色字母加绒卫衣'库存，这是最畅销商品",
            "2. 在中午时段(12-14点)增加促销活动",
            "3. 推广微信支付，提供小额优惠",
            "4. 维护老客户，推出会员专属优惠",
            "5. 优化商品陈列，突出畅销商品"
        ]
        
        for suggestion in suggestions:
            print(f"  {suggestion}")
        
        # 明日预测
        print(f"\n🔮 明日销售预测:")
        
        # 简单预测：基于今日数据和趋势
        predicted_amount = total_amount * 1.1  # 增长10%
        predicted_orders = order_count * 1.05  # 增长5%
        
        print(f"  预测销售额: ¥{predicted_amount:,.2f} (+10%)")
        print(f"  预测订单数: {int(predicted_orders)} 笔 (+5%)")
        print(f"  建议备货量: {int(total_quantity * 1.15)} 件")
        
        return data
    
    def save_demo_report(self, data):
        """保存演示报告"""
        report = {
            'report_date': self.today,
            'generated_at': datetime.now().isoformat(),
            'data_type': 'demo_analysis',
            'sales_data': data,
            'summary': self.generate_summary(data)
        }
        
        filename = f"shopdiary_demo_report_{self.today}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 演示报告已保存: {filename}")
        
        # 同时生成文本报告
        text_filename = f"shopdiary_demo_report_{self.today}.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_text_report(data))
        
        print(f"📄 文本报告已保存: {text_filename}")
    
    def generate_summary(self, data):
        """生成摘要"""
        total = data['total_amount']
        orders = data['order_count']
        avg = total / orders if orders > 0 else 0
        
        return f"{self.today} 演示分析: 销售¥{total:,.2f}, 订单{orders}笔, 均客¥{avg:,.2f}"
    
    def generate_text_report(self, data):
        """生成文本报告"""
        report = f"""笑铺日记销售分析报告
报告日期: {self.today}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

📊 销售概况
销售总额: ¥{data['total_amount']:,.2f}
订单数量: {data['order_count']} 笔
客户数量: {data['customer_count']} 人
平均客单价: ¥{data['total_amount']/data['order_count']:,.2f}

📦 商品销售TOP 5
"""
        
        products = sorted(data['products'], key=lambda x: x['amount'], reverse=True)
        for i, product in enumerate(products[:5], 1):
            report += f"{i}. {product['name']}: {product['quantity']}件, ¥{product['amount']:,.2f}\n"
        
        report += f"""
💳 支付方式
"""
        for method, amount in sorted(data['payment_methods'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / sum(data['payment_methods'].values()) * 100)
            report += f"{method}: ¥{amount:,.2f} ({percentage:.1f}%)\n"
        
        report += f"""
⏰ 销售时段
"""
        for slot, amount in sorted(data['time_slots'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / sum(data['time_slots'].values()) * 100)
            report += f"{slot}: ¥{amount:,.2f} ({percentage:.1f}%)\n"
        
        report += f"""
💡 经营建议
1. 重点补货畅销商品
2. 优化中午时段促销
3. 加强微信支付推广
4. 维护老客户关系
5. 提升商品陈列效果
"""
        return report
    
    def run_interactive_demo(self):
        """运行交互式演示"""
        print("\n" + "="*80)
        print("🔄 交互式演示模式")
        print("="*80)
        
        print("\n请输入模拟数据:")
        
        # 获取用户输入
        try:
            total = float(input("💰 今日销售总额 (元): ") or "8560.50")
            orders = int(input("📦 订单数量 (笔): ") or "32")
            customers = int(input("👥 客户数量 (人): ") or "28")
            
            print("\n📦 商品销售 (输入3个商品):")
            products = []
            for i in range(3):
                name = input(f"商品{i+1}名称: ") or f"示例商品{i+1}"
                qty = int(input(f"  销售数量: ") or "5")
                price = float(input(f"  单价 (元): ") or "100")
                amount = qty * price
                products.append({'name': name, 'quantity': qty, 'amount': amount, 'price': price})
            
            # 创建模拟数据
            demo_data = {
                'date': self.today,
                'total_amount': total,
                'order_count': orders,
                'customer_count': customers,
                'products': products,
                'payment_methods': {'微信支付': total*0.6, '支付宝': total*0.3, '现金': total*0.1},
                'time_slots': {'上午': total*0.3, '中午': total*0.4, '下午': total*0.3}
            }
            
            # 分析数据
            self.analyze_demo_data(demo_data)
            
            # 保存报告
            self.save_demo_report(demo_data)
            
        except Exception as e:
            print(f"❌ 输入错误: {e}")
            print("使用默认演示数据...")
            demo_data = self.generate_demo_data()
            self.analyze_demo_data(demo_data)
            self.save_demo_report(demo_data)

def main():
    """主函数"""
    print("🛍️ 笑铺日记销售分析演示系统")
    print("="*60)
    
    print("\n选择演示模式:")
    print("1. 完整演示 (使用模拟数据)")
    print("2. 交互式演示 (自定义数据)")
    print("3. 快速演示 (只看结果)")
    
    choice = input("\n请选择 (1/2/3): ") or "1"
    
    demo = DemoSalesAnalysis()
    
    if choice == '1':
        print("\n运行完整演示...")
        data = demo.generate_demo_data()
        demo.analyze_demo_data(data)
        demo.save_demo_report(data)
    elif choice == '2':
        demo.run_interactive_demo()
    else:
        print("\n运行快速演示...")
        data = demo.generate_demo_data()
        demo.analyze_demo_data(data)
    
    print(f"\n" + "="*80)
    print("🎯 演示完成!")
    print("="*80)
    print(f"""
💡 实际使用步骤:
1. 打开笑铺日记查看今日销售
2. 记录关键数据
3. 运行销售统计模板
4. 输入数据生成报告

📁 已生成文件:
  - shopdiary_demo_report_{demo.today}.json
  - shopdiary_demo_report_{demo.today}.txt

🚀 现在你可以:
1. 查看生成的报告了解分析格式
2. 收集实际销售数据
3. 使用相同模板进行分析
    """)

if __name__ == "__main__":
    main()