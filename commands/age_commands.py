"""
Age calculation commands
Handles /age and /state commands for server timeline calculations
"""
from discord import Embed, Interaction, Color, app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import sqlite3

from core.game_data import (
    calculate_from_login_streak,
    get_timeline_events,
    estimate_server_start_from_number,
    parse_state_input
)


async def setup_age_commands(bot: commands.Bot):
    """Register age-related slash commands"""
    
    @bot.tree.command(name="age", description="📊 Get server age from tracked database")
    @app_commands.describe(
        state_number="State/server number (e.g., 456 or State456)"
    )
    async def age_command(interaction: Interaction, state_number: str):
        """Get server age from database or suggest adding it"""
        try:
            parsed_number = parse_state_input(state_number)
            if parsed_number is None:
                await interaction.response.send_message('❌ Invalid state format! Use: `456` or `State456`', ephemeral=True)
                return
            
            # Check if server exists in database
            conn = sqlite3.connect('data/servers.db')
            cur = conn.cursor()
            cur.execute('''
                SELECT state_name, state_id, reference_date, reference_value, reference_type
                FROM servers 
                WHERE state_id = ?
                LIMIT 1
            ''', (parsed_number,))
            server = cur.fetchone()
            conn.close()
            
            if not server:
                # Server not in database - suggest adding it
                await interaction.response.send_message(
                    f'❌ **State {parsed_number} is not being tracked yet!**\n\n'
                    f'📝 To track this server, use:\n'
                    f'`/addserver server_name:State{parsed_number} state_number:{parsed_number} reference_day:1 login_streak:1`\n\n'
                    f'💡 Replace `reference_day` and `login_streak` with current values from your game.',
                    ephemeral=True
                )
                return
            
            # Server found - calculate current age
            state_name, state_id, ref_date, ref_value, ref_type = server
            reference_date = datetime.fromisoformat(ref_date)
            today = datetime.now()
            days_since_reference = (today - reference_date).days
            current_age = ref_value + days_since_reference
            weeks = current_age // 7
            months = current_age // 30
            
            # Get timeline events
            timeline = get_timeline_events(current_age, show_upcoming=True, upcoming_days=200)
            
            # Calculate server start date
            server_start = reference_date - timedelta(days=ref_value - 1)
            
            # Create embed
            display_name = state_name or f"State {state_id}"
            embed = Embed(
                title=f'🏔️ {display_name} - Server Timeline',
                description=f'📅 Started: **{server_start.strftime("%B %d, %Y")}**',
                color=Color.blue()
            )
            
            # Server Age
            embed.add_field(
                name='📅 Current Age',
                value=f'**{current_age}** days\n({weeks} weeks / ~{months} months)',
                inline=False
            )
            
            # Recent Milestones
            if timeline['completed']:
                recent_text = '\n'.join([
                    f'✅ Day {e["day"]}: {e["title"]}'
                    for e in timeline['completed'][-5:]
                ])
                embed.add_field(
                    name='📜 Recent Milestones (Completed)',
                    value=recent_text,
                    inline=False
                )
            
            # Upcoming Events
            if timeline['upcoming']:
                upcoming_text = '\n'.join([
                    f'🔜 Day {e["day"]} ({e["day"] - current_age} days): {e["title"]}'
                    for e in timeline['upcoming'][:5]
                ])
                embed.add_field(
                    name='🎯 Upcoming Events',
                    value=upcoming_text,
                    inline=False
                )
            
            embed.set_footer(text=f'� Data from tracked server database | Last updated: {reference_date.strftime("%Y-%m-%d")}')
            embed.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(f'❌ Error in /age command: {e}')
            import traceback
            traceback.print_exc()
            try:
                await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
            except:
                await interaction.followup.send(f'❌ Error: {str(e)}', ephemeral=True)
    
    @bot.tree.command(name="streak", description="📊 Calculate exact server age from VIP login streak")
    @app_commands.describe(
        login_streak="Your current VIP login streak number",
        server_name="Optional server name for reference"
    )
    async def streak_command(interaction: Interaction, login_streak: int, server_name: str = None):
        """Calculate exact server age from VIP login streak"""
        try:
            # Validate input
            if login_streak <= 0:
                await interaction.response.send_message('❌ Login streak must be a positive number!', ephemeral=True)
                return
            
            if login_streak > 3650:  # 10 years max
                await interaction.response.send_message('❌ Login streak seems too high! Please check the number.', ephemeral=True)
                return
            
            # Calculate from login streak
            result = calculate_from_login_streak(login_streak)
            timeline = get_timeline_events(result['server_age_days'], show_upcoming=True, upcoming_days=200)
            
            # Calculate months
            months = result['server_age_days'] // 30
            
            # Create embed with clean format
            embed = Embed(
                title='🏔️ Whiteout Survival Server Age Tracker',
                description='Server information based on VIP login streak',
                color=Color.blue()
            )
            
            # Server Age section
            embed.add_field(
                name='📅 Server Age',
                value=f'**{result["server_age_days"]}** days\n({result["weeks"]} weeks / ~{months} months)',
                inline=False
            )
            
            # Creation Date section
            embed.add_field(
                name='🗓️ Creation Date',
                value=result["server_start_date"].strftime("%B %d, %Y"),
                inline=False
            )
            
            # Recent Milestones (last 5 completed events)
            if timeline['completed']:
                recent_text = '\n'.join([
                    f'✅ Day {e["day"]}: {e["title"]}'
                    for e in timeline['completed'][-5:]
                ])
                embed.add_field(
                    name='📜 Recent Milestones (Completed)',
                    value=recent_text,
                    inline=False
                )
            
            # Upcoming Events (next 5 events)
            if timeline['upcoming']:
                upcoming_text = '\n'.join([
                    f'🔜 Day {e["day"]} ({e["day"] - result["server_age_days"]} days): {e["title"]}'
                    for e in timeline['upcoming'][:5]
                ])
                embed.add_field(
                    name='🎯 Upcoming Events',
                    value=upcoming_text,
                    inline=False
                )
            
            embed.set_footer(text='💡 Tip: Make sure you joined on Day 1 and logged in every day for accurate results')
            embed.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(f'❌ Error in /streak command: {e}')
            import traceback
            traceback.print_exc()
            try:
                await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
            except:
                await interaction.followup.send(f'❌ Error: {str(e)}', ephemeral=True)
