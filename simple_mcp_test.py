#!/usr/bin/env python3
"""
简单的MCP协议测试
直接测试小红书MCP服务器的工具
"""

import requests
import json

def test_xiaohongshu_mcp():
    """测试小红书MCP服务器"""
    url = "http://localhost:18060/mcp"
    
    print("🔧 测试小红书MCP服务器")
    print("="*60)
    
    # 1. 初始化
    print("1. 初始化会话...")
    init_response = requests.post(url, json={
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {},
        "id": 1
    }, timeout=10)
    
    if init_response.status_code != 200:
        print(f"   初始化失败: HTTP {init_response.status_code}")
        return
    
    init_result = init_response.json()
    print(f"   初始化成功: {init_result.get('result', {}).get('serverInfo', {}).get('name')}")
    
    # 2. 直接测试工具（不通过tools/list）
    print("\n2. 直接测试工具调用...")
    
    # 测试检查登录状态
    print("   a) 检查登录状态...")
    login_response = requests.post(url, json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "check_login_status",
            "arguments": {}
        },
        "id": 2
    }, timeout=10)
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        print(f"      响应: {login_result}")
    else:
        print(f"      失败: HTTP {login_response.status_code}")
    
    # 测试搜索功能
    print("\n   b) 测试搜索功能...")
    search_response = requests.post(url, json={
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
        "id": 3
    }, timeout=30)
    
    if search_response.status_code == 200:
        search_result = search_response.json()
        print(f"      响应状态: 成功")
        
        if 'result' in search_result and 'content' in search_result['result']:
            try:
                feeds = json.loads(search_result['result']['content'])
                if isinstance(feeds, list):
                    print(f"      找到 {len(feeds)} 条内容")
                    if feeds:
                        for i, feed in enumerate(feeds[:3], 1):
                            title = feed.get('title', '无标题')[:40]
                            likes = feed.get('likes', 0)
                            print(f"      {i}. {title}... (点赞: {likes})")
                else:
                    print(f"      返回数据格式: {type(feeds)}")
            except Exception as e:
                print(f"      解析错误: {e}")
        else:
            print(f"      响应结构: {search_result.keys()}")
    else:
        print(f"      失败: HTTP {search_response.status_code}")
    
    # 测试获取推荐列表
    print("\n   c) 测试获取推荐列表...")
    feeds_response = requests.post(url, json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "list_feeds",
            "arguments": {}
        },
        "id": 4
    }, timeout=30)
    
    if feeds_response.status_code == 200:
        feeds_result = feeds_response.json()
        print(f"      响应状态: 成功")
        
        if 'result' in feeds_result and 'content' in feeds_result['result']:
            try:
                feeds = json.loads(feeds_result['result']['content'])
                if isinstance(feeds, list):
                    print(f"      找到 {len(feeds)} 条推荐内容")
                    if feeds:
                        for i, feed in enumerate(feeds[:3], 1):
                            title = feed.get('title', '无标题')[:40]
                            likes = feed.get('likes', 0)
                            print(f"      {i}. {title}... (点赞: {likes})")
                else:
                    print(f"      返回数据格式: {type(feeds)}")
            except Exception as e:
                print(f"      解析错误: {e}")
        else:
            print(f"      响应结构: {feeds_result.keys()}")
    else:
        print(f"      失败: HTTP {feeds_response.status_code}")
    
    print("\n" + "="*60)
    print("✅ 测试完成")

if __name__ == "__main__":
    test_xiaohongshu_mcp()