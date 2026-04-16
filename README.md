# 🎯 AI 智能求职助手 | AI Job Hunter

> [中文](#中文) | [English](#english)

---

<a id="中文"></a>
## 🇨🇳 中文

> 智能求职助手，全网搜索岗位，AI 分析人岗匹配度，结果直接推送到微信。上传一次简历，让 AI 帮你找。

![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red?logo=streamlit)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-blue)
![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Search-green)
![WeChat](https://img.shields.io/badge/PushPlus-WeChat-07c160?logo=wechat)

### 🎯 应用场景

**求职者场景：**
- **被动求职监控** — 设定目标岗位（如"深圳 AI 产品经理"），每天搜一次，匹配结果推送到微信
- **简历-岗位匹配** — 上传简历，AI 根据你的技能、经验、职业目标评估每个岗位的匹配度
- **多城市并行搜索** — 同时搜索不同城市和行业，对比机会
- **面试准备** — 用 AI 分析了解每个公司要什么，针对性准备简历和面试话术

**职业发展场景：**
- **市场调研** — 搜索感兴趣的角色，AI 总结薪资范围、技能要求、行业趋势
- **转行准备** — 上传当前简历，搜索目标领域，AI 识别技能差距和可迁移经验
- **应届生求职** — 经验有限时，AI 帮你找到匹配度最高的入门岗位

### 核心差异化

传统招聘平台需要手动浏览和主观判断。本工具**自动化整个流程**：搜索 → 过滤 → AI 分析 → 微信推送。AI 不只是匹配关键词，而是整体理解岗位需求并与你的简历对比。

### ✨ 功能特性

- 🔍 **全网岗位搜索** — 通过 DuckDuckGo 跨平台搜索岗位信息
- 🤖 **AI 匹配分析** — DeepSeek 根据简历/技能评估每个岗位的匹配度
- 📄 **简历上传** — 支持 .txt 和 .md 格式简历，用于个性化匹配
- 📱 **微信推送** — 一键通过 PushPlus 将结果推送到微信
- 📊 **匹配评分** — 每个岗位获得 0-100 匹配分 + 详细分析
- 📋 **批量分析** — 同时分析多个岗位，生成综合报告

### 📊 分析报告内容

**每个岗位：**
- **匹配分数**（0-100）及细分维度
- **技能匹配** — 你的哪些技能符合要求
- **技能差距** — 你还缺什么，重要性如何
- **建议** — 要不要投？为什么？

**综合报告：**
- 按匹配度排名的最佳岗位
- 所有岗位的共通技能要求
- 市场洞察和投递策略

### 🏗️ 系统架构

```
┌───────────────────────────────────────────────────────┐
│                 Streamlit Web UI                       │
│  ┌───────────┐  ┌────────────┐  ┌──────────────────┐ │
│  │  简历上传  │  │  搜索分析  │  │  结果 & 微信推送 │ │
│  └─────┬─────┘  └─────┬──────┘  └────────┬─────────┘ │
└────────┼──────────────┼──────────────────┼───────────┘
        │              │                  │
┌───────▼──────────────▼──────────────────▼───────────┐
│              流水线模块                               │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ job_search  │  │ ai_analyzer  │  │ wechat_    │ │
│  │ .py         │  │ .py          │  │ notifier   │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────┘
        │                  │                   │
        ▼                  ▼                   ▼
┌──────────────┐  ┌────────────────┐  ┌──────────────┐
│ DuckDuckGo   │  │  DeepSeek API  │  │  PushPlus    │
│ 搜索引擎     │  │  (匹配 AI)     │  │  (微信)      │
└──────────────┘  └────────────────┘  └──────────────┘
```

### 📖 工作流程

**搜索流程：**
```
用户查询（岗位 + 城市）
  → DuckDuckGo 定向关键词搜索
  → 抓取招聘页面
  → 解析 HTML 提取：职位名、公司、薪资、地点、要求
  → 展示结构化结果
```

**分析流程：**
```
岗位列表 + 用户简历
  → 发送给 DeepSeek（结构化 prompt）
  → AI 评估：技能匹配、经验适配、成长潜力
  → 生成每个岗位的匹配分数（0-100）
  → 产出综合报告和建议
```

**推送流程：**
```
分析结果
  → 格式化为微信友好的消息（Markdown）
  → POST 到 PushPlus API
  → 消息推送到用户微信
```

### 📁 项目结构

```
ai-job-hunter/
├── app.py                  # Streamlit Web 界面
├── job_search.py           # 岗位搜索与解析模块
├── ai_analyzer.py          # AI 匹配分析引擎
├── wechat_notifier.py      # 微信推送模块
├── test_search.py          # 搜索功能独立测试脚本
├── requirements.txt        # Python 依赖
├── .env.example            # 环境变量模板
└── 启动应用.bat             # Windows 快速启动
```

### 🚀 快速开始

```bash
git clone https://github.com/SsllF8/ai-job-hunter.git
cd ai-job-hunter
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env  # 填入 API 密钥
streamlit run app.py
```

### ⚙️ 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | ✅ | DeepSeek API 密钥 |
| `PUSHPLUS_TOKEN` | ✅ | PushPlus 微信推送 Token |

**获取 PushPlus Token：**
1. 访问 [pushplus.plus](https://www.pushplus.plus)
2. 微信扫码登录
3. 从控制台复制 Token
4. 粘贴到 `.env` 中的 `PUSHPLUS_TOKEN`

### 🛠️ 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| Web 框架 | Streamlit | 交互式求职搜索 UI |
| 岗位搜索 | DuckDuckGo Search | 网页搜索岗位信息 |
| HTML 解析 | BeautifulSoup + lxml | 从页面提取结构化岗位数据 |
| AI 匹配 | DeepSeek API | 简历-岗位匹配分析 |
| 消息推送 | PushPlus API | 微信消息推送 |

### 💡 面试要点 / Interview Talking Points

**1. 为什么不直接用招聘平台的 API？**
- 主流招聘平台（Boss 直聘、拉勾等）没有公开 API，且反爬严格
- DuckDuckGo Search 是免费、无需认证的搜索接口，适合做 demo
- 生产环境可以换用招聘平台 API 或招聘数据聚合服务

**2. AI 匹配分析怎么做才靠谱？**
- 关键是 **prompt 工程**：结构化地传入简历和岗位 JD，要求 AI 逐维度评估
- 不只是关键词匹配，而是让 AI **理解语义**（比如"熟悉 Python"和"Python 开发经验"是同一个意思）
- 通过 few-shot 示例引导输出格式，确保结果结构化

**3. 微信推送的实现原理？**
- PushPlus 是一个微信公众号消息推送服务
- 本质是 HTTP POST 请求，body 包含 token + 消息内容
- 缺点：每个用户需要单独关注公众号；优点：免费、实现简单

**4. 这个项目的实际价值？**
- 展示了**全链路 AI 应用**能力：数据采集 → AI 分析 → 消息推送
- 体现了"用 AI 解决实际问题"的思路，不只是调 API
- 可以扩展为自动化求职工具，每天定时搜索 + 推送

### ⚠️ 搭建中可能遇到的问题 / Troubleshooting

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 搜索不到结果 | DuckDuckGo 对中文招聘关键词支持有限 | 尝试不同关键词组合，加引号精确搜索 |
| 搜索结果不准确 | DuckDuckGo 返回非招聘页面 | 在解析时增加域名/标题过滤逻辑 |
| AI 分析结果过长 | LLM 输出未限制 | 在 prompt 中要求"简洁输出，每岗位不超过 5 行" |
| 微信推送失败 | Token 过期或消息过长 | 检查 Token 是否有效，PushPlus 单条消息限制 |
| BeautifulSoup 解析报错 | 网页结构变化 | 增加异常处理，用 try-except 包裹解析逻辑 |
| DuckDuckGo 被限流 | 请求频率过高 | 加入请求间隔（time.sleep），或换用其他搜索引擎 |

### 🚀 扩展方向 / Future Enhancements

- **定时自动搜索** — 每天定时执行搜索 + 分析 + 推送（APScheduler）
- **多平台搜索** — 接入 Boss 直聘、拉勾、猎聘的搜索结果（需处理反爬）
- **简历优化建议** — AI 根据目标岗位 JD，给出简历修改建议
- **面试题预测** — 根据岗位要求，AI 生成可能的面试题和参考答案
- **薪资谈判助手** — 基于市场数据分析，给出薪资期望建议
- **投递追踪** — 记录已投递的岗位，跟踪面试进度
- **多人协作** — 支持团队共享岗位信息，协同筛选

---

<a id="english"></a>
## 🇬🇧 English

> An intelligent job search assistant that finds positions across the web, analyzes fit using AI matching, and pushes results directly to your WeChat. Upload your resume once, and let AI do the hunting.

### Use Cases

- **Passive Job Monitoring** — Set up target position, run daily, get matches pushed to WeChat
- **Resume-Job Matching** — AI evaluates each job's fit score based on your skills and experience
- **Multi-city Search** — Search across different cities and industries simultaneously
- **Interview Preparation** — AI analysis helps you understand what each company is looking for

### Key Differentiator

This tool **automates the entire pipeline**: search → filter → AI analysis → WeChat notification. The AI understands job requirements holistically and compares them against your actual resume, not just keyword matching.

### Features

- 🔍 **Web Job Search** — Searches job listings via DuckDuckGo
- 🤖 **AI Matching Analysis** — DeepSeek evaluates each job against your resume
- 📄 **Resume Upload** — Upload .txt or .md resume for personalized matching
- 📱 **WeChat Push** — One-click push via PushPlus
- 📊 **Match Score** — 0-100 fit score with detailed reasoning
- 📋 **Batch Analysis** — Comprehensive summary across multiple jobs

### Architecture

```
┌───────────────────────────────────────────────────────┐
│                 Streamlit Web UI                       │
│  ┌───────────┐  ┌────────────┐  ┌──────────────────┐ │
│  │  Resume   │  │  Search &  │  │  Results &       │ │
│  │  Upload   │  │  Analyze   │  │  Push to WeChat  │ │
│  └─────┬─────┘  └─────┬──────┘  └────────┬─────────┘ │
└────────┼──────────────┼──────────────────┼───────────┘
        │              │                  │
┌───────▼──────────────▼──────────────────▼───────────┐
│              Pipeline Modules                         │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ job_search  │  │ ai_analyzer  │  │ wechat_    │ │
│  │ .py         │  │ .py          │  │ notifier   │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────┘
        │                  │                   │
        ▼                  ▼                   ▼
┌──────────────┐  ┌────────────────┐  ┌──────────────┐
│ DuckDuckGo   │  │  DeepSeek API  │  │  PushPlus    │
│ Search API   │  │  (Match AI)    │  │  (WeChat)    │
└──────────────┘  └────────────────┘  └──────────────┘
```

### Quick Start

```bash
git clone https://github.com/SsllF8/ai-job-hunter.git
cd ai-job-hunter
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env  # Fill in your API keys
streamlit run app.py
```

### Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | ✅ | Your DeepSeek API key for AI analysis |
| `PUSHPLUS_TOKEN` | ✅ | Your PushPlus token for WeChat push notifications |

### Interview Talking Points

**1. Why not use job platform APIs directly?**
- Major platforms (Boss直聘, 拉勾) have no public APIs and strict anti-scraping
- DuckDuckGo Search is free, no auth needed — good for demos
- Production could switch to job data aggregation services

**2. How do you make AI matching reliable?**
- Key is **prompt engineering**: structured resume + JD input, require per-dimension evaluation
- Not just keyword matching — AI understands semantics
- Few-shot examples guide output format

**3. How does WeChat push work?**
- PushPlus is a WeChat public account push service
- Essentially HTTP POST with token + message body
- Pro: free and simple; Con: each user needs to follow the account

**4. What's the real value of this project?**
- Demonstrates **end-to-end AI application**: data collection → AI analysis → notification
- Shows "AI solving real problems" mindset, not just calling APIs

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No search results | DuckDuckGo limited Chinese job search | Try different keyword combinations |
| Irrelevant results | Non-job pages in results | Add domain/title filtering in parser |
| AI output too long | Unconstrained LLM output | Add length limit in system prompt |
| WeChat push fails | Expired token or long message | Check token validity, message size limits |
| Parse errors | Page structure changes | Add try-except around parsing |
| Rate limited | Too many requests | Add delays between requests |

### Future Enhancements

- **Scheduled Search** — Daily automated search + analysis + push (APScheduler)
- **Multi-platform Search** — Boss直聘, 拉勾, 猎聘 integration
- **Resume Optimization** — AI suggests improvements based on target JD
- **Interview Question Prediction** — Generate likely questions based on job requirements
- **Salary Negotiation** — Market data-driven salary recommendation
- **Application Tracking** — Track applied positions and interview progress
- **Team Collaboration** — Share job listings within a team

## 📄 License

This project is licensed under the MIT License.
