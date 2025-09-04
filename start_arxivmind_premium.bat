@echo off
echo 🧠 Starting ArxivMind Premium - AI Research Assistant
echo ================================================
echo.

REM Activate virtual environment
echo 1️⃣ Activating virtual environment...
call "arXiv Mind\Scripts\activate.bat"

REM Install all requirements
echo.
echo 2️⃣ Installing requirements...
pip install -r requirements.txt
pip install -r backend/requirements.txt

REM Set OpenRouter API key
echo.
echo 3️⃣ Setting OpenRouter API key...
set OPENROUTER_KEY=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

REM Start backend in background
echo.
echo 4️⃣ Starting premium backend server...
echo    Backend will run on: http://localhost:8000
echo    API docs: http://localhost:8000/docs
echo.
start "ArxivMind Backend" cmd /k "python run_backend.py"

REM Wait for backend to start
echo 5️⃣ Waiting for backend to start...
timeout /t 10 /nobreak > nul

REM Check if backend is running
echo 6️⃣ Checking backend status...
python -c "import requests; r = requests.get('http://localhost:8000/health'); print('✅ Backend is running!' if r.status_code == 200 else '❌ Backend not responding')"

REM Start frontend
echo.
echo 7️⃣ Starting enhanced frontend...
echo    Frontend will run on: http://localhost:8501
echo    Backend API: http://localhost:8000
echo.
echo 🎉 ArxivMind Premium is starting up!
echo.
echo 🚀 Features Available:
echo    • Multi-model AI analysis (GPT-4, Claude 3.5, Gemini Pro, Llama 3.1)
echo    • arXiv paper search and analysis
echo    • Comparative paper analysis
echo    • AI-powered peer review
echo    • Interactive visualizations
echo.
echo 📖 Open these URLs in your browser:
echo    Frontend: http://localhost:8501
echo    Backend API: http://localhost:8000/docs
echo.
echo 💰 Budget: $2.00 (Use wisely!)
echo.
echo Press any key to start the frontend...
pause > nul

streamlit run arxivmind/app.py --server.port 8501

pause



