"""
Clear and re-sync all Discord slash commands
Run this when commands are showing as "outdated"
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Clear old commands and sync new ones"""
    print(f'✅ {bot.user} is now online!')
    print('🔄 Clearing old commands...')
    
    try:
        # Clear all global commands
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        print('✅ Cleared all global commands')
        
        # Clear guild-specific commands for all guilds
        for guild in bot.guilds:
            bot.tree.clear_commands(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f'✅ Cleared commands for guild: {guild.name}')
        
        print('')
        print('✨ All old commands cleared!')
        print('Now restart the bot normally with start.bat to register new commands')
        print('')
        
    except Exception as e:
        print(f'❌ Error: {e}')
    
    # Close the bot
    await bot.close()


# Run the bot
if __name__ == '__main__':
    if not TOKEN:
        print('❌ Error: DISCORD_TOKEN not found in .env file!')
    else:
        bot.run(TOKEN)
