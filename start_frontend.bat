@echo off
echo 🧠 Starting ArxivMind Frontend...
echo.

REM Activate virtual environment
call "arXiv Mind\Scripts\activate.bat"

REM Install frontend requirements
echo Installing frontend requirements...
pip install streamlit plotly PyPDF2 requests

REM Start the Streamlit frontend
echo Starting Streamlit frontend...
echo.
echo 🌐 Frontend will be available at: http://localhost:8501
echo 🔗 Backend should be running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the frontend
echo.

streamlit run arxivmind/app.py --server.port 8501

pause
