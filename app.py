"""
AI 智能求职助手 - 主界面
搜索岗位 -> AI 分析匹配度 -> 推送到微信
"""

import streamlit as st
import os
from dotenv import load_dotenv

from job_search import search_jobs, extract_job_info
from ai_analyzer import batch_analyze, generate_summary
from wechat_notifier import push_job_results, push_summary

load_dotenv()

st.set_page_config(
    page_title="AI 智能求职助手",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 AI 智能求职助手")
st.caption("搜索岗位 → AI 分析匹配度 → 一键推送到微信")

st.markdown("---")

# ============ 侧边栏：简历上传 ============
with st.sidebar:
    st.header("📄 我的简历")
    st.caption("上传简历后，AI 会根据你的简历来分析岗位匹配度")
    
    uploaded_file = st.file_uploader(
        "上传简历（支持 .txt / .md）",
        type=["txt", "md"],
        help="支持纯文本或 Markdown 格式的简历"
    )
    
    resume_text = ""
    if uploaded_file:
        try:
            resume_text = uploaded_file.read().decode("utf-8")
            st.success(f"简历已加载（{len(resume_text)} 字）")
            with st.expander("预览简历内容"):
                st.text(resume_text[:1000])
        except Exception as e:
            st.error(f"简历读取失败: {e}")
    else:
        st.info("不上传简历，系统会使用默认画像")

# ============ 主区域：搜索条件 ============
st.subheader("🔍 搜索条件")

# 第一行：关键词 + 城市
col1, col2 = st.columns([3, 2])
with col1:
    keyword = st.text_input(
        "搜索关键词",
        placeholder="例如：低代码开发、AI Agent、AI工具产品经理",
        value="低代码开发"
    )
with col2:
    city = st.selectbox(
        "城市",
        ["", "北京", "上海", "广州", "深圳", "杭州", "成都", "南京", "武汉", "苏州", "西安", "远程"],
        format_func=lambda x: "不限" if x == "" else x,
    )

# 第二行：区域 + 薪资范围 + 工作类型
col3, col4, col5 = st.columns([2, 2, 2])

with col3:
    # 根据城市显示不同区域选项
    district_options = {
        "": ["不限"],
        "北京": ["不限", "朝阳区", "海淀区", "西城区", "东城区", "丰台区", "大兴区", "通州区"],
        "上海": ["不限", "浦东新区", "徐汇区", "黄浦区", "静安区", "长宁区", "杨浦区", "闵行区", "虹口区"],
        "广州": ["不限", "天河区", "越秀区", "海珠区", "番禺区", "白云区", "黄埔区"],
        "深圳": ["不限", "南山区", "福田区", "宝安区", "龙岗区", "罗湖区", "龙华区"],
        "杭州": ["不限", "西湖区", "滨江区", "余杭区", "拱墅区", "上城区"],
        "成都": ["不限", "高新区", "锦江区", "武侯区", "青羊区", "成华区"],
        "南京": ["不限", "建邺区", "鼓楼区", "玄武区", "雨花台区", "江宁区"],
        "武汉": ["不限", "洪山区", "武昌区", "江汉区", "东湖高新区"],
        "苏州": ["不限", "工业园区", "姑苏区", "吴中区", "高新区"],
        "西安": ["不限", "雁塔区", "高新区", "碑林区", "长安区"],
        "远程": ["不限"],
    }
    districts = district_options.get(city, ["不限"])
    district = st.selectbox("区域", districts)

with col4:
    salary_range = st.selectbox(
        "薪资范围",
        ["不限", "3K以下", "3K-5K", "5K-10K", "10K-15K", "15K-25K", "25K-50K", "50K以上"],
    )

with col5:
    job_type = st.selectbox(
        "工作类型",
        ["不限", "全职", "兼职", "实习", "远程"],
    )

# 第三行：搜索数量
max_results = st.select_slider("搜索数量", options=[5, 8, 10, 15, 20], value=8)

st.markdown("---")

# ============ 搜索按钮 ============
if st.button("🚀 开始搜索与分析", type="primary", use_container_width=True):
    if not keyword:
        st.warning("请输入搜索关键词")
    else:
        # 转换薪资为搜索词
        salary_min = ""
        if salary_range not in ["不限", "3K以下"]:
            salary_min = salary_range.split("-")[0]
        
        # 转换工作类型
        job_type_str = "" if job_type == "不限" else job_type
        
        # Step 1: 搜索
        with st.status("🔍 正在搜索岗位...", expanded=True) as status:
            location = f"{city}{district}" if city and district != "不限" else city
            st.write(f"关键词：**{keyword}** | 地点：**{location or '不限'}** | 薪资：**{salary_range}** | 类型：**{job_type}**")
            
            raw_results = search_jobs(
                keyword=keyword,
                city=city,
                district=district if district != "不限" else "",
                salary_min=salary_min,
                job_type=job_type_str,
                max_results=max_results,
            )
            
            if not raw_results:
                st.error("未搜索到结果，请尝试更换关键词或放宽筛选条件")
                status.update(label="❌ 搜索无结果", state="error")
                st.stop()
            
            st.write(f"搜索到 **{len(raw_results)}** 条结果，正在提取岗位信息...")
            jobs = extract_job_info(raw_results)
            status.update(label=f"✅ 搜索完成，找到 {len(jobs)} 个岗位", state="complete")
        
        # Step 2: AI 分析
        with st.status("🤖 AI 正在分析岗位匹配度...", expanded=True) as status:
            analyzed_jobs = batch_analyze(jobs, max_jobs=max_results, resume_text=resume_text)
            
            success_count = sum(1 for j in analyzed_jobs if j.get("match_score", -1) > 0)
            status.update(
                label=f"✅ 分析完成：{success_count} 个岗位分析成功", 
                state="complete"
            )
        
        # Step 3: 生成总结
        with st.status("📊 正在生成市场分析报告...", expanded=True) as status:
            summary = generate_summary(analyzed_jobs, resume_text=resume_text)
            status.update(label="✅ 分析报告已生成", state="complete")
        
        # 保存到 session_state
        st.session_state["analyzed_jobs"] = analyzed_jobs
        st.session_state["summary"] = summary
        st.session_state["keyword"] = keyword
        st.session_state["city"] = city

# ============ 显示结果 ============
if "analyzed_jobs" in st.session_state:
    jobs = st.session_state["analyzed_jobs"]
    summary = st.session_state["summary"]
    
    st.markdown("---")
    st.subheader("📊 市场分析报告")
    st.markdown(summary)
    
    st.markdown("---")
    st.subheader(f"📋 岗位分析结果（共 {len(jobs)} 个，按匹配度排序）")
    
    col_push, col_info = st.columns([1, 3])
    with col_push:
        pushed = st.button("📲 推送到微信", type="secondary", use_container_width=True)
    with col_info:
        st.caption("点击后会将所有分析结果推送到你的微信")
    
    if pushed:
        keyword_val = st.session_state.get("keyword", "")
        city_val = st.session_state.get("city", "")
        with st.spinner("正在推送..."):
            push_job_results(jobs, keyword_val, city_val)
            push_summary(summary)
        st.success("✅ 推送成功！请查看你的微信。")
    
    for i, job in enumerate(jobs, 1):
        score = job.get("match_score", 0)
        
        if score >= 70:
            emoji = "🟢"
        elif score >= 40:
            emoji = "🟡"
        elif score > 0:
            emoji = "🔴"
        else:
            emoji = "⚪"
        
        with st.container():
            st.markdown(f"#### {emoji} {i}. {job['title']}")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if score > 0:
                    st.metric("匹配度", f"{score} 分")
                else:
                    st.metric("匹配度", "分析失败")
            with col_b:
                if job.get("company"):
                    st.write(f"🏢 {job['company']}")
                if job.get("salary_range") and job["salary_range"] != "面议":
                    st.write(f"💰 {job['salary_range']}")
                else:
                    st.write(f"💰 面议")
            with col_c:
                if job.get("key_skills"):
                    skills = " ".join([f"`{s}`" for s in job["key_skills"]])
                    st.write(f"**核心技能：** {skills}")
            
            with st.expander("查看详细分析"):
                if job.get("gap_analysis"):
                    st.write(f"**📊 差距分析：** {job['gap_analysis']}")
                if job.get("suggestion"):
                    st.write(f"**💡 建议：** {job['suggestion']}")
                if job.get("highlight"):
                    st.write(f"**⚡ 亮点/风险：** {job['highlight']}")
                if job.get("snippet"):
                    st.write(f"**📝 摘要：** {job['snippet']}")
                if job.get("url"):
                    st.markdown(f"🔗 [查看原始页面]({job['url']})")
            
            st.markdown("---")

st.caption("💡 DuckDuckGo 搜索 + DeepSeek AI 分析 + PushPlus 微信推送")
