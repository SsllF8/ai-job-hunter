"""
PushPlus 微信推送模块
将分析结果推送到用户微信
"""

import os
import json
import requests
import logging

logger = logging.getLogger(__name__)


def push_to_wechat(title: str, content: str, template: str = "markdown") -> bool:
    """
    通过 PushPlus 推送消息到微信
    
    Args:
        title: 消息标题
        content: 消息内容（支持 markdown）
        template: 消息模板，支持 html/txt/markdown/json
        
    Returns:
        是否推送成功
    """
    token = os.getenv("PUSHPLUS_TOKEN")
    if not token:
        logger.error("PUSHPLUS_TOKEN 未配置")
        return False
    
    url = "http://www.pushplus.plus/send"
    
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
    }
    
    try:
        response = requests.post(url, json=data, timeout=15)
        result = response.json()
        
        if result.get("code") == 200:
            logger.info(f"微信推送成功: {title}")
            return True
        else:
            logger.error(f"微信推送失败: {result}")
            return False
            
    except Exception as e:
        logger.error(f"微信推送异常: {e}")
        return False


def push_job_results(jobs: list[dict], keyword: str, city: str = "") -> bool:
    """
    将岗位分析结果格式化后推送到微信
    
    Args:
        jobs: 分析后的岗位列表
        keyword: 搜索关键词
        city: 搜索城市
        
    Returns:
        是否推送成功
    """
    # 构建 Markdown 内容
    lines = [
        f"## 🔍 搜索条件",
        f"- 关键词：{keyword}",
        f"- 城市：{city or '不限'}",
        f"- 找到 {len(jobs)} 个相关岗位",
        "",
        "---",
        "",
    ]
    
    for i, job in enumerate(jobs, 1):
        score = job.get("match_score", 0)
        # 匹配度颜色标记
        if score >= 70:
            emoji = "🟢"
        elif score >= 40:
            emoji = "🟡"
        elif score > 0:
            emoji = "🔴"
        else:
            emoji = "⚪"
        
        lines.append(f"### {emoji} {i}. {job['title']}")
        if job.get("company"):
            lines.append(f"- 公司：{job['company']}")
        lines.append(f"- 匹配度：**{score}分**")
        if job.get("salary_range"):
            lines.append(f"- 薪资：{job['salary_range']}")
        if job.get("key_skills"):
            lines.append(f"- 核心技能：{'、'.join(job['key_skills'])}")
        if job.get("gap_analysis"):
            lines.append(f"- 差距分析：{job['gap_analysis']}")
        if job.get("highlight"):
            lines.append(f"- 💡 {job['highlight']}")
        if job.get("url"):
            lines.append(f"- 🔗 [查看详情]({job['url']})")
        lines.append("")
    
    content = "\n".join(lines)
    title = f"🎯 AI求职助手 | {keyword}{('·' + city) if city else ''} | {len(jobs)}个岗位"
    
    return push_to_wechat(title=title, content=content, template="markdown")


def push_summary(summary: str) -> bool:
    """
    推送分析总结到微信
    
    Args:
        summary: 分析总结内容（Markdown）
        
    Returns:
        是否推送成功
    """
    return push_to_wechat(
        title="📊 AI求职助手 | 市场分析报告",
        content=summary,
        template="markdown"
    )
