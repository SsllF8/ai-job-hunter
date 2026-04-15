"""
招聘信息搜索模块
通过搜索引擎获取真实招聘信息
"""

from ddgs import DDGS
import re
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_jobs(keyword: str, city: str = "", district: str = "", 
                salary_min: str = "", job_type: str = "",
                max_results: int = 10) -> list[dict]:
    """
    使用搜索引擎搜索招聘信息
    
    Args:
        keyword: 搜索关键词
        city: 城市，如 "上海"
        district: 区域，如 "徐汇区"
        salary_min: 最低薪资筛选，如 "5K", "10K"
        job_type: 工作类型，如 "全职", "兼职", "远程"
        max_results: 最大返回结果数
    """
    
    # 构造搜索词
    location = f"{city}{district}" if city and district else (city or "")
    
    # 构造多个搜索查询
    queries = []
    
    if location:
        queries.append(f"{location}{keyword}招聘 2025")
        queries.append(f"{keyword}岗位 {location} 最新招聘")
        queries.append(f"{keyword}工作 {location}")
    else:
        queries.append(f"{keyword}招聘 2025")
        queries.append(f"{keyword}岗位 最新招聘")
        queries.append(f"{keyword}工作 招聘")
    
    # 如果有薪资要求，加一个查询
    if salary_min:
        queries.insert(0, f"{keyword}招聘 {location} {salary_min}以上")
    
    # 如果有工作类型要求
    if job_type:
        queries.append(f"{keyword} {job_type} {location} 招聘")
    
    # 去重收集
    seen_urls = set()
    results = []
    
    for query in queries:
        if len(results) >= max_results:
            break
        
        try:
            with DDGS() as ddgs:
                search_results = list(ddgs.text(
                    query,
                    max_results=max_results,
                    region="cn-zh",
                ))
            
            logger.info(f"查询 '{query}' 返回 {len(search_results)} 条")
            
            for r in search_results:
                url = r.get("href", "")
                title = r.get("title", "")
                snippet = r.get("body", "")
                
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                
                # 过滤搜索结果页
                skip_patterns = ["/search", "/s?", "query=", "keyword=", "/jobs/search", "/job/search"]
                if any(p in url for p in skip_patterns):
                    continue
                
                # 过滤明显不是岗位帖子的结果
                skip_words = ["搜索结果", "为您找到", "招聘网站", "招聘大全", "招聘会", 
                              "怎么找", "有哪些平台", "渠道推荐", "求职指南"]
                if any(w in title for w in skip_words):
                    continue
                
                # 过滤过期岗位（标题中含去年及更早的日期）
                current_year = datetime.now().year
                old_date_patterns = [
                    rf"20{current_year - 2}",  # 前年
                    rf"20{current_year - 3}",  # 大前年
                    rf"({current_year - 2})年",
                ]
                matched_old = False
                for p in old_date_patterns:
                    if re.search(p, title + " " + snippet):
                        matched_old = True
                        break
                if matched_old:
                    continue
                
                # 判断是否可能过期（标题中包含"已结束"、"已关闭"、"已下线"等）
                expired_words = ["已结束", "已关闭", "已下线", "已过期", "已停招", "已截止"]
                if any(w in title for w in expired_words):
                    continue
                
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                })
                
                if len(results) >= max_results:
                    break
                    
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            continue
    
    logger.info(f"最终返回 {len(results)} 条结果")
    return results


def extract_job_info(results: list[dict]) -> list[dict]:
    """
    从搜索结果中提取岗位关键信息
    """
    jobs = []
    
    for result in results:
        title = result["title"]
        url = result["url"]
        snippet = result["snippet"]
        
        # 提取公司名称
        company = ""
        patterns = [
            r"[-|—_·](.+?)\s*$",
            r"^(.+?)\s*[-|—_·]",
        ]
        for p in patterns:
            m = re.search(p, title)
            if m and len(m.group(1)) < 30:
                company = m.group(1).strip()
                break
        
        # 提取薪资
        salary = "面议"
        salary_patterns = [
            r"(\d+[-~]\d+)K",
            r"(\d+[-~]\d+)k",
            r"(\d+[-~]\d+元/月)",
            r"(\d+[-~]\d+/月)",
            r"(\d+[-~]\d+万/年)",
            r"(\d{4,5}[-~]\d{4,5})",
        ]
        for p in salary_patterns:
            m = re.search(p, title + " " + snippet)
            if m:
                salary = m.group(1)
                break
        
        jobs.append({
            "title": title,
            "url": url,
            "snippet": snippet,
            "company": company,
            "salary_range": salary,
        })
    
    return jobs
