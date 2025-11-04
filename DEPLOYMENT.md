# Deployment Guide

## Local Development Setup

1. Clone the repository
2. Copy `.env.example` to `.env`
3. Add your Discord bot token to `.env`
4. Keep `AUTO_UPDATE=false` in `.env`
5. Run `start.bat` (Windows) or `bash start.sh` (Linux)

## Production/Server Deployment

### Option 1: Windows Server

1. Clone the repository:
   ```powershell
   git clone https://github.com/Rakesh-S1/wosbot.git
   cd wosbot
   ```

2. Create `.env` file:
   ```powershell
   copy .env.example .env
   ```

3. Edit `.env` and configure:
   ```
   DISCORD_TOKEN=your_actual_bot_token
   CLEAR_COMMANDS=false
   AUTO_UPDATE=true
   ```

4. Run the bot:
   ```powershell
   start.bat
   ```

5. **Auto-restart on server reboot:**
   - Create a scheduled task in Windows Task Scheduler
   - Trigger: At system startup
   - Action: Start program `C:\path\to\wosbot\start.bat`
   - Or use NSSM (Non-Sucking Service Manager) to run as Windows service

### Option 2: Linux Server (Ubuntu/Debian)

1. Clone the repository:
   ```bash
   git clone https://github.com/Rakesh-S1/wosbot.git
   cd wosbot
   ```

2. Create `.env` file:
   ```bash
   cp .env.example .env
   nano .env  # or use vim/vi
   ```

3. Edit `.env` and configure:
   ```
   DISCORD_TOKEN=your_actual_bot_token
   CLEAR_COMMANDS=false
   AUTO_UPDATE=true
   ```

4. Make the startup script executable:
   ```bash
   chmod +x start.sh
   ```

5. Run the bot:
   ```bash
   bash start.sh
   ```

6. **Run as a systemd service (recommended for production):**
   
   a. Edit the `wosbot.service` file:
   ```bash
   nano wosbot.service
   ```
   
   b. Update the paths and username:
   ```ini
   User=your_username
   WorkingDirectory=/home/your_username/wosbot
   ExecStart=/home/your_username/wosbot/venv/bin/python3 /home/your_username/wosbot/bot.py
   EnvironmentFile=/home/your_username/wosbot/.env
   ```
   
   c. Create logs directory:
   ```bash
   mkdir -p logs
   ```
   
   d. Copy service file to systemd:
   ```bash
   sudo cp wosbot.service /etc/systemd/system/
   ```
   
   e. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable wosbot
   sudo systemctl start wosbot
   ```
   
   f. Check service status:
   ```bash
   sudo systemctl status wosbot
   ```
   
   g. View logs:
   ```bash
   # Real-time logs
   sudo journalctl -u wosbot -f
   
   # Or check log files
   tail -f logs/bot.log
   tail -f logs/bot-error.log
   ```
   
   h. Service management commands:
   ```bash
   sudo systemctl stop wosbot      # Stop the bot
   sudo systemctl restart wosbot   # Restart the bot
   sudo systemctl disable wosbot   # Disable auto-start
   ```

### Option 3: Cloud Hosting (Railway, Heroku, etc.)

1. Add a `Procfile`:
   ```
   worker: python bot.py
   ```

2. Set environment variables in the hosting dashboard:
   - `DISCORD_TOKEN=your_bot_token`
   - `AUTO_UPDATE=false` (cloud platforms handle deployments differently)

3. Connect your GitHub repository for auto-deployment

### Auto-Update Feature

When `AUTO_UPDATE=true` in `.env`:
- Bot will run `git pull origin main` on every restart
- Automatically gets the latest code from GitHub
- Updates dependencies if `requirements.txt` changed
- Perfect for production servers

When `AUTO_UPDATE=false` (default):
- No automatic git pulls
- Use for local development
- Manually control when to update code

### Deployment Workflow

1. **Develop locally** with `AUTO_UPDATE=false`
2. **Commit and push** changes to GitHub
3. **Restart production bot** - it will auto-update with `AUTO_UPDATE=true`

Or manually update production:
```powershell
git pull origin main
start.bat
```

### Keep Bot Running 24/7

**Windows:**
- Use Task Scheduler (startup trigger)
- Use NSSM to run as Windows service
- Use pm2-windows for process management

**Linux:**
- Use systemd service
- Use pm2 process manager
- Use screen/tmux sessions

### Monitoring

Check bot status:
- Discord bot appears online
- Check logs in terminal
- Database file exists: `data/buildings.db`

### Troubleshooting

**Auto-update not working:**
- Check git is installed: `git --version`
- Verify `.env` has `AUTO_UPDATE=true`
- Check git credentials are configured

**Bot not starting after update:**
- Check `requirements.txt` - may need to install new dependencies
- Database might need re-scraping (will happen automatically)
- Check for errors in terminal output
