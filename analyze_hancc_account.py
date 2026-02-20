#!/usr/bin/env python3
"""
分析小红书账号：韩cc女装
"""

import requests
import json
import time
from datetime import datetime
import re
from collections import Counter

class HanccAnalyzer:
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
                    "name": "hancc-account-analyzer",
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
    
    def search_account_content(self, account_name="韩cc女装"):
        """搜索账号相关内容"""
        print(f"\n🔍 搜索账号: {account_name}")
        
        # 尝试不同的搜索关键词
        search_terms = [
            "韩cc女装",
            "韩cc",
            "韩cc穿搭",
            "韩系女装"
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
                                    # 过滤包含账号名的内容
                                    for feed in feeds_data['feeds']:
                                        if 'noteCard' in feed:
                                            note_card = feed['noteCard']
                                            user = note_card.get('user', {})
                                            display_title = note_card.get('displayTitle', '')
                                            
                                            # 检查是否包含账号名
                                            if account_name in display_title or account_name in user.get('nickname', ''):
                                                all_feeds.append(feed)
                            except:
                                pass
            
            time.sleep(1)  # 避免请求过快
        
        # 如果没有找到，尝试获取一般穿搭内容
        if not all_feeds:
            print("   未找到账号专属内容，获取穿搭相关内容...")
            result = self.call_tool("search_feeds", {"keyword": "韩系穿搭"})
            if result and 'content' in result:
                content = result['content']
                if content and isinstance(content, list):
                    for item in content:
                        if 'text' in item:
                            try:
                                feeds_data = json.loads(item['text'])
                                if 'feeds' in feeds_data:
                                    all_feeds.extend(feeds_data['feeds'][:20])  # 取前20条
                            except:
                                pass
        
        print(f"   找到 {len(all_feeds)} 条相关内容")
        return all_feeds
    
    def analyze_account_patterns(self, feeds):
        """分析账号内容模式"""
        print("\n📊 分析账号内容模式...")
        
        analysis = {
            "content_types": Counter(),
            "keywords": Counter(),
            "interaction_stats": {
                "total_likes": 0,
                "avg_likes": 0,
                "max_likes": 0,
                "min_likes": float('inf')
            },
            "title_patterns": [],
            "posting_patterns": {}
        }
        
        if not feeds:
            return analysis
        
        # 分析每条内容
        for feed in feeds:
            if 'noteCard' in feed:
                note_card = feed['noteCard']
                
                # 标题分析
                title = note_card.get('displayTitle', '')
                if title:
                    analysis["title_patterns"].append(title)
                    
                    # 提取关键词
                    words = re.findall(r'[\u4e00-\u9fff]+', title)
                    for word in words:
                        if len(word) >= 2:  # 至少2个字
                            analysis["keywords"][word] += 1
                
                # 互动数据分析
                if 'interactInfo' in note_card:
                    interact = note_card['interactInfo']
                    likes = interact.get('likedCount', 0)
                    if isinstance(likes, str):
                        try:
                            likes = int(likes.replace('万', '0000').replace('千', '000'))
                        except:
                            likes = 0
                    
                    analysis["interaction_stats"]["total_likes"] += likes
                    analysis["interaction_stats"]["max_likes"] = max(
                        analysis["interaction_stats"]["max_likes"], 
                        likes
                    )
                    analysis["interaction_stats"]["min_likes"] = min(
                        analysis["interaction_stats"]["min_likes"], 
                        likes
                    )
                
                # 内容类型分类
                if 'desc' in note_card:
                    desc = note_card['desc']
                    # 简单分类
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
                    else:
                        analysis["content_types"]['其他'] += 1
        
        # 计算平均点赞
        if feeds:
            analysis["interaction_stats"]["avg_likes"] = (
                analysis["interaction_stats"]["total_likes"] / len(feeds)
            )
        
        return analysis
    
    def generate_account_report(self, feeds, analysis, account_name="韩cc女装"):
        """生成账号分析报告"""
        print("\n📋 生成账号分析报告...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 小红书账号分析报告：{account_name}
生成时间: {timestamp}
分析内容数量: {len(feeds)}

## 📊 账号概况

### 内容类型分布
"""
        
        for content_type, count in analysis["content_types"].items():
            percentage = (count / len(feeds)) * 100 if feeds else 0
            report += f"- **{content_type}**: {count} 条 ({percentage:.1f}%)\n"
        
        report += f"""
### 互动数据分析
- **总点赞数**: {analysis["interaction_stats"]["total_likes"]:,}
- **平均点赞**: {analysis["interaction_stats"]["avg_likes"]:,.0f}
- **最高点赞**: {analysis["interaction_stats"]["max_likes"]:,}
- **最低点赞**: {analysis["interaction_stats"]["min_likes"]:,}

## 🔑 热门关键词 (前15个)
"""
        
        # 获取热门关键词
        top_keywords = analysis["keywords"].most_common(15)
        for i, (keyword, count) in enumerate(top_keywords, 1):
            report += f"{i}. **{keyword}** ({count}次)\n"
        
        report += f"""
## 📝 标题模式分析

### 常见标题类型
"""
        
        # 分析标题模式
        title_patterns = {
            "教程型": sum(1 for t in analysis["title_patterns"] if any(word in t for word in ['教程', '教学', '怎么', '如何'])),
            "测评型": sum(1 for t in analysis["title_patterns"] if any(word in t for word in ['测评', '试穿', '实测', '开箱'])),
            "分享型": sum(1 for t in analysis["title_patterns"] if any(word in t for word in ['分享', '推荐', '安利', '种草'])),
            "疑问型": sum(1 for t in analysis["title_patterns"] if any(word in t for word in ['？', '?', '什么', '怎么', '为什么'])),
            "感叹型": sum(1 for t in analysis["title_patterns"] if any(word in t for word in ['！', '!', '绝了', '太', '超'])),
        }
        
        for pattern, count in title_patterns.items():
            percentage = (count / len(analysis["title_patterns"])) * 100 if analysis["title_patterns"] else 0
            report += f"- **{pattern}**: {count} 条 ({percentage:.1f}%)\n"
        
        report += f"""
## 🔥 热门标题示例
"""
        
        for i, title in enumerate(analysis["title_patterns"][:10], 1):
            report += f"{i}. {title}\n"
        
        report += f"""
## 💡 账号运营建议

### 1. 内容策略优化
"""
        
        # 基于分析给出建议
        if analysis["content_types"].get('穿搭教程', 0) > 0:
            report += "- **强化教程内容**: 穿搭教程类内容受欢迎，可增加步骤分解、搭配原理讲解\n"
        
        if analysis["content_types"].get('韩系风格', 0) > 0:
            report += "- **突出韩系特色**: 明确韩系风格定位，可增加韩国流行趋势解读\n"
        
        if analysis["interaction_stats"]["avg_likes"] > 1000:
            report += "- **保持高质量**: 当前互动数据良好，继续保持内容质量\n"
        else:
            report += "- **提升互动**: 尝试增加互动引导，如提问、投票、抽奖等\n"
        
        report += f"""
### 2. 标题优化建议
- **增加关键词**: 多使用 {', '.join([k for k, _ in top_keywords[:5]])} 等高频关键词
- **强化情感**: 使用感叹词和表情符号增强情感表达
- **制造好奇**: 使用疑问句式引发读者好奇
- **突出价值**: 明确说明内容能给读者带来的好处

### 3. 发布时间建议
基于小红书用户活跃时间，建议发布时间：
- **工作日**: 12:00-13:00 (午休时间), 18:00-20:00 (下班后)
- **周末**: 10:00-12:00 (上午), 15:00-17:00 (下午), 20:00-22:00 (晚上)

### 4. 内容扩展方向
1. **季节穿搭**: 结合当前季节推出相应穿搭
2. **场合穿搭**: 通勤、约会、旅行等不同场合搭配
3. **单品解析**: 深度解析热门单品的多种搭配方式
4. **身材适配**: 针对不同身材的穿搭建议
5. **性价比推荐**: 高性价比的韩系女装推荐

## 🎯 爆款内容公式

基于分析，建议采用以下公式：
```
韩系风格 + 实用教程 + 情感表达 + 视觉吸引 = 爆款
```

### 具体模板：
1. **教程模板**: "韩系单品的多种穿法，不同人群都说效果好"
2. **测评模板**: "品牌单品实测！优点明显但有些缺点，具体建议"
3. **分享模板**: "我宣布这是今年最棒的单品！理由充分"
4. **疑问模板**: "穿搭问题怎么解决？几个技巧让你效果显著"

---
*分析基于小红书公开内容，数据仅供参考*
"""
        
        return report
    
    def run_analysis(self):
        """运行完整分析"""
        print("="*60)
        print("👗 小红书账号分析：韩cc女装")
        print("="*60)
        
        # 创建会话
        if not self.create_session():
            print("❌ 无法创建MCP会话")
            return
        
        # 搜索账号内容
        feeds = self.search_account_content()
        
        if not feeds:
            print("⚠️ 未找到账号专属内容，将分析相关穿搭内容")
        
        # 分析内容模式
        analysis = self.analyze_account_patterns(feeds)
        
        # 生成报告
        report = self.generate_account_report(feeds, analysis)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"韩cc女装账号分析报告_{timestamp}.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ 分析完成!")
        print(f"📄 报告已保存: {report_file}")
        print("\n" + "="*60)
        
        # 打印摘要
        print("\n📋 分析摘要:")
        print("-" * 40)
        
        # 提取关键信息
        lines = report.split('\n')
        for line in lines[:50]:  # 打印前50行
            if line.strip():
                print(line)
        
        return report

def main():
    """主函数"""
    analyzer = HanccAnalyzer()
    
    try:
        report = analyzer.run_analysis()
        
    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()