#!/usr/bin/env python3
"""
测试SSE连接
"""

import requests
import json

def test_sse_connection():
    """测试SSE连接"""
    url = "http://localhost:18060/mcp"
    
    print("🔌 测试SSE连接...")
    
    # 尝试建立SSE连接
    headers = {
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        print(f"SSE响应状态: {response.status_code}")
        print(f"SSE响应头: {response.headers}")
        
        # 读取一些事件
        for i, line in enumerate(response.iter_lines()):
            if i >= 5:  # 只读取前5行
                break
            if line:
                print(f"事件 {i+1}: {line.decode('utf-8')}")
                
    except Exception as e:
        print(f"SSE连接失败: {e}")
    
    print("\n尝试POST到SSE端点...")
    
    # 尝试发送POST请求到SSE端点
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "sse-test", "version": "1.0.0"}
                },
                "id": 1
            },
            stream=True,
            timeout=10
        )
        
        print(f"POST SSE响应状态: {response.status_code}")
        print(f"响应头: {response.headers}")
        
        # 尝试读取响应
        content = response.content.decode('utf-8')
        print(f"响应内容: {content[:200]}...")
        
    except Exception as e:
        print(f"POST SSE失败: {e}")

def test_websocket():
    """测试WebSocket连接"""
    print("\n🔌 测试WebSocket连接...")
    
    # 尝试WebSocket端点
    ws_urls = [
        "ws://localhost:18060/mcp",
        "ws://localhost:18060/ws",
        "ws://localhost:18060/socket"
    ]
    
    for ws_url in ws_urls:
        print(f"尝试 {ws_url}...")
        # 这里需要websocket库，我们只检查端点是否存在
        try:
            response = requests.get(ws_url.replace("ws://", "http://"), timeout=5)
            print(f"  HTTP响应: {response.status_code}")
        except:
            print(f"  连接失败")

def main():
    """主函数"""
    print("📡 测试MCP服务器连接方式")
    print("="*60)
    
    test_sse_connection()
    test_websocket()
    
    print("\n" + "="*60)
    print("✅ 测试完成")

if __name__ == "__main__":
    main()