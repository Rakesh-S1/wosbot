#!/bin/bash

echo "======================================="
echo " WOS Bot - Quick Setup"
echo "======================================="
echo ""

# Check for --clear argument
CLEAR_MODE=false
if [ "$1" == "--clear" ] || [ "$1" == "-c" ]; then
    CLEAR_MODE=true
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

echo "[1/5] Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment found!"
fi

echo ""
echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

echo ""
echo "[3/5] Checking and installing dependencies..."
echo "Verifying all requirements are installed..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "All dependencies are installed!"

echo ""
echo "[4/5] Checking for .env file..."
if [ ! -f ".env" ]; then
    echo ".env file not found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "[ACTION REQUIRED]"
    echo "Please edit .env file and add your Discord bot token"
    echo "Then run this script again"
    exit 0
fi

echo ""
echo "Checking .env configuration..."
if grep -q "your_bot_token_here" .env; then
    echo "[WARNING] .env file still has placeholder token"
    echo "Please edit .env and add your real Discord bot token"
    exit 0
fi

echo ""
echo "[5/5] Starting bot..."
echo ""

# Set CLEAR_COMMANDS in .env if --clear was used
if [ "$CLEAR_MODE" == "true" ]; then
    echo "[CLEAR MODE] Enabling command clearing..."
    sed -i 's/CLEAR_COMMANDS=false/CLEAR_COMMANDS=true/' .env
    echo "This will clear outdated commands and sync new ones."
    echo ""
else
    # Check if CLEAR_COMMANDS is already set to true in .env
    if grep -q "CLEAR_COMMANDS=true" .env; then
        echo "[CLEAR MODE] Clearing old Discord commands..."
        echo "This will clear outdated commands and sync new ones."
        echo ""
    fi
fi

echo "Bot is running... Press Ctrl+C to stop"
echo "======================================="
echo ""
python3 bot.py

# Reset CLEAR_COMMANDS to false if we set it
if [ "$CLEAR_MODE" == "true" ]; then
    echo ""
    echo "Resetting CLEAR_COMMANDS to false..."
    sed -i 's/CLEAR_COMMANDS=true/CLEAR_COMMANDS=false/' .env
fi
