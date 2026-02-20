#!/usr/bin/env python3
"""
按照MCP协议正确流程测试
"""

import requests
import json
import time

class MCPClient:
    def __init__(self, url="http://localhost:18060/mcp"):
        self.url = url
        self.session = None
        
    def initialize(self):
        """初始化MCP会话"""
        print("1. 初始化MCP会话...")
        response = requests.post(
            self.url,
            json={
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {},
                "id": 1
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   初始化成功: {result.get('result', {}).get('serverInfo', {}).get('name')}")
            return True
        else:
            print(f"   初始化失败: HTTP {response.status_code}")
            return False
    
    def list_tools(self):
        """列出可用工具"""
        print("2. 列出可用工具...")
        response = requests.post(
            self.url,
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 2
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            tools = result.get('result', {}).get('tools', [])
            print(f"   找到 {len(tools)} 个工具:")
            for tool in tools:
                print(f"     - {tool.get('name')}: {tool.get('description', '')[:50]}...")
            return tools
        else:
            print(f"   列出工具失败: HTTP {response.status_code}")
            return []
    
    def call_tool(self, name, arguments):
        """调用工具"""
        print(f"3. 调用工具: {name}...")
        response = requests.post(
            self.url,
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": arguments
                },
                "id": 3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print(f"   工具调用错误: {result['error']}")
                return None
            else:
                print(f"   工具调用成功")
                return result.get('result', {})
        else:
            print(f"   工具调用失败: HTTP {response.status_code}")
            return None
    
    def test_search(self):
        """测试搜索功能"""
        print("\n🔍 测试小红书搜索功能")
        print("="*50)
        
        # 初始化
        if not self.initialize():
            return
        
        # 列出工具
        tools = self.list_tools()
        if not tools:
            return
        
        # 查找搜索工具
        search_tool = None
        for tool in tools:
            if 'search' in tool.get('name', '').lower():
                search_tool = tool
                break
        
        if not search_tool:
            print("❌ 未找到搜索工具")
            return
        
        print(f"\n🎯 使用工具: {search_tool.get('name')}")
        
        # 测试搜索
        test_cases = [
            {"keyword": "美食推荐", "sort": "hot", "page": 1},
            {"keyword": "春季穿搭", "sort": "hot", "page": 1},
            {"keyword": "护肤心得", "sort": "hot", "page": 1},
        ]
        
        for i, params in enumerate(test_cases, 1):
            print(f"\n📝 测试搜索 {i}: {params['keyword']}")
            result = self.call_tool(search_tool['name'], params)
            
            if result and 'content' in result:
                try:
                    feeds = json.loads(result['content'])
                    if isinstance(feeds, list):
                        print(f"   找到 {len(feeds)} 条内容")
                        if feeds:
                            # 显示前3条
                            for j, feed in enumerate(feeds[:3], 1):
                                title = feed.get('title', '无标题')[:40]
                                likes = feed.get('likes', 0)
                                print(f"   {j}. {title}... (点赞: {likes})")
                    else:
                        print(f"   返回数据: {type(feeds)}")
                except Exception as e:
                    print(f"   解析错误: {e}")
            
            # 避免请求过快
            time.sleep(2)
        
        print("\n" + "="*50)
        print("✅ 搜索测试完成")

def main():
    """主函数"""
    client = MCPClient()
    client.test_search()

if __name__ == "__main__":
    main()