"""
Helper script to list custom emojis from your Discord server.
Run this after uploading the resource icons as custom emojis.
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.emojis = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"\n✅ Connected as {bot.user}")
    print("\n" + "="*60)
    print("Custom Emojis in your server(s):")
    print("="*60 + "\n")
    
    for guild in bot.guilds:
        print(f"📁 {guild.name} (ID: {guild.id})")
        print("-" * 60)
        
        emojis = guild.emojis
        if not emojis:
            print("  No custom emojis found")
        else:
            for emoji in sorted(emojis, key=lambda e: e.name):
                print(f"  {emoji} :{emoji.name}: → <:{emoji.name}:{emoji.id}>")
        print()
    
    print("="*60)
    print("\nTo use these in the bot, copy the format:")
    print("  <:emoji_name:emoji_id>")
    print("\nFor example:")
    print("  embed.add_field(name='<:meat:123456789> Meat', value='100M')")
    print("="*60)
    
    await bot.close()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN not found in .env file")
    else:
        bot.run(token)
