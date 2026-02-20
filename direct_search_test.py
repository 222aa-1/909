#!/usr/bin/env python3
"""
直接测试小红书搜索功能
使用更简单的方法
"""

import requests
import json
import time

def test_direct_search():
    """直接测试搜索"""
    url = "http://localhost:18060/mcp"
    
    print("🔍 直接测试小红书搜索")
    print("="*60)
    
    # 1. 初始化（使用完整的参数）
    print("1. 初始化MCP会话...")
    init_data = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {},
                "logging": {},
                "resources": {}
            },
            "clientInfo": {
                "name": "xiaohongshu-analyzer",
                "version": "1.0.0"
            }
        },
        "id": 1
    }
    
    response = requests.post(url, json=init_data, timeout=10)
    if response.status_code != 200:
        print(f"   初始化失败: {response.status_code}")
        return
    
    init_result = response.json()
    print(f"   初始化成功")
    
    # 2. 等待一下，让服务器处理
    print("2. 等待服务器准备...")
    time.sleep(2)
    
    # 3. 尝试直接调用搜索工具
    print("3. 尝试搜索...")
    
    # 根据文档，工具名是"search_feeds"
    search_data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "search_feeds",
            "arguments": {
                "keyword": "美食",
                "sort": "hot",
                "page": 1
            }
        },
        "id": 2
    }
    
    # 尝试多次，可能有延迟
    for attempt in range(3):
        print(f"   尝试 {attempt + 1}/3...")
        try:
            response = requests.post(url, json=search_data, timeout=30)
            print(f"   响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   响应: {result}")
                
                if 'error' in result:
                    print(f"   错误: {result['error']}")
                elif 'result' in result:
                    print(f"   成功! 找到结果")
                    if 'content' in result['result']:
                        content = result['result']['content']
                        print(f"   内容长度: {len(content)} 字符")
                        print(f"   内容预览: {content[:200]}...")
                        
                        # 尝试解析JSON
                        try:
                            feeds = json.loads(content)
                            if isinstance(feeds, list):
                                print(f"   解析成功! 找到 {len(feeds)} 条内容")
                                for i, feed in enumerate(feeds[:3], 1):
                                    title = feed.get('title', '无标题')[:50]
                                    likes = feed.get('likes', 0)
                                    print(f"     {i}. {title}... (点赞: {likes})")
                                return True
                        except json.JSONDecodeError:
                            print(f"   内容不是JSON: {content[:100]}")
                    break
            else:
                print(f"   HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"   异常: {e}")
        
        time.sleep(2)
    
    print("\n" + "="*60)
    print("❌ 搜索测试失败")
    return False

def test_simple_http():
    """测试简单的HTTP接口（如果存在）"""
    print("\n🔧 测试其他HTTP端点...")
    
    # 尝试常见的端点
    endpoints = [
        "/",
        "/api",
        "/api/search",
        "/search",
        "/feeds",
        "/status"
    ]
    
    base_url = "http://localhost:18060"
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"  {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"    内容: {response.text[:100]}...")
        except:
            print(f"  {endpoint}: 连接失败")

def main():
    """主函数"""
    print("📱 小红书MCP服务器直接测试")
    print("="*60)
    
    # 测试直接搜索
    success = test_direct_search()
    
    if not success:
        # 测试其他HTTP端点
        test_simple_http()
    
    print("\n" + "="*60)
    print("✅ 测试完成")

if __name__ == "__main__":
    main()