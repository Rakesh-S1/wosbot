#!/bin/bash

echo "======================================="
echo " Clear Discord Commands"
echo "======================================="
echo ""
echo "This will clear all old Discord commands"
echo "and sync new ones from your updated code."
echo ""
echo "Use this when:"
echo "  - Commands show as 'outdated'"
echo "  - You added/removed/changed commands"
echo "  - Discord shows old command versions"
echo ""
read -p "Press Enter to continue..."

# Go to parent directory (project root)
cd "$(dirname "$0")/.."

echo ""
echo "Setting CLEAR_COMMANDS=true..."

# Temporarily set the flag in .env
sed -i 's/CLEAR_COMMANDS=false/CLEAR_COMMANDS=true/' .env

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting bot with command clearing..."
python3 bot.py

echo ""
echo "Resetting CLEAR_COMMANDS=false..."
sed -i 's/CLEAR_COMMANDS=true/CLEAR_COMMANDS=false/' .env

echo ""
echo "Commands cleared! Restarting bot normally..."
sleep 2

echo ""
echo "Bot is running... Press Ctrl+C to stop"
echo "======================================="
echo ""
python3 bot.py
