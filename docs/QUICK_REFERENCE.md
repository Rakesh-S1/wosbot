# 🏔️ Wosland Bot - Quick Reference

## 🚀 Quick Start

### First Time Setup
```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
copy .env.example .env

# 3. Edit .env and add your Discord bot token

# 4. Run the bot
python bot.py
```

### Or Use Quick Start Script
```powershell
.\start.bat
```

---

## 📝 All Commands

### Server Age Tracking

```
!setserver <name> <YYYY-MM-DD>
```
Register a Whiteout Survival server
- Example: `!setserver State456 2024-01-15`

```
!serverage <name>
```
View detailed server information
- Shows: days active, season, SVS count, next SVS date, milestones

```
!listservers
```
List all registered servers in this Discord

```
!deleteserver <name>
```
Remove a server from tracking

```
!woshelp
```
Show help menu with all commands

---

## 📊 What Gets Tracked

### Server Information
- **Days Active**: Total days since server start
- **Weeks**: Number of complete weeks
- **Season**: Current season (90 days per season)
- **Expected SVS**: Estimated total SVS events (every 14 days)
- **Next SVS**: Predicted date of next State vs State
- **Days Until SVS**: Countdown to next SVS

### Milestones
- ✅ Week 1 Complete (7 days)
- ✅ First SVS (14 days)
- ✅ Month 1 Complete (30 days)
- ✅ 2 Months (60 days)
- ✅ Season 1 Complete (90 days)
- ✅ 6 Months (180 days)
- ✅ 1 Year Anniversary (365 days)

---

## 🎯 Example Workflow

### 1. Register Your Server
```
!setserver MyState 2024-10-15
```

### 2. Check Server Age
```
!serverage MyState
```

### 3. View All Servers
```
!listservers
```

---

## 🔧 Common Issues

### Bot not responding?
1. Check bot is online (green dot in Discord)
2. Verify "Message Content Intent" enabled in Developer Portal
3. Ensure bot has permissions in channel

### Token error?
1. Make sure `.env` file exists (not `.env.example`)
2. No extra spaces in token
3. Token should be: `DISCORD_TOKEN=actual_token_here`

### Can't find commands?
- Prefix is `!` (exclamation mark)
- Type `!woshelp` to see all commands

---

## 📁 Files

- `bot.py` - Main bot code
- `game_data.py` - Whiteout Survival data
- `requirements.txt` - Dependencies
- `.env` - Your bot token (SECRET!)
- `data/servers.json` - Server data storage

---

## 🔗 Useful Links

### Get Bot Token
[Discord Developer Portal](https://discord.com/developers/applications)

### Data Sources
- [WOS Nerds](https://wosnerds.com/) - Community data hub
- [OneChilledGamer](https://onechilledgamer.com/) - Verified costs
- [WOS Info](https://www.wos-info.com/war-research) - Calculators
- [WOS Wiki](https://www.whiteoutsurvival.wiki/) - Game mechanics

### Community
- [Reddit r/whiteoutsurvival](https://www.reddit.com/r/whiteoutsurvival/)
- [Facebook Community](https://www.facebook.com/groups/whiteoutsurvivalcommunity/)

---

## 🎮 Coming Soon

- [ ] Research cost calculator
- [ ] SVS statistics tracking
- [ ] Troop cost calculator
- [ ] Event calendar
- [ ] Alliance tools
- [ ] Hero recommendations

---

**Made with ❄️ by the WOS community**
