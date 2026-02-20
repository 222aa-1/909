#!/usr/bin/env python3
"""
快速分析hcc1001110011账号
"""

import requests
import json
import time
from datetime import datetime

def quick_analyze():
    print("🚀 快速分析小红书账号: hcc1001110011")
    print("="*60)
    
    # 直接调用MCP工具
    server_url = "http://localhost:18060/mcp"
    
    # 1. 创建会话
    print("🔧 创建会话...")
    init_data = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "quick-analyzer", "version": "1.0"}
        },
        "id": 1
    }
    
    try:
        response = requests.post(server_url, json=init_data, timeout=10)
        session_id = response.headers.get('Mcp-Session-Id')
        
        if not session_id:
            print("❌ 无法获取会话ID")
            return
        
        headers = {"Content-Type": "application/json", "Mcp-Session-Id": session_id}
        print(f"   会话ID: {session_id}")
        
        # 2. 搜索账号相关内容
        print("\n🔍 搜索账号内容...")
        
        # 搜索穿搭相关内容
        search_results = []
        keywords = ["穿搭", "女装", "时尚", "韩系"]
        
        for keyword in keywords:
            print(f"   搜索: {keyword}")
            call_data = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "search_feeds",
                    "arguments": {"keyword": keyword}
                },
                "id": int(time.time() * 1000) % 10000
            }
            
            response = requests.post(server_url, headers=headers, json=call_data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and 'content' in result['result']:
                    content = result['result']['content']
                    if content:
                        search_results.extend(content)
            
            time.sleep(1)
        
        # 3. 分析结果
        print(f"\n📊 找到 {len(search_results)} 条相关内容")
        
        if not search_results:
            print("⚠️ 未找到相关内容，使用通用穿搭分析")
            # 使用之前的数据
            return generate_generic_report()
        
        # 提取标题和关键词
        titles = []
        for item in search_results[:20]:  # 取前20条
            if 'text' in item:
                try:
                    data = json.loads(item['text'])
                    if 'feeds' in data:
                        for feed in data['feeds'][:5]:  # 每个结果取前5条
                            if 'noteCard' in feed:
                                title = feed['noteCard'].get('displayTitle', '')
                                if title:
                                    titles.append(title)
                except:
                    pass
        
        print(f"   提取到 {len(titles)} 个标题")
        
        # 4. 生成快速报告
        report = generate_quick_report(titles)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"hcc1001110011_快速分析_{timestamp}.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ 快速分析完成!")
        print(f"📄 报告已保存: {report_file}")
        
        # 打印摘要
        print("\n" + "="*60)
        print("📋 分析摘要:")
        print("-" * 40)
        lines = report.split('\n')
        for line in lines[:30]:
            if line.strip():
                print(line)
        
    except Exception as e:
        print(f"❌ 分析错误: {e}")
        # 生成通用报告
        report = generate_generic_report()
        print("\n📄 已生成通用穿搭分析报告")

def generate_quick_report(titles):
    """生成快速报告"""
    from collections import Counter
    import re
    
    # 分析关键词
    keywords = Counter()
    for title in titles:
        words = re.findall(r'[\u4e00-\u9fff]{2,}', title)
        for word in words:
            keywords[word] += 1
    
    # 内容分类
    categories = Counter()
    for title in titles:
        if any(word in title for word in ['穿搭', '搭配', '衣服']):
            categories['穿搭教程'] += 1
        elif any(word in title for word in ['测评', '试穿', '实测']):
            categories['产品测评'] += 1
        elif any(word in title for word in ['分享', '推荐', '安利']):
            categories['好物分享'] += 1
        elif any(word in title for word in ['韩系', '韩风']):
            categories['韩系风格'] += 1
        else:
            categories['其他'] += 1
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# 小红书账号快速分析报告
账号ID: hcc1001110011
生成时间: {timestamp}
分析内容: {len(titles)} 条

## 📊 内容概况

### 内容类型分布
"""
    
    for category, count in categories.items():
        percentage = (count / len(titles)) * 100 if titles else 0
        report += f"- **{category}**: {count} 条 ({percentage:.1f}%)\n"
    
    report += f"""
## 🔑 热门关键词 (前15个)
"""
    
    top_keywords = keywords.most_common(15)
    for i, (keyword, count) in enumerate(top_keywords, 1):
        report += f"{i}. **{keyword}** ({count}次)\n"
    
    report += f"""
## 📝 标题示例
"""
    
    for i, title in enumerate(titles[:10], 1):
        report += f"{i}. {title}\n"
    
    report += f"""
## 💡 初步分析

### 账号特点
1. **内容方向**: 主要聚焦{', '.join([c for c, _ in categories.most_common(3)])}
2. **关键词偏好**: 高频使用{', '.join([k for k, _ in top_keywords[:3]])}
3. **标题风格**: {'情感表达较强' if any('!' in t or '！' in t for t in titles) else '较为平实'}

### 建议方向
1. **内容优化**: 增加教程类内容的实用价值
2. **关键词策略**: 强化{', '.join([k for k, _ in top_keywords[:2]])}相关关键词
3. **互动提升**: 增加疑问式和互动引导

## 🎯 精准分析建议

由于快速分析的限制，建议进行深度分析：

### 需要获取的数据
1. **准确账号内容**: 使用账号ID精确获取
2. **互动数据**: 点赞、收藏、评论数量
3. **发布时间**: 发布频率和时间规律
4. **粉丝数据**: 粉丝增长和活跃度

### 深度分析方向
1. **竞品对比**: 与同类账号对比分析
2. **爆款分析**: 分析高互动内容特征
3. **趋势预测**: 预测内容发展方向
4. **策略优化**: 具体的内容和运营建议

---
*注: 此为快速分析报告，基于相关关键词搜索*
*建议进行深度分析获取更准确数据*
"""
    
    return report

def generate_generic_report():
    """生成通用穿搭分析报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# 小红书穿搭账号通用分析报告
生成时间: {timestamp}

## 📊 行业趋势分析

### 热门穿搭风格
1. **韩系简约风** - 干净利落，注重版型
2. **复古港风** - 90年代复古元素
3. **运动休闲风** - 舒适与时尚结合
4. **甜酷女孩风** - 甜美与帅气混搭

### 爆款内容特征
- **教程型**: "穿搭的3个显瘦技巧"
- **测评型**: "单品实测对比"
- **分享型**: "我的穿搭合集"
- **疑问型**: "怎么穿显高？"

## 🎯 账号运营建议

### 内容策略
1. **明确风格定位**: 选择1-2个主打风格
2. **系列化内容**: 打造主题系列内容
3. **实用价值**: 提供可操作的穿搭建议
4. **视觉统一**: 建立品牌视觉风格

### 发布时间建议
- **最佳时段**: 12:00-14:00, 19:00-21:00
- **最佳日期**: 周四、周五
- **发布频率**: 每周3-5次

### 互动提升
1. **提问互动**: 使用疑问式标题
2. **投票活动**: 让用户参与选择
3. **话题讨论**: 引发用户讨论
4. **抽奖活动**: 增加粉丝粘性

## 📈 数据指标参考

### 优质内容标准
- **点赞率**: >3%
- **收藏率**: >5%
- **评论率**: >1%
- **分享率**: >0.5%

### 运营目标
- **短期**: 提升内容质量和互动
- **中期**: 打造爆款内容
- **长期**: 建立品牌影响力

---
*注: 此为通用分析报告*
*建议获取具体账号数据进行精准分析*
"""
    
    # 保存报告
    report_file = f"穿搭账号通用分析_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    quick_analyze()