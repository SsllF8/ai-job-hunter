# 🎯 AI Job Hunter

> An intelligent job search assistant that finds positions across the web, analyzes fit using AI matching, and pushes results directly to your WeChat. Upload your resume once, and let AI do the hunting.

![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red?logo=streamlit)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-blue)
![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Search-green)
![WeChat](https://img.shields.io/badge/PushPlus-WeChat-07c160?logo=wechat)

## 🎯 Use Cases

### Job Seeker Scenarios
- **Passive Job Monitoring** — Set up your target position (e.g., "AI product manager in Shenzhen"), run a search, and get matching jobs pushed to WeChat instantly. Repeat daily to stay on top of new postings
- **Resume-Job Matching** — Upload your resume and let the AI evaluate each job's fit score based on your skills, experience, and career goals, so you only apply to the most relevant positions
- **Multi-city Job Search** — Search across different cities and industries simultaneously, compare opportunities side by side
- **Interview Preparation** — Use the AI analysis to understand what each company is looking for, so you can tailor your resume and interview talking points

### Career Development Scenarios
- **Market Research** — Search for roles you're interested in and let the AI summarize salary ranges, required skills, and industry trends
- **Career Pivoting** — Upload your current resume and search for roles in a different field — the AI will identify skill gaps and highlight transferable experience
- **Fresh Graduate** — With limited experience, use the AI to find entry-level positions where your background has the best match

### Key Differentiator
Traditional job boards require manual browsing and subjective judgment. This tool **automates the entire pipeline**: search → filter → AI analysis → WeChat notification. The AI doesn't just match keywords — it understands job requirements holistically and compares them against your actual resume.

## ✨ Features

### Core Capabilities
- 🔍 **Web Job Search** — Searches job listings across multiple platforms via DuckDuckGo
- 🤖 **AI Matching Analysis** — DeepSeek evaluates each job against your resume/skills profile
- 📄 **Resume Upload** — Upload a text/Markdown resume for personalized matching
- 📱 **WeChat Push** — One-click push of matched job results via PushPlus to WeChat
- 📊 **Match Score** — Each job gets a 0-100 fit score with detailed reasoning
- 📋 **Batch Analysis** — Analyze multiple jobs at once with a comprehensive summary report

### Analysis Report Includes
For each matched job:
- **Match Score** (0-100) with breakdown
- **Skill Alignment** — Which of your skills match the requirements
- **Skill Gaps** — What you're missing and how important they are
- **Recommendation** — Should you apply? Why or why not?

Summary report across all jobs:
- Best matches ranked by score
- Common required skills across all positions
- Market insight and application strategy

## 🏗️ Architecture

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

## 📁 Project Structure

```
ai-job-hunter/
├── app.py                  # Streamlit web interface
├── job_search.py           # Job search & parsing module
├── ai_analyzer.py          # AI matching analysis engine
├── wechat_notifier.py      # WeChat push notification module
├── test_search.py          # Standalone search test script
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── 启动应用.bat             # Windows quick start
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- DeepSeek API Key ([Get one here](https://platform.deepseek.com))
- PushPlus Token ([Get one here](https://www.pushplus.plus) — scan QR code with WeChat)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/SsllF8/ai-job-hunter.git
cd ai-job-hunter

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and fill in your API keys

# 5. Run the application
streamlit run app.py
```

Or simply double-click `启动应用.bat` on Windows.

### How to Use

1. **Upload Resume** (optional) — Upload your resume in `.txt` or `.md` format from the sidebar. If you don't upload one, the system uses a default profile
2. **Search Jobs** — Enter your target position, location, and other filters, then click "🔍 搜索岗位"
3. **Analyze Matches** — Click "🤖 AI 智能分析" to run batch matching analysis on found jobs
4. **Push to WeChat** — Click "📱 推送到微信" to send results to your WeChat via PushPlus

## ⚙️ Configuration

Create a `.env` file based on `.env.example`:

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | ✅ | Your DeepSeek API key for AI analysis |
| `PUSHPLUS_TOKEN` | ✅ | Your PushPlus token for WeChat push notifications |

### Setting Up PushPlus (WeChat Push)
1. Visit [pushplus.plus](https://www.pushplus.plus)
2. Scan the QR code with WeChat to log in
3. Copy your token from the dashboard
4. Paste it into `.env` as `PUSHPLUS_TOKEN`

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | Streamlit | Interactive job search UI |
| Job Search | DuckDuckGo Search | Web scraping for job listings |
| HTML Parsing | BeautifulSoup + lxml | Extract structured job data from pages |
| AI Matching | DeepSeek API | Resume-job fit analysis |
| Push Notifications | PushPlus API | WeChat message delivery |

## 🔧 How It Works

### Search Pipeline
```
User Query (position + location)
  → DuckDuckGo search with targeted keywords
  → Scrape top job listing pages
  → Parse HTML to extract: title, company, salary, location, requirements
  → Display structured results
```

### Analysis Pipeline
```
Job listings + User Resume
  → Send to DeepSeek with structured prompt
  → AI evaluates: skill match, experience fit, growth potential
  → Generate match score (0-100) per job
  → Produce overall summary with recommendations
```

### Push Pipeline
```
Analysis results
  → Format as WeChat-friendly message (Markdown)
  → POST to PushPlus API
  → Message delivered to user's WeChat
```

## 📝 Example Searches

Try these search queries:
- "AI 产品经理 深圳"
- "Python 开发工程师 远程"
- "数据分析实习生 北京"
- "低代码开发 上海"
- "LLM 应用开发"

## 📄 License

This project is licensed under the MIT License.
