#!/usr/bin/env python3
"""
笑铺日记销售统计模板
输入销售数据，自动生成统计报告
"""

from datetime import datetime, date
import json

class SalesStatistics:
    def __init__(self):
        self.today = date.today().strftime("%Y-%m-%d")
        self.sales_data = {}
        
    def input_sales_data(self):
        """输入销售数据"""
        print("="*80)
        print("📊 笑铺日记销售数据输入")
        print("="*80)
        print(f"日期: {self.today}")
        print("="*80)
        
        print("\n请输入今日销售数据:")
        print("(如果不知道具体数据，可以留空或输入0)")
        
        # 基础销售数据
        self.sales_data['total_amount'] = float(input("💰 今日销售总额 (元): ") or "0")
        self.sales_data['order_count'] = int(input("📦 订单数量 (笔): ") or "0")
        self.sales_data['customer_count'] = int(input("👥 客户数量 (人): ") or "0")
        
        # 商品销售明细
        print("\n📦 商品销售明细 (可选):")
        print("(输入商品信息，输入'完成'结束)")
        
        products = []
        while True:
            product_name = input("商品名称 (输入'完成'结束): ")
            if product_name.lower() == '完成':
                break
            
            quantity = int(input(f"  {product_name} 销售数量: ") or "0")
            amount = float(input(f"  {product_name} 销售金额 (元): ") or "0")
            price = float(input(f"  {product_name} 单价 (元): ") or "0")
            
            products.append({
                'name': product_name,
                'quantity': quantity,
                'amount': amount,
                'price': price,
                'profit_margin': self.calculate_profit_margin(price)
            })
        
        self.sales_data['products'] = products
        
        # 支付方式
        print("\n💳 支付方式统计 (可选):")
        payment_methods = {}
        
        methods = ['现金', '微信', '支付宝', '银行卡', '其他']
        for method in methods:
            amount = input(f"  {method}支付金额 (元): ")
            if amount:
                payment_methods[method] = float(amount)
        
        self.sales_data['payment_methods'] = payment_methods
        
        # 时间段
        print("\n⏰ 销售时间段 (可选):")
        time_slots = {}
        
        slots = ['上午(9-12)', '中午(12-14)', '下午(14-17)', '晚上(17-21)', '深夜(21-24)']
        for slot in slots:
            amount = input(f"  {slot}销售金额 (元): ")
            if amount:
                time_slots[slot] = float(amount)
        
        self.sales_data['time_slots'] = time_slots
        
        return self.sales_data
    
    def calculate_profit_margin(self, sale_price, cost_price=None):
        """计算毛利率"""
        if cost_price is None:
            # 如果没有成本价，使用估算
            if sale_price < 50:
                cost_price = sale_price * 0.4  # 60%毛利率
            elif sale_price < 200:
                cost_price = sale_price * 0.5  # 50%毛利率
            else:
                cost_price = sale_price * 0.6  # 40%毛利率
        
        if cost_price > 0:
            return ((sale_price - cost_price) / sale_price) * 100
        return 0
    
    def generate_report(self):
        """生成统计报告"""
        if not self.sales_data:
            print("❌ 没有销售数据")
            return
        
        print("\n" + "="*80)
        print("📈 笑铺日记销售统计报告")
        print("="*80)
        print(f"报告日期: {self.today}")
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # 基础统计
        total_amount = self.sales_data['total_amount']
        order_count = self.sales_data['order_count']
        customer_count = self.sales_data['customer_count']
        
        print(f"\n📊 基础销售统计:")
        print(f"  销售总额: ¥{total_amount:,.2f}")
        print(f"  订单数量: {order_count} 笔")
        print(f"  客户数量: {customer_count} 人")
        
        if order_count > 0:
            avg_order_value = total_amount / order_count
            print(f"  平均客单价: ¥{avg_order_value:,.2f}")
        
        if customer_count > 0:
            avg_customer_value = total_amount / customer_count
            print(f"  人均消费: ¥{avg_customer_value:,.2f}")
        
        # 商品分析
        products = self.sales_data.get('products', [])
        if products:
            print(f"\n📦 商品销售分析:")
            print(f"  销售商品种类: {len(products)} 种")
            
            # 按金额排序
            products_sorted = sorted(products, key=lambda x: x['amount'], reverse=True)
            
            total_quantity = sum(p['quantity'] for p in products)
            total_product_amount = sum(p['amount'] for p in products)
            
            print(f"  总销售数量: {total_quantity} 件")
            print(f"  商品销售总额: ¥{total_product_amount:,.2f}")
            
            print(f"\n  🏆 畅销商品TOP 5:")
            for i, product in enumerate(products_sorted[:5], 1):
                print(f"    {i}. {product['name']}: {product['quantity']}件, ¥{product['amount']:,.2f}, 毛利率{product.get('profit_margin', 0):.1f}%")
        
        # 支付方式分析
        payment_methods = self.sales_data.get('payment_methods', {})
        if payment_methods:
            print(f"\n💳 支付方式分析:")
            total_payment = sum(payment_methods.values())
            
            for method, amount in sorted(payment_methods.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_payment * 100) if total_payment > 0 else 0
                print(f"  {method}: ¥{amount:,.2f} ({percentage:.1f}%)")
        
        # 时间段分析
        time_slots = self.sales_data.get('time_slots', {})
        if time_slots:
            print(f"\n⏰ 销售时间段分析:")
            total_time_amount = sum(time_slots.values())
            
            for slot, amount in sorted(time_slots.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_time_amount * 100) if total_time_amount > 0 else 0
                print(f"  {slot}: ¥{amount:,.2f} ({percentage:.1f}%)")
        
        # 业绩评估
        print(f"\n🎯 今日业绩评估:")
        
        if total_amount == 0:
            print("  今日无销售记录")
        elif total_amount < 1000:
            print("  销售业绩: 较低 (建议加强促销)")
            print("  建议: 推出特价商品，增加客户引流")
        elif total_amount < 5000:
            print("  销售业绩: 中等 (保持稳定)")
            print("  建议: 优化商品组合，提升客单价")
        elif total_amount < 10000:
            print("  销售业绩: 良好 (表现不错)")
            print("  建议: 维护老客户，开发新客户")
        else:
            print("  销售业绩: 优秀 (非常出色)")
            print("  建议: 扩大规模，考虑分店")
        
        # 明日建议
        print(f"\n💡 明日经营建议:")
        
        suggestions = [
            "1. 检查库存，补充畅销商品",
            "2. 分析客户偏好，优化商品陈列",
            "3. 准备促销活动，提升客流量",
            "4. 整理客户信息，进行回访",
            "5. 总结今日经验，优化服务流程"
        ]
        
        for suggestion in suggestions:
            print(f"  {suggestion}")
        
        # 保存报告
        self.save_report()
    
    def save_report(self):
        """保存报告到文件"""
        report = {
            'date': self.today,
            'generated_at': datetime.now().isoformat(),
            'sales_data': self.sales_data,
            'summary': self.generate_summary_text()
        }
        
        filename = f"shopdiary_sales_report_{self.today}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 报告已保存: {filename}")
    
    def generate_summary_text(self):
        """生成摘要文本"""
        total = self.sales_data.get('total_amount', 0)
        orders = self.sales_data.get('order_count', 0)
        
        if total == 0:
            return f"{self.today} 无销售记录"
        else:
            avg = total / orders if orders > 0 else 0
            return f"{self.today} 销售: ¥{total:,.2f}, 订单: {orders}笔, 均客: ¥{avg:,.2f}"
    
    def quick_analysis(self, total_amount, order_count):
        """快速分析（只需两个数据）"""
        print("\n" + "="*80)
        print("⚡ 快速销售分析")
        print("="*80)
        
        print(f"📅 日期: {self.today}")
        print(f"💰 销售总额: ¥{total_amount:,.2f}")
        print(f"📦 订单数量: {order_count} 笔")
        
        if order_count > 0:
            avg_order = total_amount / order_count
            print(f"📊 平均客单价: ¥{avg_order:,.2f}")
            
            # 简单评估
            if avg_order < 100:
                print(f"🎯 客单价较低，建议:")
                print(f"   - 推荐搭配销售")
                print(f"   - 设置满减优惠")
                print(f"   - 推出套餐组合")
            elif avg_order < 300:
                print(f"🎯 客单价适中，建议:")
                print(f"   - 维护现有客户")
                print(f"   - 优化商品结构")
                print(f"   - 提升服务质量")
            else:
                print(f"🎯 客单价较高，建议:")
                print(f"   - 开发高端客户")
                print(f"   - 提供增值服务")
                print(f"   - 建立会员体系")
        
        print(f"\n💡 经营建议:")
        print(f"  1. 记录每日销售数据")
        print(f"  2. 分析销售趋势")
        print(f"  3. 优化库存管理")
        print(f"  4. 提升客户体验")

def main():
    """主函数"""
    print("🛍️ 笑铺日记销售统计系统")
    print("="*60)
    
    print("\n选择分析模式:")
    print("1. 完整数据输入 (推荐)")
    print("2. 快速分析 (只需总额和订单数)")
    print("3. 查看使用说明")
    
    choice = input("\n请选择 (1/2/3): ")
    
    stats = SalesStatistics()
    
    if choice == '1':
        stats.input_sales_data()
        stats.generate_report()
    elif choice == '2':
        total = float(input("💰 请输入今日销售总额 (元): ") or "0")
        orders = int(input("📦 请输入订单数量 (笔): ") or "0")
        stats.quick_analysis(total, orders)
    else:
        print(f"""
使用说明:

📋 **完整数据输入**:
   适合有详细销售数据的情况
   可以分析商品、支付方式、时间段等

⚡ **快速分析**:
   只需销售总额和订单数
   适合快速查看基本情况

📊 **输出内容**:
   - 基础销售统计
   - 业绩评估
   - 经营建议
   - 自动保存报告

🎯 **建议**:
   1. 每日记录销售数据
   2. 使用本工具定期分析
   3. 根据建议优化经营
        """)

if __name__ == "__main__":
    main()