#!/bin/bash
echo ""
echo " =========================================="
echo "  MoodMatch — AI Music for Your Emotions"
echo " =========================================="
echo ""

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
echo "[2/3] Activating virtual environment..."
source venv/bin/activate

# Install if needed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[3/3] Installing dependencies (first time only)..."
    pip install -r requirements.txt
else
    echo "[3/3] Dependencies already installed."
fi

echo ""
echo " 🎵 Starting MoodMatch at http://localhost:5000"
echo " Press Ctrl+C to stop"
echo ""

python app.py