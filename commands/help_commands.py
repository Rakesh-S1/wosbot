"""
Help command
Displays available commands and usage information
"""
from discord import Embed, Interaction, Color
from discord.ext import commands


async def setup_help_commands(bot: commands.Bot):
    """Register help slash command"""
    
    @bot.tree.command(name="help", description="❓ Show all available commands")
    async def help_command(interaction: Interaction):
        """Display help information"""
        try:
            embed = Embed(
                title='🏔️ WOS Bot - Command Guide',
                description='Track Whiteout Survival server ages and events',
                color=Color.blue()
            )
            
            embed.add_field(
                name='📊 Server Info Commands',
                value=(
                    '`/age <state_id> <login_streak>` - Calculate server age from VIP login streak\n'
                    '`/state <state_number>` - Estimate server age from state number'
                ),
                inline=False
            )
            
            embed.add_field(
                name='💰 Resource Calculator Commands',
                value=(
                    '`/buildingcost <building> <from> <to>` - Calculate building upgrade costs\n'
                    '`/waracademycost <from_fc> <to_fc>` - Calculate War Academy FC upgrade costs\n'
                    '`/researchcost <research> <from> <to>` - Calculate research upgrade costs\n'
                    '`/waracademyresearch` - T11 research costs (coming soon)'
                ),
                inline=False
            )
            
            embed.add_field(
                name='💾 Server Tracking Commands',
                value=(
                    '`/addserver <state_id> <login_streak>` - Add a server for automatic tracking\n'
                    '`/server <state_id>` - View current age of tracked server\n'
                    '`/listservers` - List all tracked servers\n'
                    '`/updateserver <state_id> <new_streak>` - Update server reference point\n'
                    '`/deleteserver <state_id>` - Remove server from tracking'
                ),
                inline=False
            )
            
            embed.add_field(
                name='📋 How to Use Tracking',
                value=(
                    '**1.** Find your VIP login streak in-game (VIP page)\n'
                    '**2.** Add server: `/addserver 1780 407`\n'
                    '**3.** View anytime: `/server 1780`\n'
                    '**4.** Bot auto-calculates current age daily!'
                ),
                inline=False
            )
            
            embed.add_field(
                name='💡 Tips',
                value=(
                    '• Login streak = exact server age in days\n'
                    '• Tracking saves reference point, auto-updates\n'
                    '• State number gives rough estimate only\n'
                    '• Optional: Add state names for easier reference'
                ),
                inline=False
            )
            
            embed.set_footer(text='Made for tracking WOS server events | Questions? Ask in support')
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(f'Error in /help: {e}')
            await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
