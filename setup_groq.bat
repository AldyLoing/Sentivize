@echo off
REM Sentivize - Quick Start Script dengan Groq AI Integration
REM Run this script untuk setup lengkap

echo.
echo ============================================================
echo    SENTIVIZE - GROQ AI INTEGRATION SETUP
echo ============================================================
echo.

echo [1/6] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo OK!
echo.

echo [2/6] Checking Virtual Environment...
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
) else (
    echo Virtual environment found!
)
echo.

echo [3/6] Activating Virtual Environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo OK!
echo.

echo [4/6] Installing Dependencies...
echo This may take a few minutes...
pip install -q groq vaderSentiment textblob PyPDF2 python-docx streamlit pandas numpy plotly openpyxl
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo All dependencies installed!
echo.

echo [5/6] Running Integration Tests...
python test_groq_integration.py
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed. Check output above.
    echo The system should still work in basic mode.
    echo.
) else (
    echo.
    echo All tests passed!
    echo.
)

echo [6/6] Groq API Key Configuration...
echo.
echo Do you have a Groq API key? (Y/N)
set /p has_key="> "

if /i "%has_key%"=="Y" (
    echo.
    echo Please enter your Groq API key:
    echo (Get one free at https://console.groq.com)
    set /p api_key="> "
    
    if not "%api_key%"=="" (
        setx GROQ_API_KEY "%api_key%" >nul
        set GROQ_API_KEY=%api_key%
        echo.
        echo API key saved successfully!
        echo.
    ) else (
        echo No API key entered - using traditional NLP mode
    )
) else (
    echo.
    echo No problem! Get your free Groq API key at:
    echo https://console.groq.com
    echo.
    echo The system will run in traditional NLP mode for now.
    echo You can add the API key later by setting GROQ_API_KEY environment variable.
    echo.
)

echo.
echo ============================================================
echo    SETUP COMPLETE!
echo ============================================================
echo.
echo To start Sentivize:
echo   1. Run: streamlit run app.py
echo   2. Or double-click: run.bat
echo.
echo To verify installation:
echo   Run: python test_groq_integration.py
echo.
echo Documentation:
echo   - README_GROQ.md - Main documentation
echo   - GROQ_SETUP_GUIDE.md - Detailed setup guide
echo.
echo ============================================================
echo.

pause
