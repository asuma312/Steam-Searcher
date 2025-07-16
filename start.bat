@echo off
rem
call .venv\Scripts\activate
start "" python run.py
start "" python kaggle_collector.py

rem
timeout /t 3 /nobreak

rem
cd app/frontend
npm run dev

pause