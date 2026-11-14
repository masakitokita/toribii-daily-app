@echo off
chcp 65001 > nul
echo 必要なライブラリを確認中...
pip install streamlit pandas --quiet
echo.
echo 炭火バル とりびぃーの 店舗管理アプリを起動します...
streamlit run app.py
pause
