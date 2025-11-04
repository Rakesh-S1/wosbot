#!/bin/bash

echo "======================================="
echo " Wosland Discord Bot - Quick Setup"
echo "======================================="
echo ""

# Parse command line arguments
CLEAR_MODE=false
UPDATE_MODE=false

for arg in "$@"; do
    case $arg in
        --clear|-c)
            CLEAR_MODE=true
            ;;
        --no-update)
            UPDATE_MODE=false
            ;;
    esac
done

# Check for AUTO_UPDATE in .env (for production)
if [ -f .env ]; then
    if grep -q "AUTO_UPDATE=true" .env; then
        UPDATE_MODE=true
    fi
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

echo "[1/6] Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "      Python version: $PYTHON_VERSION"

# Auto-update from Git if enabled
if [ "$UPDATE_MODE" = true ]; then
    echo ""
    echo "[2/6] Auto-updating from Git..."
    echo "      Running: git pull origin main"
    
    if git pull origin main; then
        echo "      ✓ Code updated successfully"
    else
        echo "      ✗ Git pull failed - continuing with existing code"
    fi
else
    echo ""
    echo "[2/6] Skipping auto-update (AUTO_UPDATE=false)"
fi

echo ""
echo "[3/6] Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "      Creating virtual environment..."
    python3 -m venv venv
    echo "      ✓ Virtual environment created"
else
    echo "      ✓ Virtual environment exists"
fi

echo ""
echo "[4/6] Activating virtual environment..."
source venv/bin/activate
echo "      ✓ Virtual environment activated"

echo ""
echo "[5/6] Installing/updating dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "      ✓ Dependencies installed"

echo ""
echo "[6/6] Starting bot..."

# Set CLEAR_COMMANDS if --clear flag was used
if [ "$CLEAR_MODE" = true ]; then
    export CLEAR_COMMANDS=true
    echo "      [CLEAR MODE] Will clear old slash commands"
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "[ERROR] .env file not found!"
    echo "Please create a .env file with your DISCORD_TOKEN"
    echo ""
    echo "Example .env file:"
    echo "  DISCORD_TOKEN=your_token_here"
    echo "  CLEAR_COMMANDS=false"
    echo "  AUTO_UPDATE=false"
    echo ""
    exit 1
fi

echo "      Loading environment from .env"
echo ""
echo "======================================="
echo " Bot is starting..."
echo "======================================="
echo ""

# Run the bot
python3 bot.py

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "======================================="
    echo " Bot stopped with an error"
    echo "======================================="
    read -p "Press Enter to exit..."
fi
