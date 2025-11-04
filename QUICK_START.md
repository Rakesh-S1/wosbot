# Quick Deployment Commands

## For Linux System

### Initial Setup:
```bash
# 1. Clone repository
git clone https://github.com/Rakesh-S1/wosbot.git
cd wosbot

# 2. Create .env file
cp .env.example .env
nano .env  # Add your DISCORD_TOKEN and set AUTO_UPDATE=true

# 3. Make start script executable
chmod +x start.sh

# 4. Run the bot
bash start.sh
```

### Run as Background Service (Recommended):
```bash
# 1. Edit service file with your paths
nano wosbot.service

# 2. Create logs directory
mkdir -p logs

# 3. Install service
sudo cp wosbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable wosbot
sudo systemctl start wosbot

# 4. Check status
sudo systemctl status wosbot

# 5. View logs
sudo journalctl -u wosbot -f
```

### Service Management:
```bash
sudo systemctl start wosbot      # Start
sudo systemctl stop wosbot       # Stop
sudo systemctl restart wosbot    # Restart
sudo systemctl status wosbot     # Check status
sudo journalctl -u wosbot -f     # View real-time logs
```

## For Windows System

### Initial Setup:
```powershell
# 1. Clone repository
git clone https://github.com/Rakesh-S1/wosbot.git
cd wosbot

# 2. Create .env file
copy .env.example .env
notepad .env  # Add your DISCORD_TOKEN and set AUTO_UPDATE=true

# 3. Run the bot
start.bat
```

### Run as Windows Service (using NSSM):
```powershell
# 1. Download NSSM from https://nssm.cc/download
# 2. Install service
nssm install wosbot "C:\path\to\wosbot\start.bat"

# 3. Configure service
nssm set wosbot AppDirectory "C:\path\to\wosbot"
nssm set wosbot Description "Wosland Discord Bot"
nssm set wosbot Start SERVICE_AUTO_START

# 4. Start service
nssm start wosbot
```

## Production .env Configuration

For deployment, your `.env` should look like:
```
DISCORD_TOKEN=your_actual_token_here
CLEAR_COMMANDS=false
AUTO_UPDATE=true
```

## Auto-Update Feature

When `AUTO_UPDATE=true`:
- Bot automatically runs `git pull` on startup
- Fetches latest code from GitHub
- Perfect for production deployments
- Make sure Git credentials are configured

For local development, keep `AUTO_UPDATE=false`
