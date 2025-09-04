@echo off
echo ========================================
echo    ArxivMind Simple System Startup
echo ========================================
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call "arXiv Mind\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install basic requirements
echo 📦 Installing requirements...
pip install fastapi uvicorn streamlit requests PyPDF2 python-multipart

REM Start backend in background
echo 🚀 Starting backend server...
start "ArxivMind Backend" python run_simple_backend.py

REM Wait for backend to start
echo ⏳ Waiting for backend to start...
timeout /t 8 /nobreak > nul

REM Check backend health
echo 🏥 Checking backend health...
python -c "import requests; r = requests.get('http://localhost:8000/health', timeout=5); print('✅ Backend is healthy!' if r.status_code == 200 else '❌ Backend check failed')" 2>nul
if errorlevel 1 (
    echo ⚠️  Backend health check failed, but continuing...
)

REM Start frontend
echo 🖥️  Starting frontend...
echo.
echo 🌐 Frontend will open at: http://localhost:8501
echo 🔧 Backend API docs at: http://localhost:8000/docs
echo.
streamlit run arxivmind/simple_app.py --server.port 8501

echo.
echo 🛑 System stopped
pause


