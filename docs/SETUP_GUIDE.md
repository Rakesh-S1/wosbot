# 🏔️ Wosland Discord Bot - Setup Guide

A Python Discord bot for **Whiteout Survival** with verified game data from community sources.

## ✅ **Step 1: Installation**

### Install Python Dependencies

Open PowerShell in the `wosbot` folder and run:

```powershell
pip install -r requirements.txt
```

This installs:
- `discord.py` - Discord bot framework
- `python-dotenv` - Environment variable management
- `aiohttp` - Async HTTP client

## 🔑 **Step 2: Get Your Discord Bot Token**

### 1. Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Give it a name (e.g., "Wosland Bot")
4. Click **"Create"**

### 2. Create a Bot User

1. In your application, go to **"Bot"** tab (left sidebar)
2. Click **"Add Bot"** → **"Yes, do it!"**
3. Under **"Privileged Gateway Intents"**, enable:
   - ✅ **Message Content Intent**
4. Click **"Reset Token"** → **"Yes, do it!"**
5. Click **"Copy"** to copy your bot token
   - ⚠️ **KEEP THIS SECRET!** Never share it publicly

### 3. Set Bot Permissions

Under **"Bot"** tab, recommended settings:
- ✅ Public Bot (if you want others to invite it)
- ❌ Requires OAuth2 Code Grant (keep this off)

## 🌐 **Step 3: Invite Bot to Your Server**

### 1. Generate Invite Link

1. In Developer Portal, go to **"OAuth2"** → **"URL Generator"**
2. Select **Scopes**:
   - ✅ `bot`
3. Select **Bot Permissions**:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Read Messages/View Channels
   - ✅ Use Slash Commands (optional)
4. Copy the **Generated URL** at the bottom
5. Paste it in your browser
6. Select your Discord server
7. Click **"Authorize"**

## ⚙️ **Step 4: Configure the Bot**

### 1. Create Environment File

In PowerShell:
```powershell
Copy-Item .env.example .env
```

### 2. Add Your Bot Token

Open `.env` in a text editor (Notepad, VS Code, etc.) and replace:

```env
DISCORD_TOKEN=your_bot_token_here
```

With your actual token:

```env
DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GhJ4kL.xYz...
```

**Save the file!**

## 🚀 **Step 5: Run the Bot**

In PowerShell:

```powershell
python bot.py
```

You should see:
```
<YourBotName> has connected to Discord!
Bot is in 1 server(s)
```

## 📱 **Step 6: Test the Bot**

In any Discord channel where the bot has access, type:

```
!woshelp
```

You should see the help menu with all commands!

## 🎮 **Available Commands**

### Server Age Tracking

| Command | Description | Example |
|---------|-------------|---------|
| `!setserver <name> <date>` | Register a Whiteout Survival server | `!setserver State456 2024-10-15` |
| `!serverage <name>` | Get server age, SVS predictions, milestones | `!serverage State456` |
| `!listservers` | List all registered servers | `!listservers` |
| `!deleteserver <name>` | Remove a server from tracking | `!deleteserver State456` |
| `!woshelp` | Show all available commands | `!woshelp` |

### Example Usage

```
!setserver State456 2024-01-15
```
Bot responds with: ✅ Server registered

```
!serverage State456
```
Bot shows:
- 📅 Days active
- 📆 Weeks
- 🎯 Current season
- ⚔️ Expected SVS count
- 🗓️ Next SVS date (estimated)
- 🏆 Milestones reached

## 📊 **Data Sources**

This bot uses verified data from:
- **WOS Nerds** (wosnerds.com) - Community data hub
- **OneChilledGamer** - Verified troop costs
- **WOS Info** - War Academy calculator
- **Whiteout Survival Wiki** - Official game mechanics

All research costs, SVS cycles, and game formulas are based on community-verified data.

## 🔧 **Troubleshooting**

### Bot doesn't respond to commands

**Check:**
1. ✅ Bot is online in Discord (green dot)
2. ✅ Bot has "Message Content Intent" enabled in Developer Portal
3. ✅ Bot has permissions to read/send messages in the channel
4. ✅ You're using the correct prefix: `!`

### "DISCORD_TOKEN not found" error

**Solution:**
1. Make sure you created `.env` file (not `.env.example`)
2. Verify token in `.env` has no extra spaces
3. Token should be on the line: `DISCORD_TOKEN=your_token_here`

### Bot connects but commands don't work

**Check:**
1. In Discord Developer Portal → Bot → Enable **"Message Content Intent"**
2. Restart the bot after enabling
3. Bot needs permission "Read Message History"

### Permission Error when starting

**Solution:**
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🌟 **Running 24/7**

To keep your bot online:

### Option 1: Local Computer
Use a task scheduler or run in background

### Option 2: Cloud Hosting (Recommended)
- **Heroku** (Free tier available)
- **DigitalOcean** ($5/month)
- **AWS Free Tier**
- **PythonAnywhere**
- **Repl.it**

## 📁 **Project Structure**

```
wosbot/
├── bot.py              # Main bot code
├── game_data.py        # Whiteout Survival game data
├── requirements.txt    # Python dependencies
├── .env               # Your bot token (DO NOT SHARE)
├── .env.example       # Template for .env
├── .gitignore         # Git ignore rules
├── data/              # Bot data storage
│   └── servers.json   # Server tracking data
├── README.md          # This file
└── SETUP_GUIDE.md     # This guide
```

## 🔒 **Security**

- ⚠️ **NEVER** share your `.env` file
- ⚠️ **NEVER** commit `.env` to GitHub
- ⚠️ The `.gitignore` file prevents this automatically
- If you accidentally expose your token, **reset it immediately** in Developer Portal

## 🆘 **Need Help?**

1. Check this guide again
2. Verify all steps completed
3. Check Discord Developer Portal settings
4. Ensure bot is in your server
5. Test with `!woshelp` command

## 🎯 **What's Next?**

Coming soon:
- Research cost calculator
- SVS statistics tracking
- Troop cost calculator
- Event reminders
- Alliance tools

## 📜 **Credits**

- Data sources: WOS Nerds, OneChilledGamer, WOS Info, WOS Wiki
- Community contributions from Whiteout Survival players
- Not affiliated with Whiteout Survival or Century Games

---

**Made by WOS players, for WOS players** 🏔️
