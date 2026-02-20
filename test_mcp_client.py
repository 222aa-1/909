#!/usr/bin/env python3
"""
使用mcp库测试小红书MCP服务器
"""

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    import asyncio
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    print("❌ mcp库未安装，尝试安装...")

async def test_mcp_server():
    """测试MCP服务器"""
    print("🔧 使用MCP客户端测试...")
    
    # 创建HTTP服务器参数
    # 注意：小红书MCP服务器使用HTTP，但mcp库主要支持stdio
    # 我们需要使用requests直接测试
    
    import requests
    import json
    
    url = "http://localhost:18060/mcp"
    
    # 尝试建立SSE连接
    print("尝试SSE连接...")
    try:
        sse_response = requests.get(
            "http://localhost:18060/mcp",
            headers={"Accept": "text/event-stream"},
            stream=True,
            timeout=5
        )
        print(f"SSE响应状态: {sse_response.status_code}")
    except Exception as e:
        print(f"SSE连接失败: {e}")
    
    # 尝试标准的MCP流程
    print("\n尝试标准MCP流程...")
    
    # 1. 初始化
    init_data = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        },
        "id": 1
    }
    
    response = requests.post(url, json=init_data, timeout=10)
    print(f"初始化响应: {response.status_code}")
    if response.status_code == 200:
        print(f"初始化结果: {response.json()}")
    
    # 2. 尝试tools/list
    list_data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    }
    
    response = requests.post(url, json=list_data, timeout=10)
    print(f"\ntools/list响应: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"tools/list结果: {result}")
        
        # 如果有工具，尝试调用
        if 'result' in result and 'tools' in result['result']:
            tools = result['result']['tools']
            print(f"找到 {len(tools)} 个工具")
            
            # 尝试调用第一个工具
            if tools:
                tool = tools[0]
                print(f"\n尝试调用工具: {tool.get('name')}")
                
                call_data = {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": tool['name'],
                        "arguments": {}
                    },
                    "id": 3
                }
                
                response = requests.post(url, json=call_data, timeout=30)
                print(f"工具调用响应: {response.status_code}")
                if response.status_code == 200:
                    print(f"工具调用结果: {response.json()}")

def main():
    """主函数"""
    print("📱 小红书MCP服务器测试")
    print("="*60)
    
    if HAS_MCP:
        asyncio.run(test_mcp_server())
    else:
        # 使用简单的requests测试
        import requests
        import json
        
        url = "http://localhost:18060/mcp"
        
        print("使用简单HTTP测试...")
        
        # 测试ping
        print("\n1. 测试ping...")
        response = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": "ping",
            "params": {},
            "id": 1
        }, timeout=10)
        
        print(f"   Ping响应: {response.status_code}")
        if response.status_code == 200:
            print(f"   Ping结果: {response.json()}")
        
        # 测试直接调用工具（不通过tools/list）
        print("\n2. 直接调用已知工具...")
        
        # 根据文档，工具名可能是：
        # - check_login_status
        # - search_feeds
        # - list_feeds
        # - publish_content
        # - publish_with_video
        # - get_feed_detail
        # - post_comment_to_feed
        # - user_profile
        
        tools_to_test = [
            "check_login_status",
            "list_feeds",
            "search_feeds"
        ]
        
        for tool_name in tools_to_test:
            print(f"\n   测试工具: {tool_name}")
            
            # 构建参数
            arguments = {}
            if tool_name == "search_feeds":
                arguments = {"keyword": "美食", "sort": "hot", "page": 1}
            elif tool_name == "list_feeds":
                arguments = {}
            elif tool_name == "check_login_status":
                arguments = {}
            
            try:
                response = requests.post(url, json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    },
                    "id": 100
                }, timeout=30)
                
                print(f"   响应状态: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"   响应内容: {result}")
                    
                    # 尝试解析内容
                    if 'result' in result and 'content' in result['result']:
                        try:
                            content = json.loads(result['result']['content'])
                            print(f"   解析内容: {type(content)}")
                            if isinstance(content, list):
                                print(f"   找到 {len(content)} 条数据")
                                if content:
                                    print(f"   第一条: {content[0]}")
                        except:
                            print(f"   原始内容: {result['result']['content'][:100]}...")
                
            except Exception as e:
                print(f"   调用异常: {e}")
        
        print("\n" + "="*60)
        print("✅ 测试完成")

if __name__ == "__main__":
    main()