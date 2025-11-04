# Scripts & Utilities

This folder contains utility scripts and backup files.

## 🔧 Utility Scripts

### `clear_and_sync.bat` (Windows)
Clears old Discord commands and syncs new ones. Use when commands show as "outdated" or when you add/modify commands.

**Usage:**
```bash
cd scripts
.\clear_and_sync.bat
```

### `clear_and_sync.sh` (Linux/Mac)
Same as above but for Unix systems.

**Usage:**
```bash
cd scripts
chmod +x clear_and_sync.sh
./clear_and_sync.sh
```

### `start.sh` (Linux/Mac)
Main startup script for Linux/Mac systems. Sets up virtual environment, installs dependencies, and runs the bot.

**Usage:**
```bash
cd scripts
chmod +x start.sh
./start.sh
```

### `clear_commands.py` (Deprecated)
Old manual command clearing script. Use `clear_and_sync.bat/sh` instead.

## 📦 Backup Files

- `bot_old.py` - Backup of old monolithic bot.py (before reorganization)
- `README_old.md` - Backup of old README
