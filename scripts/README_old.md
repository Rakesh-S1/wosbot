# 🏔️ Wosland Discord Bot - Whiteout Survival Tools

A Discord bot for tracking Whiteout Survival server age, milestones, and SVS schedules with **verified community data**.

## ✨ Features

- **Server Age Tracking**: Track multiple Whiteout Survival servers with their start dates
- **Automatic Calculations**: Days active, weeks, seasons, expected SVS count
- **Next SVS Prediction**: Estimates when the next State vs State event will occur (14-day cycles)
- **Milestone Tracking**: Shows important milestones based on server age
- **Multi-Server Support**: Track multiple servers in one Discord server
- **Persistent Data**: Server information is saved and persists between bot restarts
- **Verified Game Data**: Uses accurate data from WOS Nerds, OneChilledGamer, WOS Info, and official wiki

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!setserver <name> <date>` | Register a server with its start date | `!setserver State456 2024-10-15` |
| `!serverage <name>` | Get detailed server timeline with events | ````
!serverage State456
```
Bot shows comprehensive timeline:
- 📊 Server age (days, weeks, season)
- ⭐ Current hero generation (Gen 1-13+)
- ⚔️ Total SVS events occurred
- 🗓️ Next SVS date prediction
- 🎊 Next major unlock with countdown
- ✅ Recent achievements (last 5 events)
- 🔮 Coming soon (next 3 events)

### View Full Timeline
```
!timeline State456
```
Shows all unlocked hero generations, major features, and upcoming events

## 📊 What Gets Tracked` |
| `!timeline <name>` | View full detailed timeline | `!timeline State456` |
| `!listservers` | List all registered servers | `!listservers` |
| `!deleteserver <name>` | Remove a server from tracking | `!deleteserver State456` |
| `!woshelp` | Show all available commands | `!woshelp` |

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A Discord account
- Administrator access to a Discord server (to add the bot)

### Step 1: Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "Wosland Bot")
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot" and confirm
5. Under "Privileged Gateway Intents", enable:
   - ✅ Message Content Intent
6. Click "Reset Token" and copy your bot token (keep it secret!)

### Step 2: Install Dependencies

1. Open a terminal/command prompt in the bot directory
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Configure the Bot

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` in a text editor and add your bot token:
   ```
   DISCORD_TOKEN=your_actual_bot_token_here
   ```

### Step 4: Invite Bot to Your Server

1. Go back to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Go to "OAuth2" → "URL Generator"
4. Select scopes:
   - ✅ `bot`
5. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Read Messages/View Channels
6. Copy the generated URL and open it in your browser
7. Select your server and authorize the bot

### Step 5: Run the Bot

```bash
python bot.py
```

You should see a message: `[BotName] has connected to Discord!`

## 💡 Usage Examples

### Register Your First Server
```
!setserver State123 2024-01-15
```

### Check Server Age
```
!serverage State123
```

The bot will show:
- Days active
- Number of weeks
- Current season
- Expected SVS count
- Next SVS date (estimated)
- Milestones reached

### List All Servers
```
!listservers
```

### Remove a Server
```
!deleteserver State123
```

## 📊 What Gets Tracked

- **Server Start Date**: The date your server was created
- **Days Active**: Total days since server started
- **Weeks**: Number of complete weeks
- **Season**: Current season (90 days per season)
- **Expected SVS**: Estimated number of SVS events (every 14 days)
- **Next SVS**: Predicted date of next State vs State event
- **Milestones**: 
  - Week 1 completion
  - First SVS
  - Month 1
  - 2 Months
  - Season 1
  - 6 Months
  - 1 Year

## 🗂️ Data Storage

Server data is stored locally in `data/servers.json`. Each Discord server has its own set of tracked Whiteout Survival servers.

## 🛠️ Troubleshooting

### Bot doesn't respond to commands
- Make sure the bot has permissions to read and send messages in the channel
- Verify "Message Content Intent" is enabled in the Developer Portal
- Check that the bot is online (you should see it in the member list)

### "DISCORD_TOKEN not found" error
- Make sure you created a `.env` file (not `.env.example`)
- Verify your token is correct and has no extra spaces

### Commands work but nothing happens
- Check the bot has "Embed Links" permission
- Verify the bot can see the channel you're typing in

## 📝 Notes

- SVS timing is estimated based on typical 14-day cycles
- Actual SVS dates may vary depending on your server
- Data is stored per Discord server (guild), so different Discord servers can track different game servers

## 🔄 Keeping the Bot Running 24/7

For production use, consider:
- Using a hosting service (Heroku, DigitalOcean, AWS, etc.)
- Running as a system service
- Using tools like PM2 or systemd to auto-restart on crashes

## 📜 License

MIT License - Feel free to modify and use as needed!

## 🤝 Contributing

This is a community tool for Whiteout Survival players. Feel free to suggest features or improvements!

---

**Not affiliated with Whiteout Survival or its developers. This is an unofficial community tool.**
