@echo off
title Launching PharmaShield Servers...

cd /d "%~dp0"
echo [1/2] Starting Backend Server (FastAPI on Port 8000)...
start "PharmaShield-Backend" python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

cd /d "%~dp0frontend"
echo [2/2] Starting Frontend Server (Next.js on Port 3000)...
start "PharmaShield-Frontend" npm run dev

echo.
echo Both servers launched successfully!
echo Frontend: http://localhost:3000
echo Backend: http://127.0.0.1:8000/docs

