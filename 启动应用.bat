@echo off
cd /d %~dp0
call .venv\Scripts\activate
echo ========================================
echo   AI 智能求职助手 启动中...
echo ========================================
echo.
start http://localhost:8502
streamlit run app.py --server.port 8502
pause
