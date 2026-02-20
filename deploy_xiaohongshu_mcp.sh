#!/bin/bash

# 小红书MCP服务器部署脚本
# 作者: Clawd
# 时间: 2026-02-18

set -e  # 遇到错误时退出

echo "🚀 小红书MCP服务器部署脚本"
echo "=============================="

# 检查是否在正确目录
cd /Users/imac/.openclaw/workspace/xiaohongshu-mcp

# 1. 检查是否已下载
if [ ! -f "xiaohongshu-mcp-darwin-arm64.tar.gz" ]; then
    echo "📦 下载MCP服务器文件..."
    curl -L -o xiaohongshu-mcp-darwin-arm64.tar.gz "https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-darwin-arm64.tar.gz"
    
    if [ $? -ne 0 ]; then
        echo "❌ 下载失败，请检查网络连接"
        exit 1
    fi
    echo "✅ 下载完成"
else
    echo "📦 文件已存在，跳过下载"
fi

# 2. 解压文件
echo "📂 解压文件..."
tar xzf xiaohongshu-mcp-darwin-arm64.tar.gz

# 3. 检查解压后的文件
if [ ! -f "xiaohongshu-login-darwin-arm64" ] || [ ! -f "xiaohongshu-mcp-darwin-arm64" ]; then
    echo "❌ 解压失败或文件不完整"
    exit 1
fi

# 4. 添加执行权限
echo "🔧 设置执行权限..."
chmod +x xiaohongshu-login-darwin-arm64
chmod +x xiaohongshu-mcp-darwin-arm64

echo "✅ 部署完成！"
echo ""
echo "📋 下一步操作："
echo "1. 运行登录工具: ./xiaohongshu-login-darwin-arm64"
echo "   - 会打开浏览器窗口"
echo "   - 使用小红书账号扫码登录"
echo "   - 登录成功后自动保存cookies"
echo ""
echo "2. 启动MCP服务器: ./xiaohongshu-mcp-darwin-arm64"
echo "   - 默认无头模式运行"
echo "   - 如需调试可加参数: -headless=false"
echo ""
echo "3. 服务器运行在: http://localhost:18060/mcp"
echo ""
echo "4. 测试连接:"
echo "   curl -X POST http://localhost:18060/mcp \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\",\"params\":{},\"id\":1}'"
echo ""
echo "🎯 完成后即可搜索小红书近15天爆款文案！"