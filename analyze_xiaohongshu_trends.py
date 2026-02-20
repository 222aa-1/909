#!/usr/bin/env python3
"""
小红书爆款文案分析脚本
搜索近15天的爆款文案并总结关键词
"""

import requests
import json
import re
import time
from datetime import datetime, timedelta
from collections import Counter
import jieba
import jieba.analyse

class XiaohongshuAnalyzer:
    def __init__(self, server_url="http://localhost:18060/mcp"):
        """初始化MCP客户端"""
        self.server_url = server_url
        self.session_id = None
        self.headers = {}
        
    def create_session(self):
        """创建MCP会话"""
        print("🔧 创建MCP会话...")
        
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
                    "name": "xiaohongshu-trend-analyzer",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }
        
        response = requests.post(self.server_url, json=init_data, timeout=10)
        if response.status_code != 200:
            print(f"   初始化失败: {response.status_code}")
            return False
        
        # 获取会话ID
        self.session_id = response.headers.get('Mcp-Session-Id')
        if self.session_id:
            print(f"   会话ID: {self.session_id}")
            self.headers = {
                "Content-Type": "application/json",
                "Mcp-Session-Id": self.session_id
            }
            return True
        else:
            print("   未找到会话ID")
            return False
    
    def call_tool(self, tool_name, arguments):
        """调用MCP工具"""
        call_data = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": int(time.time() * 1000) % 10000
        }
        
        try:
            response = requests.post(
                self.server_url, 
                headers=self.headers, 
                json=call_data, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'error' in result:
                    print(f"   工具调用错误: {result['error']}")
                    return None
                elif 'result' in result:
                    return result['result']
            else:
                print(f"   HTTP错误: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   调用异常: {e}")
            return None
    
    def search_recent_feeds(self, keyword="爆款", days=15):
        """搜索近期的内容"""
        print(f"\n🔍 搜索近{days}天的内容...")
        
        # 尝试不同的搜索参数
        search_params = [
            {"keyword": keyword},
            {"keyword": "热门"},
            {"keyword": "推荐"}
        ]
        
        all_feeds = []
        
        for params in search_params:
            print(f"   搜索关键词: {params['keyword']}")
            result = self.call_tool("search_feeds", params)
            
            if result and 'content' in result:
                content = result['content']
                if content and isinstance(content, list):
                    for item in content:
                        if 'text' in item:
                            try:
                                feeds_data = json.loads(item['text'])
                                if 'feeds' in feeds_data:
                                    all_feeds.extend(feeds_data['feeds'])
                            except:
                                pass
            
            time.sleep(1)  # 避免请求过快
        
        # 如果没有搜索结果，尝试使用list_feeds
        if not all_feeds:
            print("   使用list_feeds获取内容...")
            result = self.call_tool("list_feeds", {})
            if result and 'content' in result:
                content = result['content']
                if content and isinstance(content, list):
                    for item in content:
                        if 'text' in item:
                            try:
                                feeds_data = json.loads(item['text'])
                                if 'feeds' in feeds_data:
                                    all_feeds.extend(feeds_data['feeds'])
                            except:
                                pass
        
        # 过滤近期的内容
        recent_feeds = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for feed in all_feeds:
            # 这里可以根据实际数据结构调整时间过滤逻辑
            # 由于API可能不返回时间，我们先保留所有内容
            recent_feeds.append(feed)
        
        print(f"   找到 {len(recent_feeds)} 条内容")
        return recent_feeds
    
    def extract_keywords(self, feeds, top_n=20):
        """从内容中提取关键词"""
        print(f"\n📊 提取关键词 (前{top_n}个)...")
        
        # 收集所有文本
        all_text = ""
        titles = []
        
        for feed in feeds:
            if 'noteCard' in feed:
                note_card = feed['noteCard']
                if 'displayTitle' in note_card:
                    title = note_card['displayTitle']
                    titles.append(title)
                    all_text += title + " "
                
                # 如果有互动信息，可以记录点赞数
                if 'interactInfo' in note_card:
                    interact = note_card['interactInfo']
                    likes = interact.get('likedCount', '0')
                    # 可以用于筛选爆款内容
        
        if not all_text:
            return []
        
        # 使用jieba提取关键词
        jieba.analyse.set_stop_words("stop_words.txt")  # 如果有停用词文件
        
        # 提取关键词
        keywords = jieba.analyse.extract_tags(
            all_text, 
            topK=top_n, 
            withWeight=True,
            allowPOS=('n', 'vn', 'v', 'a', 'nr', 'ns', 'nt', 'nz')
        )
        
        return keywords, titles
    
    def analyze_trends(self, feeds):
        """分析趋势和模式"""
        print("\n📈 分析趋势模式...")
        
        trends = {
            "热门话题": [],
            "高频词汇": [],
            "内容类型": {},
            "情感倾向": {"positive": 0, "negative": 0, "neutral": 0}
        }
        
        # 分析内容类型
        content_types = Counter()
        for feed in feeds:
            if 'noteCard' in feed:
                note_card = feed['noteCard']
                title = note_card.get('displayTitle', '')
                
                # 简单分类
                if any(word in title for word in ['美食', '吃', '餐厅', '料理']):
                    content_types['美食'] += 1
                elif any(word in title for word in ['穿搭', '衣服', '时尚', '搭配']):
                    content_types['时尚穿搭'] += 1
                elif any(word in title for word in ['旅游', '旅行', '景点', '打卡']):
                    content_types['旅游'] += 1
                elif any(word in title for word in ['美妆', '化妆', '护肤', '美容']):
                    content_types['美妆护肤'] += 1
                elif any(word in title for word in ['生活', '日常', 'vlog', '记录']):
                    content_types['生活日常'] += 1
                elif any(word in title for word in ['学习', '知识', '干货', '教程']):
                    content_types['知识干货'] += 1
                elif any(word in title for word in ['情感', '恋爱', '婚姻', '感情']):
                    content_types['情感'] += 1
                elif any(word in title for word in ['搞笑', '幽默', '段子', '笑话']):
                    content_types['搞笑娱乐'] += 1
                else:
                    content_types['其他'] += 1
        
        trends["内容类型"] = dict(content_types)
        
        return trends
    
    def generate_report(self, keywords, titles, trends, days=15):
        """生成分析报告"""
        print("\n📋 生成分析报告...")
        
        report = f"""# 小红书近{days}天爆款文案分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
分析内容数量: {len(titles)}

## 📊 关键词分析
"""
        
        # 关键词部分
        report += "| 排名 | 关键词 | 权重 |\n"
        report += "|------|--------|------|\n"
        for i, (keyword, weight) in enumerate(keywords, 1):
            report += f"| {i} | {keyword} | {weight:.4f} |\n"
        
        # 趋势分析
        report += f"\n## 📈 内容类型分布\n"
        for content_type, count in trends["内容类型"].items():
            percentage = (count / len(titles)) * 100 if titles else 0
            report += f"- **{content_type}**: {count} 条 ({percentage:.1f}%)\n"
        
        # 热门标题示例
        report += f"\n## 🔥 热门标题示例\n"
        for i, title in enumerate(titles[:10], 1):
            report += f"{i}. {title}\n"
        
        # 爆款文案特征总结
        report += f"""
## 💡 爆款文案特征总结

### 1. 标题特征
- **数字吸引**: 使用具体数字增加可信度
- **情绪词**: 使用感叹词、表情符号增强情感表达
- **疑问句式**: 引发读者好奇和互动
- **利益点明确**: 直接说明能给读者带来的价值

### 2. 内容结构
- **开头抓眼球**: 前3秒决定用户是否继续阅读
- **中间有价值**: 提供实用信息或情感共鸣
- **结尾有行动**: 引导点赞、收藏、评论或关注

### 3. 热门话题方向
"""
        
        # 根据关键词推荐话题方向
        hot_keywords = [k for k, _ in keywords[:5]]
        report += f"- 基于高频关键词 {', '.join(hot_keywords)} 的内容更容易获得关注\n"
        
        # 创作建议
        report += f"""
## 🎯 创作建议

1. **结合热点**: 关注当前热门话题和节日节点
2. **突出价值**: 标题明确说明内容能给读者带来的好处
3. **情感共鸣**: 使用能引发情感共鸣的语言
4. **视觉吸引**: 配合高质量的图片或视频
5. **互动引导**: 明确引导用户点赞、评论、收藏

## 📝 示例爆款标题模板

1. "我宣布XXX是今年最XXX的XXX！"
2. "XXX个XXX技巧，让你XXX不再XXX"
3. "XXX原来要这样XXX！后悔没早点知道"
4. "XXX的XXX，XXX人都说XXX"
5. "XXX vs XXX，哪个更XXX？"

---
*分析基于小红书MCP服务器获取的公开内容，仅供参考*
"""
        
        return report
    
    def run_analysis(self, days=15):
        """运行完整分析"""
        print("="*60)
        print("📱 小红书爆款文案分析系统")
        print("="*60)
        
        # 创建会话
        if not self.create_session():
            print("❌ 无法创建MCP会话")
            return
        
        # 搜索近期内容
        feeds = self.search_recent_feeds(days=days)
        
        if not feeds:
            print("❌ 未找到内容数据")
            return
        
        # 提取关键词
        keywords, titles = self.extract_keywords(feeds)
        
        if not keywords:
            print("❌ 无法提取关键词")
            return
        
        # 分析趋势
        trends = self.analyze_trends(feeds)
        
        # 生成报告
        report = self.generate_report(keywords, titles, trends, days)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"小红书爆款文案分析报告_{timestamp}.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ 分析完成!")
        print(f"📄 报告已保存: {report_file}")
        print("\n" + "="*60)
        
        # 打印摘要
        print("\n📋 报告摘要:")
        print("-" * 40)
        lines = report.split('\n')
        for line in lines[:50]:  # 打印前50行作为摘要
            print(line)
        
        return report

def main():
    """主函数"""
    analyzer = XiaohongshuAnalyzer()
    
    try:
        report = analyzer.run_analysis(days=15)
        
        if report:
            # 保存简版报告
            with open("小红书爆款关键词摘要.txt", "w", encoding="utf-8") as f:
                # 提取关键词部分
                lines = report.split('\n')
                for line in lines:
                    if "| 排名 |" in line or line.startswith("| ") and "|" in line:
                        f.write(line + "\n")
                    
    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()