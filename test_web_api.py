#!/usr/bin/env python3
"""
测试Web API是否正常工作
"""

import requests
import json

def test_api():
    """测试API"""
    base_url = "http://localhost:9988"
    
    print("🧪 测试股票分析Web API...")
    print("=" * 50)
    
    # 测试1: 分析AAPL
    print("\n1. 测试分析AAPL股票:")
    try:
        response = requests.post(
            f"{base_url}/api/analyze",
            json={"symbol": "AAPL", "period": "1mo"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 成功! 状态码: {response.status_code}")
            print(f"   当前价格: ${data['analysis']['current_price']:.2f}")
            print(f"   价格变化: {data['analysis']['price_change_pct']:.2f}%")
            print(f"   RSI状态: {data['analysis']['rsi_level']}")
        else:
            print(f"   ❌ 失败! 状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 测试2: 测试错误处理
    print("\n2. 测试错误处理（空股票代码）:")
    try:
        response = requests.post(
            f"{base_url}/api/analyze",
            json={"symbol": "", "period": "1mo"},
            timeout=10
        )
        
        if response.status_code == 400:
            print(f"   ✅ 正确返回错误! 状态码: {response.status_code}")
            print(f"   错误信息: {response.json().get('error', '未知错误')}")
        else:
            print(f"   ⚠️  预期400错误，但收到: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 测试3: 获取股票列表
    print("\n3. 测试获取股票列表:")
    try:
        response = requests.get(f"{base_url}/api/stocks", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 成功! 状态码: {response.status_code}")
            print(f"   可用股票数量: {len(data.get('stocks', []))}")
            print("   热门股票:")
            for stock in data.get('stocks', [])[:5]:
                print(f"     - {stock['symbol']} ({stock['name']})")
        else:
            print(f"   ❌ 失败! 状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 测试4: 测试热门股票
    print("\n4. 测试热门股票分析:")
    try:
        response = requests.get(f"{base_url}/api/trending", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 成功! 状态码: {response.status_code}")
            print(f"   热门股票数量: {len(data.get('trending', []))}")
            for stock in data.get('trending', []):
                trend = "📈" if stock['trend'] == '上涨' else "📉"
                print(f"     {trend} {stock['symbol']}: ${stock['current_price']:.2f} ({stock['price_change_pct']:.2f}%)")
        else:
            print(f"   ❌ 失败! 状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    print("\n" + "=" * 50)
    print("🌐 Web界面地址: http://localhost:9988")
    print("💡 打开浏览器访问以上地址使用完整功能")

if __name__ == "__main__":
    test_api()