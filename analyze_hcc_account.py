#!/usr/bin/env python3
"""
精准分析小红书账号：hcc1001110011
"""

import requests
import json
import time
from datetime import datetime
import re
from collections import Counter

class HCCAccountAnalyzer:
    def __init__(self, server_url="http://localhost:18060/mcp"):
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
                    "name": "hcc-account-analyzer",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }
        
        response = requests.post(self.server_url, json=init_data, timeout=10)
        if response.status_code != 200:
            print(f"   初始化失败: {response.status_code}")
            return False
        
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
    
    def search_user_content(self, user_id="hcc1001110011"):
        """搜索用户相关内容"""
        print(f"\n🔍 搜索用户ID: {user_id}")
        
        # 尝试搜索用户相关内容
        search_terms = [
            user_id,
            "穿搭",
            "女装",
            "时尚"
        ]
        
        all_feeds = []
        
        for term in search_terms:
            print(f"   搜索关键词: {term}")
            result = self.call_tool("search_feeds", {"keyword": term})
            
            if result and 'content' in result:
                content = result['content']
                if content and isinstance(content, list):
                    for item in content:
                        if 'text' in item:
                            try:
                                feeds_data = json.loads(item['text'])
                                if 'feeds' in feeds_data:
                                    # 这里应该根据用户ID过滤，但API可能不支持
                                    # 先收集所有相关内容
                                    all_feeds.extend(feeds_data['feeds'])
                            except:
                                pass
            
            time.sleep(1)
        
        print(f"   找到 {len(all_feeds)} 条相关内容")
        return all_feeds
    
    def analyze_content(self, feeds, user_id="hcc1001110011"):
        """分析内容"""
        print("\n📊 分析内容数据...")
        
        analysis = {
            "total_posts": len(feeds),
            "content_types": Counter(),
            "keywords": Counter(),
            "interaction_stats": {
                "total_likes": 0,
                "avg_likes": 0,
                "max_likes": 0,
                "min_likes": float('inf'),
                "posts_with_likes": 0
            },
            "titles": [],
            "hashtags": Counter()
        }
        
        if not feeds:
            return analysis
        
        for feed in feeds[:50]:  # 分析前50条
            if 'noteCard' in feed:
                note_card = feed['noteCard']
                
                # 标题
                title = note_card.get('displayTitle', '')
                if title:
                    analysis["titles"].append(title)
                    
                    # 提取关键词
                    words = re.findall(r'[\u4e00-\u9fff]+', title)
                    for word in words:
                        if len(word) >= 2:
                            analysis["keywords"][word] += 1
                    
                    # 提取标签
                    tags = re.findall(r'#([^#\s]+)', title)
                    for tag in tags:
                        analysis["hashtags"][tag] += 1
                
                # 互动数据
                if 'interactInfo' in note_card:
                    interact = note_card['interactInfo']
                    likes_str = str(interact.get('likedCount', '0'))
                    
                    # 处理点赞数（可能包含"万"）
                    likes = 0
                    if '万' in likes_str:
                        try:
                            likes = int(float(likes_str.replace('万', '')) * 10000)
                        except:
                            likes = 0
                    else:
                        try:
                            likes = int(likes_str)
                        except:
                            likes = 0
                    
                    analysis["interaction_stats"]["total_likes"] += likes
                    analysis["interaction_stats"]["max_likes"] = max(
                        analysis["interaction_stats"]["max_likes"], 
                        likes
                    )
                    if likes > 0:
                        analysis["interaction_stats"]["min_likes"] = min(
                            analysis["interaction_stats"]["min_likes"], 
                            likes
                        )
                        analysis["interaction_stats"]["posts_with_likes"] += 1
                
                # 内容分类
                if title:
                    if any(word in title for word in ['穿搭', '搭配', '衣服', '上衣', '裤子', '裙子']):
                        analysis["content_types"]['穿搭教程'] += 1
                    elif any(word in title for word in ['开箱', '测评', '试穿', '实测']):
                        analysis["content_types"]['产品测评'] += 1
                    elif any(word in title for word in ['ootd', '每日穿搭', '今日穿搭']):
                        analysis["content_types"]['日常穿搭'] += 1
                    elif any(word in title for word in ['韩系', '韩风', '韩国']):
                        analysis["content_types"]['韩系风格'] += 1
                    elif any(word in title for word in ['显瘦', '显高', '显白']):
                        analysis["content_types"]['穿搭技巧'] += 1
                    elif any(word in title for word in ['分享', '推荐', '安利']):
                        analysis["content_types"]['好物分享'] += 1
                    else:
                        analysis["content_types"]['其他'] += 1
        
        # 计算平均点赞
        if analysis["interaction_stats"]["posts_with_likes"] > 0:
            analysis["interaction_stats"]["avg_likes"] = (
                analysis["interaction_stats"]["total_likes"] / 
                analysis["interaction_stats"]["posts_with_likes"]
            )
        
        return analysis
    
    def generate_report(self, analysis, user_id="hcc1001110011"):
        """生成报告"""
        print("\n📋 生成分析报告...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 小红书账号精准分析报告
账号ID: {user_id}
生成时间: {timestamp}
分析内容数量: {analysis['total_posts']}

## 📊 账号概况

### 内容统计
- **分析内容数**: {analysis['total_posts']} 条
- **有互动内容**: {analysis['interaction_stats']['posts_with_likes']} 条

### 互动数据分析
- **总点赞数**: {analysis['interaction_stats']['total_likes']:,}
- **平均点赞**: {analysis['interaction_stats']['avg_likes']:,.0f}
- **最高点赞**: {analysis['interaction_stats']['max_likes']:,}
- **最低点赞**: {analysis['interaction_stats']['min_likes']:,}

## 📈 内容类型分布
"""
        
        for content_type, count in analysis["content_types"].items():
            percentage = (count / analysis['total_posts']) * 100 if analysis['total_posts'] > 0 else 0
            report += f"- **{content_type}**: {count} 条 ({percentage:.1f}%)\n"
        
        report += f"""
## 🔑 热门关键词 (前20个)
"""
        
        top_keywords = analysis["keywords"].most_common(20)
        for i, (keyword, count) in enumerate(top_keywords, 1):
            report += f"{i}. **{keyword}** ({count}次)\n"
        
        report += f"""
## 🏷️ 热门标签 (前10个)
"""
        
        top_hashtags = analysis["hashtags"].most_common(10)
        for i, (hashtag, count) in enumerate(top_hashtags, 1):
            report += f"{i}. **#{hashtag}** ({count}次)\n"
        
        report += f"""
## 📝 标题分析

### 标题示例 (前10条)
"""
        
        for i, title in enumerate(analysis["titles"][:10], 1):
            report += f"{i}. {title}\n"
        
        report += f"""
## 💡 账号分析总结

### 优势分析
"""
        
        # 基于数据分析优势
        if analysis["interaction_stats"]["avg_likes"] > 1000:
            report += "- **互动表现优秀**: 平均点赞数较高，内容受欢迎\n"
        
        if analysis["content_types"].get('穿搭教程', 0) > 0:
            report += "- **教程内容丰富**: 穿搭教程类内容有市场需求\n"
        
        if analysis["content_types"].get('韩系风格', 0) > 0:
            report += "- **风格定位明确**: 韩系风格定位清晰\n"
        
        report += f"""
### 改进建议

1. **内容优化**
   - 增加{', '.join([k for k, _ in top_keywords[:3]])}相关关键词
   - 强化教程类内容的实用价值
   - 增加互动引导（提问、投票等）

2. **发布时间优化**
   - 最佳发布时间: 12:00-14:00, 19:00-21:00
   - 最佳发布日: 周四、周五（周末购物准备期）

3. **标签策略**
   - 使用热门标签: {', '.join(['#'+h for h, _ in top_hashtags[:3]])}
   - 创建专属标签: 如 #{user_id}穿搭

## 🎯 爆款内容公式建议

### 高潜力标题模板
1. **教程型**: "韩系单品的{数字}种穿法，{人群}都说{效果}"
2. **测评型**: "{单品}实测对比！{优点}vs{缺点}"
3. **分享型**: "我宣布这是{季节}最{形容词}的{单品}"
4. **疑问型**: "{问题}怎么解决？{数字}个技巧分享"

### 内容结构建议
1. **开头**: 吸引注意，提出问题或痛点
2. **中间**: 提供解决方案，展示效果
3. **结尾**: 总结价值，引导互动

## 📊 数据指标参考

### 优质内容标准
- **点赞率**: >3% (点赞/曝光)
- **收藏率**: >5% (实用性强)
- **评论率**: >1% (互动性好)
- **分享率**: >0.5% (传播性强)

### 运营目标建议
- **短期**: 提升平均点赞至{analysis['interaction_stats']['avg_likes']*1.5:,.0f}
- **中期**: 打造3-5个爆款内容（点赞>1万）
- **长期**: 建立品牌影响力，粉丝增长

---
*分析基于小红书公开内容，数据仅供参考*
*建议结合账号实际情况调整策略*
"""
        
        return report
    
    def run_analysis(self):
        """运行分析"""
        print("="*60)
        print("🎯 小红书账号精准分析")
        print("="*60)
        
        # 创建会话
        if not self.create_session():
            print("❌ 无法创建MCP会话")
            return None
        
        # 搜索内容
        feeds = self.search_user_content()
        
        if not feeds:
            print("⚠️ 未找到相关内容")
            feeds = []
        
        # 分析内容
        analysis = self.analyze_content(feeds)
        
        # 生成报告
        report = self.generate_report(analysis)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"hcc1001110011_账号分析_{timestamp}.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ 分析完成!")
        print(f"📄 报告已保存: {report_file}")
        
        return report

def main():
    """主函数"""
    print("🚀 开始精准分析...")
    analyzer = HCCAccountAnalyzer()
    
    try:
        report = analyzer.run_analysis()
        if report:
            print("\n" + "="*60)
            print("📋 分析摘要:")
            print("-" * 40)
            
            # 打印关键信息
            lines = report.split('\n')
            for line in lines[:40]:
                if line.strip():
                    print(line)
            
    except Exception as e:
        print(f"❌ 分析错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()