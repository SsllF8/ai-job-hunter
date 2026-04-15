import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from job_search import search_jobs, extract_job_info

print("=== 搜索测试 ===")
results = search_jobs("低代码开发", "上海", max_results=8)
print(f"原始结果: {len(results)} 条\n")

for i, r in enumerate(results, 1):
    job_site = "[JOB]" if r.get("is_job_site") else "[WEB]"
    print(f"{job_site} {i}. {r['title']}")
    print(f"   URL: {r['url'][:100]}")
    print()

print("=== 提取岗位信息 ===")
jobs = extract_job_info(results)
for j in jobs:
    print(f"  {j['title']} | 公司: {j['company']}")
