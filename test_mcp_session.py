#!/usr/bin/env python3
"""
测试MCP会话
"""

import requests
import json
import time

def create_session():
    """创建MCP会话"""
    url = "http://localhost:18060/mcp"
    
    print("🔧 创建MCP会话...")
    
    # 1. 初始化请求
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
        return None
    
    result = response.json()
    print(f"   初始化成功")
    
    # 获取会话ID
    session_id = response.headers.get('Mcp-Session-Id')
    if session_id:
        print(f"   会话ID: {session_id}")
        return session_id
    else:
        print(f"   未找到会话ID")
        return None

def connect_sse(session_id):
    """连接SSE流"""
    url = "http://localhost:18060/mcp"
    
    print(f"\n🔌 连接SSE流 (会话ID: {session_id})...")
    
    headers = {
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Mcp-Session-Id": session_id
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        print(f"   SSE响应状态: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   SSE连接成功!")
            
            # 读取事件
            print(f"   等待服务器事件...")
            for i, line in enumerate(response.iter_lines()):
                if i >= 10:  # 只读取前10个事件
                    break
                if line:
                    line_str = line.decode('utf-8')
                    print(f"   事件 {i+1}: {line_str}")
                    
                    # 如果是空行，继续
                    if not line_str.strip():
                        continue
                    
                    # 尝试解析JSON
                    if line_str.startswith('data:'):
                        data = line_str[5:].strip()
                        if data:
                            try:
                                event = json.loads(data)
                                print(f"     解析事件: {event}")
                            except:
                                print(f"     原始数据: {data}")
        
        return response
    except Exception as e:
        print(f"   SSE连接失败: {e}")
        return None

def call_tool_with_session(session_id, tool_name, arguments):
    """使用会话调用工具"""
    url = "http://localhost:18060/mcp"
    
    print(f"\n🛠️ 调用工具: {tool_name}")
    
    # 在同一个会话中调用工具
    headers = {
        "Content-Type": "application/json",
        "Mcp-Session-Id": session_id
    }
    
    call_data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 100
    }
    
    try:
        response = requests.post(url, headers=headers, json=call_data, timeout=30)
        print(f"   响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   响应: {result}")
            
            if 'error' in result:
                print(f"   错误: {result['error']}")
            elif 'result' in result:
                print(f"   成功!")
                if 'content' in result['result']:
                    content = result['result']['content']
                    print(f"   内容长度: {len(content)} 字符")
                    
                    # 尝试解析JSON
                    try:
                        data = json.loads(content)
                        if isinstance(data, list):
                            print(f"   找到 {len(data)} 条内容")
                            for i, item in enumerate(data[:3], 1):
                                title = item.get('title', '无标题')[:50]
                                likes = item.get('likes', 0)
                                print(f"     {i}. {title}... (点赞: {likes})")
                        else:
                            print(f"   数据格式: {type(data)}")
                    except:
                        print(f"   内容预览: {content[:200]}...")
        
        return response
    except Exception as e:
        print(f"   调用失败: {e}")
        return None

def main():
    """主函数"""
    print("📱 MCP会话测试")
    print("="*60)
    
    # 创建会话
    session_id = create_session()
    if not session_id:
        print("❌ 无法创建会话")
        return
    
    # 连接SSE（在后台）
    print("\n⚠️ 注意: 需要SSE连接来接收服务器通知")
    print("   但是我们可以尝试直接调用工具...")
    
    # 直接尝试调用工具
    tools_to_test = [
        ("check_login_status", {}),
        ("list_feeds", {}),
        ("search_feeds", {"keyword": "美食", "sort": "hot", "page": 1})
    ]
    
    for tool_name, arguments in tools_to_test:
        call_tool_with_session(session_id, tool_name, arguments)
        time.sleep(2)
    
    print("\n" + "="*60)
    print("✅ 测试完成")
    print("\n💡 提示: 完整的MCP协议需要SSE连接来接收服务器通知")
    print("   你可能需要使用专门的MCP客户端（如Claude Code、Cursor等）")

if __name__ == "__main__":
    main()