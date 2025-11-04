# 🏔️ WOS Bot - Whiteout Survival Server Tracker

A powerful Discord bot for tracking Whiteout Survival server ages, timelines, and events with automatic database-backed tracking.

## ✨ Features

- **📊 Accurate Age Calculation** - Uses VIP login streak for 100% precise server age
- **💾 Automatic Tracking** - Save servers once, bot auto-updates daily
- **📜 Detailed Timeline** - 40+ major events from launch to Day 800+
- **🎯 Upcoming Events** - See what's coming next for your server
- **🗄️ Database Backed** - SQLite database for persistent tracking
- **🔧 Modular Architecture** - Clean, maintainable codebase

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd wosbot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

4. **Run the bot:**

   **Windows:**
   ```bash
   start.bat
   ```
   
   **Clear commands (when you update/add commands):**
   ```bash
   start.bat --clear
   ```
   
   Or manually:
   ```bash
   python bot.py
   ```

   **Linux/Mac:**
   ```bash
   chmod +x scripts/start.sh
   ./scripts/start.sh
   ```
   
   **Clear commands:**
   ```bash
   ./scripts/start.sh --clear
   ```
   
   Or manually:
   ```bash
   python3 bot.py
   ```

## 📋 Commands

### Server Information
- `/age <state_id> <login_streak>` - Calculate server age from VIP login streak
- `/state <state_number>` - Estimate server age from state number (rough)

### Server Tracking
- `/addserver <state_id> <login_streak> [name]` - Add server for automatic tracking
- `/server <state_id>` - View tracked server's current timeline
- `/listservers` - List all tracked servers
- `/updateserver <state_id> <new_streak>` - Update reference point
- `/deleteserver <state_id>` - Remove server from tracking

### Help
- `/help` - Show all commands with examples

## 📁 Project Structure

```
wosbot/
├── bot.py                 # Main entry point (clean, ~60 lines)
├── commands/              # Modular command files
│   ├── __init__.py       # Command registration
│   ├── age_commands.py   # /age, /state commands
│   ├── server_commands.py # Database tracking commands
│   └── help_commands.py  # /help command
├── core/                  # Core functionality
│   ├── __init__.py       # Core exports
│   ├── database.py       # SQLite operations
│   └── game_data.py      # WOS game data & calculations
├── docs/                  # Documentation
│   ├── SETUP_GUIDE.md    # Detailed setup instructions
│   ├── USAGE_GUIDE.md    # Command usage examples
│   └── ...               # Additional guides
├── data/                  # Database storage
│   └── servers.db        # SQLite database (auto-created)
├── .env                   # Environment variables (create from .env.example)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎮 How It Works

### Login Streak = Server Age
The bot uses your **VIP login streak** (found in-game on the VIP page) as the exact server age in days. This is 100% accurate because:
- Login streak starts at 1 when server opens
- Increments by 1 each day
- Never resets unless you miss a login

### Reference Point Tracking
When you add a server with `/addserver`:
1. Bot saves the **current date** and **login streak**
2. Each time you check with `/server`, bot calculates:
   - Days since reference date
   - Current age = reference streak + days passed
3. No need to manually update - it auto-calculates!

### Example
```
Day 1: /addserver 1780 407
→ Saves: Date=2024-01-15, Streak=407

Day 10: /server 1780
→ Calculates: 407 + 9 days = 416 days old
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation and configuration
- **[Usage Guide](docs/USAGE_GUIDE.md)** - Command examples and workflows
- **[Database System](docs/DATABASE_SYSTEM.md)** - Database schema and reference tracking
- **[Timeline Feature](docs/TIMELINE_FEATURE.md)** - Event timeline details
- **[Login Streak Guide](docs/LOGIN_STREAK_GUIDE.md)** - Why login streak is accurate

## 🛠️ Development

### Adding New Commands
1. Create new file in `commands/` (e.g., `research_commands.py`)
2. Define `async def setup_research_commands(bot)`
3. Add command decorators: `@bot.tree.command(...)`
4. Import in `commands/__init__.py`
5. Add to `setup_all_commands()` function

### Modifying Game Data
- Edit `core/game_data.py`
- Update `DETAILED_TIMELINE` for new events
- Adjust calculations in helper functions

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source. Use freely for tracking WOS servers.

## 🐛 Troubleshooting

**Bot not responding?**
- Check bot has `applications.commands` OAuth2 scope
- Verify bot has proper permissions in your server
- Check console for error messages

**Commands not appearing?**
- Wait 1 hour for Discord to sync (or reinvite bot)
- Kick and reinvite bot with correct scopes

**Commands showing as "outdated"?**
- Run with clear flag: `.\start.bat --clear`
- Or manually: Set `CLEAR_COMMANDS=true` in `.env`, run bot, then set back to `false`
- Or use helper script: `.\scripts\clear_and_sync.bat`

**Database errors?**
- Check `data/` directory exists
- Verify write permissions

## 🔧 Clearing Commands

When you add/modify/remove commands, Discord needs to clear old command definitions. You have **3 options**:

### Option 1: Command Line (Quickest)
```bash
.\start.bat --clear
```

### Option 2: Environment Variable
Edit `.env`:
```
CLEAR_COMMANDS=true
```
Run `.\start.bat`, then change back to `false`

### Option 3: Helper Script
```bash
.\scripts\clear_and_sync.bat
```

All three methods do the same thing - choose what's easiest for you!

## 📞 Support

Need help? Check the [docs/](docs/) folder for detailed guides.

---
Made with ❄️ for the WOS community
