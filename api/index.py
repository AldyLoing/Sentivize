"""
Vercel serverless function wrapper for Streamlit
This creates a bridge between Vercel's serverless environment and Streamlit
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from starlette.applications import Starlette
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import subprocess
import signal
import atexit

# Store the Streamlit process
streamlit_process = None

def start_streamlit():
    """Start Streamlit in background"""
    global streamlit_process
    if streamlit_process is None:
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            "app_ultra.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false"
        ])
        atexit.register(lambda: streamlit_process.kill() if streamlit_process else None)

def stop_streamlit():
    """Stop Streamlit process"""
    global streamlit_process
    if streamlit_process:
        streamlit_process.send_signal(signal.SIGTERM)
        streamlit_process = None

async def homepage(request):
    """Redirect to Streamlit app"""
    start_streamlit()
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="3;url=http://localhost:8501">
        <title>Sentivize - Loading...</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                text-align: center;
                padding: 2rem;
            }
            .spinner {
                border: 4px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top: 4px solid white;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 1rem;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            h1 { margin: 0 0 1rem; font-size: 2.5rem; }
            p { margin: 0.5rem 0; opacity: 0.9; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="spinner"></div>
            <h1>🚀 Sentivize</h1>
            <p>AI-Powered HR Analytics Platform</p>
            <p>Starting application...</p>
            <p style="font-size: 0.9rem; margin-top: 2rem;">
                If not redirected automatically, <a href="http://localhost:8501" style="color: white;">click here</a>
            </p>
        </div>
    </body>
    </html>
    """)

async def health(request):
    """Health check endpoint"""
    return HTMLResponse("OK", status_code=200)

# Define routes
routes = [
    Route("/", endpoint=homepage),
    Route("/health", endpoint=health),
]

# Create Starlette app
app = Starlette(debug=False, routes=routes)

# For Vercel
def handler(request, context):
    """Vercel serverless function handler"""
    return app(request, context)
