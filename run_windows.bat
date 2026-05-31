@echo off
echo.
echo  ==========================================
echo   MoodMatch — AI Music for Your Emotions
echo  ==========================================
echo.

:: Check if venv exists
if not exist "venv" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
)

:: Activate venv
echo [2/3] Activating virtual environment...
call venv\Scripts\activate

:: Check if dependencies installed
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo [3/3] Installing dependencies (first time only, may take 5-10 min)...
    pip install -r requirements.txt
) else (
    echo [3/3] Dependencies already installed.
)

echo.
echo  Starting MoodMatch at http://localhost:5000
echo  Press Ctrl+C to stop
echo.

python app.py
pause