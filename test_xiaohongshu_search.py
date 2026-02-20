#!/usr/bin/env python3
"""
测试小红书搜索功能
"""

import requests
import json
import time

def test_search():
    """测试搜索功能"""
    mcp_url = "http://localhost:18060/mcp"
    
    print("🔍 测试小红书搜索功能")
    print("="*50)
    
    # 测试1: 检查登录状态
    print("1. 检查登录状态...")
    try:
        response = requests.post(
            mcp_url,
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "check_login_status",
                    "arguments": {}
                },
                "id": 100
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   状态: {result}")
        else:
            print(f"   错误: HTTP {response.status_code}")
    except Exception as e:
        print(f"   异常: {e}")
    
    print()
    
    # 测试2: 搜索热门内容
    test_keywords = [
        "美食",  # 通用热门
        "穿搭",  # 热门分类
        "护肤",  # 热门分类
        "旅游",  # 热门分类
        "学习"   # 热门分类
    ]
    
    for keyword in test_keywords:
        print(f"2. 搜索关键词: '{keyword}'...")
        try:
            response = requests.post(
                mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "search_feeds",
                        "arguments": {
                            "keyword": keyword,
                            "sort": "hot",
                            "page": 1
                        }
                    },
                    "id": 200
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and 'content' in result['result']:
                    feeds = json.loads(result['result']['content'])
                    if isinstance(feeds, list):
                        print(f"   找到 {len(feeds)} 条内容")
                        if feeds:
                            # 显示第一条内容
                            first_feed = feeds[0]
                            title = first_feed.get('title', '无标题')[:50]
                            likes = first_feed.get('likes', 0)
                            print(f"   示例: {title}... (点赞: {likes})")
                    else:
                        print(f"   返回数据格式: {type(feeds)}")
                else:
                    print(f"   响应结构: {result.keys()}")
            else:
                print(f"   错误: HTTP {response.status_code}")
        except Exception as e:
            print(f"   异常: {e}")
        
        # 避免请求过快
        time.sleep(1)
        print()
    
    print("="*50)
    print("✅ 测试完成")

if __name__ == "__main__":
    test_search()