# Sentivize - Quick Start Script with Groq AI Integration (PowerShell)
# Run this script untuk setup lengkap

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   SENTIVIZE - GROQ AI INTEGRATION SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# [1/6] Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# [2/6] Check Virtual Environment
Write-Host "[2/6] Checking Virtual Environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✓ Virtual environment created!" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment found!" -ForegroundColor Green
}
Write-Host ""

# [3/6] Activate Virtual Environment
Write-Host "[3/6] Activating Virtual Environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Virtual environment activated!" -ForegroundColor Green
Write-Host ""

# [4/6] Install Dependencies
Write-Host "[4/6] Installing Dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

$packages = @(
    "groq",
    "vaderSentiment",
    "textblob",
    "PyPDF2",
    "python-docx",
    "streamlit",
    "pandas",
    "numpy",
    "plotly",
    "openpyxl"
)

pip install --quiet --upgrade pip
pip install --quiet $packages

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install some dependencies" -ForegroundColor Red
    Write-Host "Try running: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to continue anyway"
} else {
    Write-Host "✓ All dependencies installed!" -ForegroundColor Green
}
Write-Host ""

# [5/6] Run Integration Tests
Write-Host "[5/6] Running Integration Tests..." -ForegroundColor Yellow
python test_groq_integration.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠ Some tests failed. Check output above." -ForegroundColor Yellow
    Write-Host "The system should still work in basic mode." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✓ All tests passed!" -ForegroundColor Green
    Write-Host ""
}

# [6/6] Groq API Key Configuration
Write-Host "[6/6] Groq API Key Configuration..." -ForegroundColor Yellow
Write-Host ""

$hasKey = Read-Host "Do you have a Groq API key? (Y/N)"

if ($hasKey -eq "Y" -or $hasKey -eq "y") {
    Write-Host ""
    Write-Host "Please enter your Groq API key:" -ForegroundColor Cyan
    Write-Host "(Get one free at https://console.groq.com)" -ForegroundColor Gray
    $apiKey = Read-Host "> "
    
    if ($apiKey -ne "") {
        # Set for current session
        $env:GROQ_API_KEY = $apiKey
        
        # Set permanently
        [System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', $apiKey, 'User')
        
        Write-Host ""
        Write-Host "✓ API key saved successfully!" -ForegroundColor Green
        Write-Host "  - Current session: Set" -ForegroundColor Green
        Write-Host "  - Permanent: Set (User environment)" -ForegroundColor Green
        Write-Host ""
        
        # Verify
        Write-Host "Verifying API key..." -ForegroundColor Yellow
        python -c "from groq_config import get_groq_status; print('✓ Groq available!' if get_groq_status()['available'] else '✗ Key not detected')"
    } else {
        Write-Host "No API key entered - using traditional NLP mode" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "No problem! Get your free Groq API key at:" -ForegroundColor Cyan
    Write-Host "  https://console.groq.com" -ForegroundColor White
    Write-Host ""
    Write-Host "The system will run in traditional NLP mode for now." -ForegroundColor Yellow
    Write-Host "You can add the API key later by setting GROQ_API_KEY environment variable:" -ForegroundColor Gray
    Write-Host "  `$env:GROQ_API_KEY = 'your_key_here'" -ForegroundColor Gray
    Write-Host ""
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   SETUP COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 To start Sentivize:" -ForegroundColor Cyan
Write-Host "  1. Run: streamlit run app.py" -ForegroundColor White
Write-Host "  2. Or double-click: run.bat" -ForegroundColor White
Write-Host ""

Write-Host "🧪 To verify installation:" -ForegroundColor Cyan
Write-Host "  Run: python test_groq_integration.py" -ForegroundColor White
Write-Host ""

Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  - README_GROQ.md - Main documentation" -ForegroundColor White
Write-Host "  - GROQ_SETUP_GUIDE.md - Detailed setup guide" -ForegroundColor White
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press Enter to exit..."
Read-Host
