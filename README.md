# 🤖 AI 智能求职助手

> 基于 AI 的智能岗位搜索与匹配分析工具，帮助求职者快速找到合适的岗位并推送到微信。

## ✨ 功能特性

- 🔍 **智能搜索** — 通过 DuckDuckGo 搜索引擎实时搜索招聘信息
- 🧠 **AI 匹配分析** — DeepSeek AI 分析岗位匹配度，生成个性化建议
- 📄 **简历上传** — 上传个人简历，AI 基于简历内容进行精准匹配
- 📲 **微信推送** — 通过 PushPlus 将搜索结果推送到微信
- 🏙️ **多维度筛选** — 支持城市/区域、薪资范围、工作类型等条件筛选

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| DeepSeek API | AI 智能分析 |
| DuckDuckGo Search | 免费搜索引擎 |
| PushPlus | 微信消息推送 |
| Streamlit | Web 界面框架 |
| python-dotenv | 环境变量管理 |

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/SsllF8/ai-job-hunter.git
cd ai-job-hunter
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
copy .env.example .env
```

需要配置：
- `DEEPSEEK_API_KEY` — [DeepSeek 开放平台](https://platform.deepseek.com/) 申请
- `PUSHPLUS_TOKEN` — [PushPlus](https://www.pushplus.plus/) 微信扫码登录获取

### 4. 运行

```bash
streamlit run app.py
```

或者双击 `启动应用.bat`。

## 📖 使用方法

1. 在左侧边栏填写搜索条件（关键词、城市、区域、薪资等）
2. 可选：上传个人简历（.txt 或 .md 格式）
3. 点击「🚀 开始搜索与分析」
4. 查看搜索结果和 AI 分析报告
5. 点击「📲 推送到微信」将结果发送到微信

## 🔧 项目结构

```
ai-job-hunter/
├── app.py              # Streamlit 主界面
├── job_search.py       # 岗位搜索模块（DuckDuckGo）
├── ai_analyzer.py      # AI 分析模块（DeepSeek）
├── wechat_notifier.py  # 微信推送模块（PushPlus）
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板
└── 启动应用.bat         # Windows 启动脚本
```

## 📄 License

MIT
