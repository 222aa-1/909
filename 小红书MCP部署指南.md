# 小红书MCP服务器部署指南

## 🎯 目标
部署小红书MCP服务器，用于搜索近15天的爆款文案并总结关键词。

## 📦 部署方式选择

### 方案一：预编译二进制文件（推荐）
**适合**: macOS用户，无需安装Docker

### 方案二：Docker容器
**适合**: 有Docker环境的用户

### 方案三：源码编译
**适合**: 开发者，需要自定义功能

## 🔧 方案一：预编译二进制文件部署步骤

### 1. 下载文件
```bash
# 进入工作目录
cd /Users/imac/.openclaw/workspace/xiaohongshu-mcp

# 下载最新版本（macOS Apple Silicon）
curl -L -o xiaohongshu-mcp-darwin-arm64.tar.gz "https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-darwin-arm64.tar.gz"
```

### 2. 解压文件
```bash
# 解压压缩包
tar xzf xiaohongshu-mcp-darwin-arm64.tar.gz

# 查看解压后的文件
ls -la
```

### 3. 运行登录工具
```bash
# 给文件添加执行权限
chmod +x xiaohongshu-login-darwin-arm64

# 运行登录工具
./xiaohongshu-login-darwin-arm64
```

**登录步骤**:
1. 程序会打开浏览器窗口
2. 使用小红书账号扫码登录
3. 登录成功后自动保存cookies
4. 关闭浏览器窗口

### 4. 启动MCP服务器
```bash
# 给MCP服务器添加执行权限
chmod +x xiaohongshu-mcp-darwin-arm64

# 启动服务器（无头模式）
./xiaohongshu-mcp-darwin-arm64

# 或者启动有界面模式（便于调试）
./xiaohongshu-mcp-darwin-arm64 -headless=false
```

### 5. 验证服务
```bash
# 测试MCP连接
curl -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{},"id":1}'
```

## 🐳 方案二：Docker部署（如果已安装Docker）

### 1. 拉取镜像
```bash
docker pull xpzouying/xiaohongshu-mcp
```

### 2. 创建docker-compose.yml
```yaml
version: '3.8'
services:
  xiaohongshu-mcp:
    image: xpzouying/xiaohongshu-mcp:latest
    container_name: xiaohongshu-mcp
    ports:
      - "18060:18060"
    volumes:
      - ./data:/app/data
      - ./images:/app/images
    restart: unless-stopped
```

### 3. 启动服务
```bash
docker-compose up -d
```

## 🔍 MCP工具功能

### 可用工具列表
1. **check_login_status** - 检查登录状态
2. **search_feeds** - 搜索小红书内容（关键功能）
3. **list_feeds** - 获取首页推荐列表
4. **get_feed_detail** - 获取帖子详情
5. **publish_content** - 发布图文内容
6. **publish_with_video** - 发布视频内容
7. **post_comment_to_feed** - 发表评论
8. **user_profile** - 获取用户主页

### 搜索功能参数
```json
{
  "keyword": "爆款文案",
  "sort": "hot",  // hot:热门, time:最新
  "page": 1
}
```

## 📊 小红书爆款文案分析流程

### 1. 搜索近15天爆款内容
```bash
# 使用MCP搜索工具
搜索关键词: "爆款"、"热门"、"种草"
时间范围: 近15天
排序方式: 按点赞数降序
```

### 2. 数据收集策略
- **分类搜索**: 美妆、穿搭、美食、家居、学习
- **热门标签**: #爆款 #热门 #种草 #必看
- **筛选标准**: 点赞>10000，收藏>5000

### 3. 关键词提取方法
```python
# 关键词分类
情感共鸣: 破防了、泪目、谁懂啊
实用价值: 保姆级、手把手、避坑指南
视觉吸引: 绝美、神仙颜值、氛围感
话题争议: 大胆开麦、真实评价
生活分享: 日常、碎片、治愈
```

### 4. 分析维度
- **标题结构**: 数字吸引、情绪钩子、利益承诺
- **内容特点**: 痛点引入、解决方案、效果展示
- **视觉元素**: 封面图、排版、色彩搭配
- **互动策略**: 提问、投票、征集、福利

## 🛠️ 集成到OpenClaw

### 1. 配置MCP服务器
```json
// 在OpenClaw配置中添加
{
  "mcpServers": {
    "xiaohongshu": {
      "url": "http://localhost:18060/mcp",
      "type": "http"
    }
  }
}
```

### 2. 创建分析脚本
```python
# xiaohongshu_analyzer.py
import requests
import json
from datetime import datetime, timedelta

class XiaohongshuAnalyzer:
    def __init__(self, mcp_url="http://localhost:18060/mcp"):
        self.mcp_url = mcp_url
    
    def search_hot_content(self, keyword, days=15):
        """搜索近N天的热门内容"""
        # 计算时间范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 构建搜索参数
        params = {
            "keyword": f"{keyword} {start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}",
            "sort": "hot",
            "page": 1
        }
        
        # 调用MCP搜索工具
        response = requests.post(
            self.mcp_url,
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "search_feeds",
                    "arguments": params
                },
                "id": 1
            }
        )
        
        return response.json()
    
    def extract_keywords(self, content_list):
        """从内容中提取关键词"""
        keywords = {
            "情感共鸣": ["破防", "泪目", "谁懂", "共情", "emo", "绝了", "宝藏"],
            "实用价值": ["保姆级", "手把手", "小白", "零基础", "避雷", "踩坑", "省钱"],
            "视觉吸引": ["绝美", "神仙", "氛围感", "高级", "ins风", "治愈", "复古"],
            "话题争议": ["大胆开麦", "真实评价", "内行人", "揭秘", "争议"],
            "生活分享": ["日常", "碎片", "治愈", "自律", "打卡", "经验"]
        }
        
        keyword_stats = {}
        for category, words in keywords.items():
            for word in words:
                count = sum(content.lower().count(word) for content in content_list)
                if count > 0:
                    keyword_stats[f"{category}:{word}"] = count
        
        return dict(sorted(keyword_stats.items(), key=lambda x: x[1], reverse=True))
```

## 📈 分析报告生成

### 报告结构
1. **时间范围**: 近15天（2026-02-04至2026-02-18）
2. **数据样本**: 热门笔记50-100篇
3. **分析维度**: 
   - 关键词频率统计
   - 标题结构分析
   - 内容类型分布
   - 互动模式总结
4. **创作建议**: 
   - 标题优化策略
   - 内容结构建议
   - 视觉元素指导
   - 互动提升技巧

### 输出格式
- **JSON报告**: 结构化数据，便于程序处理
- **Markdown报告**: 便于阅读和分享
- **Excel表格**: 数据统计和分析
- **可视化图表**: 关键词云图、趋势图

## 🚀 快速开始脚本

```python
#!/usr/bin/env python3
"""
小红书爆款文案分析快速开始脚本
"""

import subprocess
import time
import os

def deploy_xiaohongshu_mcp():
    """部署小红书MCP服务器"""
    print("🚀 开始部署小红书MCP服务器...")
    
    # 1. 检查是否已下载
    if not os.path.exists("xiaohongshu-mcp-darwin-arm64.tar.gz"):
        print("📦 下载MCP服务器...")
        subprocess.run([
            "curl", "-L", "-o", "xiaohongshu-mcp-darwin-arm64.tar.gz",
            "https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-darwin-arm64.tar.gz"
        ])
    
    # 2. 解压文件
    print("📂 解压文件...")
    subprocess.run(["tar", "xzf", "xiaohongshu-mcp-darwin-arm64.tar.gz"])
    
    # 3. 添加执行权限
    print("🔧 设置执行权限...")
    subprocess.run(["chmod", "+x", "xiaohongshu-login-darwin-arm64"])
    subprocess.run(["chmod", "+x", "xiaohongshu-mcp-darwin-arm64"])
    
    print("✅ 部署完成！")
    print("\n📋 下一步操作：")
    print("1. 运行登录工具: ./xiaohongshu-login-darwin-arm64")
    print("2. 扫码登录小红书账号")
    print("3. 启动MCP服务器: ./xiaohongshu-mcp-darwin-arm64")
    print("4. 服务器运行在: http://localhost:18060/mcp")

if __name__ == "__main__":
    deploy_xiaohongshu_mcp()
```

## ⚠️ 注意事项

### 1. 登录问题
- 首次必须手动登录
- 不要同时在多个网页端登录同一账号
- cookies保存在 `~/.xiaohongshu/cookies.json`

### 2. 使用限制
- 每天发帖量限制：约50篇
- 标题不超过20个字
- 正文不超过1000个字
- 图片推荐使用本地路径

### 3. 风险提示
- 遵守小红书社区规范
- 避免发布违规内容
- 注意账号安全

## 📞 故障排除

### 常见问题
1. **无法连接MCP服务器**
   - 检查端口18060是否被占用
   - 确认服务器已启动
   - 查看日志输出

2. **登录失败**
   - 重新运行登录工具
   - 清除cookies文件重新登录
   - 检查网络连接

3. **搜索无结果**
   - 调整搜索关键词
   - 检查登录状态
   - 确认时间范围

### 获取帮助
- 项目GitHub: https://github.com/xpzouying/xiaohongshu-mcp
- 飞书互助群: 扫码加入（见README）
- 微信群: 扫码加入（见README）

## 🎯 完成部署后的操作

### 1. 测试搜索功能
```bash
# 使用curl测试搜索
curl -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_feeds",
      "arguments": {
        "keyword": "爆款文案",
        "sort": "hot",
        "page": 1
      }
    },
    "id": 1
  }'
```

### 2. 运行分析脚本
```bash
python3 xiaohongshu_analyzer.py
```

### 3. 生成分析报告
```bash
python3 generate_report.py --days 15 --keyword "爆款"
```

现在文件正在下载中，下载完成后按照上述指南操作即可部署小红书MCP服务器！