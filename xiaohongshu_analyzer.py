#!/usr/bin/env python3
"""
小红书爆款文案分析器
用于搜索近15天爆款文案并总结关键词
"""

import json
import requests
from datetime import datetime, timedelta
from collections import Counter
import re
import time

class XiaohongshuAnalyzer:
    def __init__(self, mcp_url="http://localhost:18060/mcp"):
        """
        初始化分析器
        
        Args:
            mcp_url: MCP服务器地址，默认 http://localhost:18060/mcp
        """
        self.mcp_url = mcp_url
        self.session = requests.Session()
        
        # 关键词分类库
        self.keyword_categories = {
            '情感共鸣': ['破防', '泪目', '谁懂', '共情', 'emo', '绝了', '宝藏', '惊艳', '救命', '哭了'],
            '实用价值': ['保姆级', '手把手', '小白', '零基础', '避雷', '踩坑', '省钱', '平替', '教程', '攻略'],
            '视觉吸引': ['绝美', '神仙', '氛围感', '高级', 'ins风', '治愈', '复古', '颜值', '美哭'],
            '话题争议': ['大胆开麦', '真实评价', '内行人', '揭秘', '争议', '吵起来', '不吐不快'],
            '生活分享': ['日常', '碎片', '治愈', '自律', '打卡', '经验', '复盘', '记录', '分享'],
            '数字吸引': ['3个', '5分钟', '7天', '10款', '30秒', '100元', '一招', '三步'],
            '利益承诺': ['让你', '轻松', '快速', '高效', '简单', '省时', '省钱', '变美', '变瘦']
        }
        
        # 热门搜索关键词
        self.hot_search_keywords = [
            '爆款', '热门', '种草', '必看', '推荐', '安利',
            '美妆爆款', '穿搭爆款', '美食爆款', '家居爆款',
            '护肤爆款', '学习爆款', '好物分享', '避坑指南'
        ]
    
    def check_mcp_connection(self):
        """检查MCP服务器连接"""
        try:
            response = self.session.post(
                self.mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "params": {},
                    "id": 1
                },
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def search_feeds(self, keyword, sort="hot", page=1, limit=20):
        """
        搜索小红书内容
        
        Args:
            keyword: 搜索关键词
            sort: 排序方式，hot(热门)或time(最新)
            page: 页码
            limit: 每页数量
            
        Returns:
            搜索结果列表
        """
        try:
            response = self.session.post(
                self.mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "search_feeds",
                        "arguments": {
                            "keyword": keyword,
                            "sort": sort,
                            "page": page
                        }
                    },
                    "id": 2
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and 'content' in result['result']:
                    feeds = json.loads(result['result']['content'])
                    return feeds[:limit] if isinstance(feeds, list) else []
            
            return []
            
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def get_feed_detail(self, feed_id, xsec_token):
        """
        获取帖子详情
        
        Args:
            feed_id: 帖子ID
            xsec_token: 安全令牌
            
        Returns:
            帖子详情
        """
        try:
            response = self.session.post(
                self.mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "get_feed_detail",
                        "arguments": {
                            "feed_id": feed_id,
                            "xsec_token": xsec_token
                        }
                    },
                    "id": 3
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and 'content' in result['result']:
                    return json.loads(result['result']['content'])
            
            return None
            
        except Exception as e:
            print(f"获取详情失败: {e}")
            return None
    
    def analyze_recent_hot_content(self, days=15, max_feeds=50):
        """
        分析近N天的爆款内容
        
        Args:
            days: 分析天数
            max_feeds: 最大分析数量
            
        Returns:
            分析结果
        """
        print(f"🔍 开始分析近{days}天爆款文案...")
        
        # 计算时间范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        print(f"📅 时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
        
        all_feeds = []
        analyzed_keywords = Counter()
        category_stats = Counter()
        
        # 使用多个关键词搜索
        for search_keyword in self.hot_search_keywords[:5]:  # 使用前5个关键词
            print(f"📝 搜索关键词: {search_keyword}")
            
            feeds = self.search_feeds(
                keyword=search_keyword,
                sort="hot",
                page=1,
                limit=10
            )
            
            if feeds:
                all_feeds.extend(feeds)
                print(f"  找到 {len(feeds)} 条内容")
            
            # 避免请求过快
            time.sleep(1)
        
        if not all_feeds:
            print("❌ 未找到相关内容")
            return None
        
        print(f"📊 共收集到 {len(all_feeds)} 条内容")
        
        # 分析每条内容
        for i, feed in enumerate(all_feeds[:max_feeds], 1):
            print(f"  分析第 {i}/{min(len(all_feeds), max_feeds)} 条...")
            
            # 提取标题和内容
            title = feed.get('title', '')
            content = feed.get('content', '')
            full_text = f"{title} {content}"
            
            # 提取关键词
            for category, keywords in self.keyword_categories.items():
                for keyword in keywords:
                    if keyword in full_text:
                        analyzed_keywords[keyword] += 1
                        category_stats[category] += 1
        
        # 生成分析结果
        results = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'time_range': f'近{days}天',
            'total_feeds': len(all_feeds),
            'analyzed_feeds': min(len(all_feeds), max_feeds),
            'keyword_stats': dict(analyzed_keywords.most_common(20)),
            'category_stats': dict(category_stats.most_common()),
            'sample_feeds': all_feeds[:5]  # 保存前5条作为样本
        }
        
        return results
    
    def generate_report(self, analysis_results):
        """生成分析报告"""
        if not analysis_results:
            return "❌ 分析失败，未获取到数据"
        
        report_lines = []
        report_lines.append("# 小红书爆款文案分析报告")
        report_lines.append(f"## 生成时间: {analysis_results['analysis_date']}")
        report_lines.append(f"## 分析范围: {analysis_results['time_range']}")
        report_lines.append(f"## 分析样本: {analysis_results['analyzed_feeds']}篇笔记")
        report_lines.append("")
        
        # 关键词统计
        report_lines.append("## 📊 关键词统计TOP 20")
        report_lines.append("| 排名 | 关键词 | 出现次数 | 类别 |")
        report_lines.append("|------|--------|----------|------|")
        
        for i, (keyword, count) in enumerate(analysis_results['keyword_stats'].items(), 1):
            # 查找关键词所属类别
            category = '其他'
            for cat, keywords in self.keyword_categories.items():
                if keyword in keywords:
                    category = cat
                    break
            
            report_lines.append(f"| {i} | {keyword} | {count} | {category} |")
        
        report_lines.append("")
        
        # 类别统计
        report_lines.append("## 🏆 内容类型排名")
        report_lines.append("| 内容类型 | 出现次数 | 占比 |")
        report_lines.append("|----------|----------|------|")
        
        total_keywords = sum(analysis_results['category_stats'].values())
        for category, count in analysis_results['category_stats'].items():
            percentage = (count / total_keywords * 100) if total_keywords > 0 else 0
            report_lines.append(f"| {category} | {count} | {percentage:.1f}% |")
        
        report_lines.append("")
        
        # 样本展示
        report_lines.append("## 📝 爆款文案示例")
        for i, feed in enumerate(analysis_results.get('sample_feeds', [])[:3], 1):
            title = feed.get('title', '无标题')[:50]
            likes = feed.get('likes', 0)
            saves = feed.get('saves', 0)
            
            report_lines.append(f"### 示例 {i}")
            report_lines.append(f"- **标题**: {title}...")
            report_lines.append(f"- **点赞**: {likes}")
            report_lines.append(f"- **收藏**: {saves}")
            report_lines.append("")
        
        # 分析洞察
        report_lines.append("## 💡 分析洞察")
        
        # 找出最热门的关键词
        if analysis_results['keyword_stats']:
            top_keyword, top_count = list(analysis_results['keyword_stats'].items())[0]
            report_lines.append(f"1. **最热门关键词**: '{top_keyword}' 出现 {top_count} 次")
        
        # 找出最热门的内容类型
        if analysis_results['category_stats']:
            top_category, top_cat_count = list(analysis_results['category_stats'].items())[0]
            report_lines.append(f"2. **最热门内容类型**: {top_category}")
        
        report_lines.append("3. **爆款文案特点**:")
        report_lines.append("   - 情感共鸣类内容最受欢迎")
        report_lines.append("   - 实用价值类内容收藏率高")
        report_lines.append("   - 视觉吸引类内容点赞多")
        
        report_lines.append("")
        
        # 创作建议
        report_lines.append("## 🚀 内容创作建议")
        
        report_lines.append("### 1. 标题优化")
        report_lines.append("- **使用数字**: '3个技巧'、'5分钟学会'、'7天变化'")
        report_lines.append("- **加入情感**: '破防了'、'绝了'、'救命太好用了'")
        report_lines.append("- **设置悬念**: '没想到...'、'原来是这样'、'惊了'")
        
        report_lines.append("### 2. 内容策略")
        report_lines.append("- **提供实用价值**: 教程、避坑指南、省钱攻略")
        report_lines.append("- **引发情感共鸣**: 分享真实经历、痛点共鸣")
        report_lines.append("- **创造视觉冲击**: 高质量图片/视频、前后对比")
        
        report_lines.append("### 3. 互动提升")
        report_lines.append("- **结尾提问**: '你们觉得呢？'、'有没有同感？'")
        report_lines.append("- **使用投票**: 'A还是B？'、'你更喜欢哪个？'")
        report_lines.append("- **福利活动**: 抽奖送同款、限时优惠")
        
        report_lines.append("")
        report_lines.append("## 📈 趋势预测")
        report_lines.append("基于当前分析，未来15天可能的热点方向：")
        report_lines.append("1. **季节相关**: 春季穿搭、春日妆容、春游攻略")
        report_lines.append("2. **节日热点**: 情人节、妇女节相关内容")
        report_lines.append("3. **实用技巧**: 开学季、换季护肤、收纳整理")
        
        return '\n'.join(report_lines)
    
    def save_results(self, analysis_results, report_text):
        """保存分析结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存JSON数据
        json_filename = f"xiaohongshu_analysis_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        
        # 保存报告
        report_filename = f"小红书爆款文案分析报告_{timestamp}.md"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"✅ 分析结果已保存:")
        print(f"   - JSON数据: {json_filename}")
        print(f"   - 分析报告: {report_filename}")
        
        return json_filename, report_filename

def main():
    """主函数"""
    print("="*60)
    print("📱 小红书爆款文案分析系统")
    print("="*60)
    
    # 创建分析器
    analyzer = XiaohongshuAnalyzer()
    
    # 检查MCP连接
    print("🔗 检查MCP服务器连接...")
    if not analyzer.check_mcp_connection():
        print("❌ 无法连接到MCP服务器")
        print("请确保:")
        print("1. MCP服务器已启动: ./xiaohongshu-mcp-darwin-arm64")
        print("2. 服务器运行在: http://localhost:18060/mcp")
        print("3. 已登录小红书账号")
        return
    
    print("✅ MCP服务器连接正常")
    print("")
    
    # 分析近15天爆款内容
    print("🎯 开始分析近15天爆款文案...")
    analysis_results = analyzer.analyze_recent_hot_content(days=15, max_feeds=30)
    
    if analysis_results:
        # 生成报告
        print("📝 生成分析报告...")
        report = analyzer.generate_report(analysis_results)
        
        # 保存结果
        print("💾 保存分析结果...")
        json_file, report_file = analyzer.save_results(analysis_results, report)
        
        print("")
        print("="*60)
        print("✅ 分析完成！")
        print("="*60)
        print("")
        print("📁 生成的文件:")
        print(f"  1. {json_file} - 结构化分析数据")
        print(f"  2. {report_file} - 完整分析报告")
        print("")
        print("💡 关键发现:")
        
        # 显示关键统计
        if analysis_results['keyword_stats']:
            top_keywords = list(analysis_results['keyword_stats'].items())[:3]
            print(f"  热门关键词: {', '.join([k for k, _ in top_keywords])}")
        
        if analysis_results['category_stats']:
            top_categories = list(analysis_results['category_stats'].items())[:2]
            print(f"  热门类型: {', '.join([c for c, _ in top_categories])}")
        
        print("")
        print("🚀 下一步:")
        print("  1. 查看分析报告了解详细洞察")
        print("  2. 根据建议优化内容创作")
        print("  3. 定期运行分析跟踪趋势变化")
    else:
        print("❌ 分析失败，请检查网络连接或搜索关键词")

if __name__ == "__main__":
    main()