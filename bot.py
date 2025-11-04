"""
WOS Bot - Whiteout Survival Server Tracker
Main entry point for the Discord bot
"""
import discord
from discord.ext import commands
import os
import sqlite3
import subprocess
from dotenv import load_dotenv

from core.database import init_database
from commands import setup_all_commands


# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def check_and_scrape_if_needed():
    """Check if buildings database exists and has data, scrape if not"""
    db_path = 'data/buildings.db'
    
    # Use venv python if available, otherwise system python
    python_exe = 'venv/Scripts/python.exe' if os.path.exists('venv/Scripts/python.exe') else 'python'
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print('⚠️  Database not found! Running scraper...')
        print('='*60)
        result = subprocess.run([python_exe, 'tools/scrape_buildings.py'], 
                              capture_output=False, text=True)
        if result.returncode != 0:
            print('❌ Scraping failed!')
            return False
        print('='*60)
        print('✅ Database created successfully!')
        return True
    
    # Check if database has data
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM buildings')
        building_count = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM levels')
        level_count = cur.fetchone()[0]
        conn.close()
        
        if building_count == 0 or level_count == 0:
            print('⚠️  Database is empty! Running scraper...')
            print('='*60)
            result = subprocess.run([python_exe, 'tools/scrape_buildings.py'], 
                                  capture_output=False, text=True)
            if result.returncode != 0:
                print('❌ Scraping failed!')
                return False
            print('='*60)
            print('✅ Database populated successfully!')
            return True
        
        print(f'✅ Database ready: {building_count} buildings, {level_count} levels')
        return True
        
    except Exception as e:
        print(f'⚠️  Database error: {e}')
        print('Running scraper...')
        print('='*60)
        result = subprocess.run([python_exe, 'tools/scrape_buildings.py'], 
                              capture_output=False, text=True)
        if result.returncode != 0:
            print('❌ Scraping failed!')
            return False
        print('='*60)
        print('✅ Database recreated successfully!')
        return True


@bot.event
async def on_ready():
    """Bot startup event"""
    print(f'✅ {bot.user} is now online!')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    
    # Check database and scrape if needed
    if not check_and_scrape_if_needed():
        print('❌ Failed to initialize database!')
        await bot.close()
        return
    
    # Initialize database
    init_database()
    print('✅ Database initialized')
    
    # Check for --clear flag to clear old commands
    clear_mode = os.getenv('CLEAR_COMMANDS', 'false').lower() == 'true'
    
    if clear_mode:
        print('🔄 Clearing old commands from Discord...')
        bot.tree.clear_commands(guild=None)
        print('✅ Old commands cleared locally')
    
    # Register all commands (always do this, even after clearing)
    await setup_all_commands(bot)
    
    # Sync slash commands with Discord
    try:
        print('🔄 Syncing commands to Discord...')
        synced = await bot.tree.sync()
        print(f'✨ Synced {len(synced)} slash command(s) globally')
    except Exception as e:
        print(f'❌ Failed to sync commands: {e}')
        import traceback
        traceback.print_exc()
    
    print('🏔️ Ready to track server timelines!')


def main():
    """Run the bot"""
    if not TOKEN:
        print('❌ Error: DISCORD_TOKEN not found in .env file!')
        print('Please create a .env file with your bot token.')
        return
    
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print('❌ Error: Invalid bot token!')
    except Exception as e:
        print(f'❌ Error starting bot: {e}')


if __name__ == '__main__':
    main()
