"""
DeepSeek AI 分析模块
分析岗位信息、计算匹配度、生成简历建议
"""

import os
import json
import re
from openai import OpenAI

# 默认用户个人信息（未上传简历时使用）
DEFAULT_PROFILE = """
求职者背景：
- 求职方向：低代码开发 / AI 工具相关
- 编程经验：零基础转行
- 已掌握技术：Python 基础、LangChain、Streamlit、DeepSeek API
- 已完成项目：
  1. 企业 RAG 知识库问答系统（LangChain + ChromaDB + Streamlit）
  2. AI 数据分析助手（Agent + 代码生成 + 自动可视化）
  3. AI 智能求职助手（搜索 + AI 分析 + 微信推送）
- 个人特点：学习能力强、善于利用 AI 工具提效
"""


def get_client() -> OpenAI:
    """创建 DeepSeek API 客户端"""
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )


def analyze_single_job(job: dict, resume_text: str = "") -> dict:
    """
    分析单个岗位信息
    
    Args:
        job: 包含 title, snippet 的岗位信息
        resume_text: 用户简历文本（可选）
    """
    client = get_client()
    
    # 使用用户简历或默认画像
    profile = resume_text if resume_text.strip() else DEFAULT_PROFILE
    
    # 构造分析内容
    job_text = f"岗位标题：{job['title']}\n岗位摘要：{job['snippet']}"
    if job.get("salary_range") and job["salary_range"] != "面议":
        job_text += f"\n薪资范围：{job['salary_range']}"
    
    prompt = f"""你是一个专业的职业规划顾问。请根据求职者背景和岗位信息，进行深度分析。

## 求职者背景
{profile}

## 岗位信息
{job_text}

## 请分析以下内容（严格按 JSON 格式输出，不要输出其他内容）：

{{
    "match_score": <1-100的匹配度分数>,
    "key_skills": ["要求的1-3个核心技能"],
    "gap_analysis": "<50字以内的差距分析，指出求职者还缺什么>",
    "suggestion": "<50字以内的建议，如何提高匹配度>",
    "salary_range": "<如果能从文本中推测薪资范围则填写，否则填'面议'>",
    "highlight": "<一句话总结这个岗位最大的亮点或风险>"
}}"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
        
        content = response.choices[0].message.content.strip()
        
        # 提取 JSON
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            analysis = json.loads(json_match.group())
        else:
            analysis = {
                "match_score": 50,
                "key_skills": [],
                "gap_analysis": content[:100],
                "suggestion": "请进一步了解该岗位详情",
                "salary_range": job.get("salary_range", "面议"),
                "highlight": "分析结果解析异常"
            }
        
        job.update(analysis)
        
    except Exception as e:
        job.update({
            "match_score": -1,
            "key_skills": [],
            "gap_analysis": f"分析失败: {str(e)}",
            "suggestion": "",
            "salary_range": job.get("salary_range", "面议"),
            "highlight": ""
        })
    
    return job


def batch_analyze(jobs: list[dict], max_jobs: int = 8, resume_text: str = "") -> list[dict]:
    """
    批量分析岗位
    """
    analyzed = []
    jobs_to_analyze = jobs[:max_jobs]
    
    for i, job in enumerate(jobs_to_analyze, 1):
        print(f"正在分析第 {i}/{len(jobs_to_analyze)} 个岗位: {job['title'][:30]}...")
        job = analyze_single_job(job, resume_text)
        analyzed.append(job)
    
    # 按匹配度降序排列
    analyzed.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return analyzed


def generate_summary(jobs: list[dict], resume_text: str = "") -> str:
    """
    生成整体求职分析总结
    """
    client = get_client()
    
    profile = resume_text if resume_text.strip() else DEFAULT_PROFILE
    
    jobs_text = ""
    for i, job in enumerate(jobs, 1):
        jobs_text += f"""
{i}. {job['title']}
   - 匹配度: {job.get('match_score', 'N/A')}分
   - 核心技能: {', '.join(job.get('key_skills', []))}
   - 薪资: {job.get('salary_range', '面议')}
   - 差距: {job.get('gap_analysis', '')}"""

    prompt = f"""你是一个专业的职业规划顾问。基于以下岗位分析结果，给求职者一份简洁有力的总结报告。

## 求职者背景
{profile}

## 岗位分析结果
{jobs_text}

## 请生成一份简洁的分析报告（Markdown 格式，300字以内）：
- 市场概况：这类岗位的整体情况
- 高频技能要求：出现最多的技能
- 简历优化建议：最应该突出的 2-3 个点
- 推荐行动：下一步应该做什么"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"生成总结失败: {e}"
