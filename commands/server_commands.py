"""
Server tracking commands
Handles database-backed server tracking with automatic age updates
"""
from discord import Embed, Interaction, Color, app_commands
from discord.ext import commands
from datetime import datetime

from core.database import (
    add_server,
    get_server,
    list_servers,
    delete_server,
    update_server_reference
)
from core.game_data import get_timeline_events


async def setup_server_commands(bot: commands.Bot):
    """Register server tracking slash commands"""
    
    @bot.tree.command(name="addserver", description="➕ Add a server for automatic tracking")
    async def addserver_command(interaction: Interaction, 
                                state_id: int,
                                login_streak: int,
                                state_name: str = None,
                                reference_date: str = None):
        """
        Add a server to track automatically
        
        Args:
            state_id: State/server number (e.g., 1780)
            login_streak: Current VIP login streak
            state_name: Optional friendly name
            reference_date: Date of check (YYYY-MM-DD), defaults to today
        """
        try:
            # Validate inputs
            if state_id <= 0 or state_id > 10000:
                await interaction.response.send_message('❌ State ID must be between 1-10000!', ephemeral=True)
                return
            
            if login_streak <= 0 or login_streak > 3650:
                await interaction.response.send_message('❌ Login streak must be between 1-3650!', ephemeral=True)
                return
            
            # Use today if no date provided
            if reference_date is None:
                ref_date = datetime.now().strftime('%Y-%m-%d')
            else:
                try:
                    datetime.strptime(reference_date, '%Y-%m-%d')
                    ref_date = reference_date
                except ValueError:
                    await interaction.response.send_message('❌ Date must be in YYYY-MM-DD format!', ephemeral=True)
                    return
            
            # Add to database
            guild_id = str(interaction.guild.id)
            user_id = str(interaction.user.id)
            
            success = add_server(
                guild_id=guild_id,
                state_id=state_id,
                reference_date=ref_date,
                reference_value=login_streak,
                reference_type='login_streak',
                added_by=user_id,
                state_name=state_name
            )
            
            if success:
                display_name = f"State {state_id}" if not state_name else f"{state_name} (State {state_id})"
                embed = Embed(
                    title='✅ Server Added Successfully',
                    description=f'**{display_name}** is now being tracked!',
                    color=Color.green()
                )
                embed.add_field(name='State ID', value=f'`{state_id}`', inline=True)
                embed.add_field(name='Reference Date', value=ref_date, inline=True)
                embed.add_field(name='Login Streak', value=f'{login_streak} days', inline=True)
                embed.add_field(name='📊 View Anytime', value=f'Use `/server {state_id}` to see current age', inline=False)
                embed.set_footer(text='The bot will automatically calculate current age from this reference point')
                
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message('❌ Error adding server to database!', ephemeral=True)
                
        except Exception as e:
            print(f'Error in /addserver: {e}')
            await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
    
    @bot.tree.command(name="server", description="📊 View current age of a tracked server")
    async def server_command(interaction: Interaction, state_id: int):
        """View current timeline for a saved server"""
        try:
            guild_id = str(interaction.guild.id)
            server_data = get_server(guild_id, state_id)
            
            if not server_data:
                servers = list_servers(guild_id)
                if servers:
                    server_list = ', '.join([str(s['state_id']) for s in servers])
                    await interaction.response.send_message(
                        f'❌ State **{state_id}** not found!\n\n'
                        f'📋 Your tracked states: {server_list}\n\n'
                        f'Use `/addserver` to add a new state.',
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f'❌ No servers tracked! Use `/addserver <state_id> <login_streak>` to add one.',
                        ephemeral=True
                    )
                return
            
            # Calculate timeline
            current_age = server_data['current_age_days']
            server_start = server_data['server_start_date']
            timeline = get_timeline_events(current_age, show_upcoming=True, upcoming_days=200)
            
            months = current_age // 30
            weeks = current_age // 7
            
            display_name = f"State {state_id}" if not server_data['state_name'] else f"{server_data['state_name']} (State {state_id})"
            
            embed = Embed(
                title=f'🏔️ {display_name}',
                description=f'Auto-tracked from reference point',
                color=Color.blue()
            )
            
            embed.add_field(
                name='📅 Current Server Age',
                value=f'**{current_age}** days\n({weeks} weeks / ~{months} months)',
                inline=False
            )
            
            embed.add_field(
                name='🗓️ Server Started',
                value=server_start.strftime("%B %d, %Y"),
                inline=False
            )
            
            embed.add_field(
                name='📌 Reference Point',
                value=f'Set on {server_data["reference_date"]}\n'
                      f'Login streak: {server_data["reference_value"]} days\n'
                      f'Days tracked: {server_data["days_since_reference"]}',
                inline=False
            )
            
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
            
            embed.set_footer(text=f'💡 Use /updateserver {state_id} <new_streak> to recalibrate if needed')
            embed.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(f'Error in /server: {e}')
            import traceback
            traceback.print_exc()
            await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
    
    @bot.tree.command(name="listservers", description="📋 List all tracked servers")
    async def listservers_command(interaction: Interaction):
        """List all servers being tracked"""
        try:
            guild_id = str(interaction.guild.id)
            servers = list_servers(guild_id)
            
            if not servers:
                await interaction.response.send_message(
                    '📋 No servers tracked yet!\n\n'
                    'Use `/addserver <state_id> <login_streak>` to start tracking.',
                    ephemeral=True
                )
                return
            
            embed = Embed(
                title='📋 Your Tracked Servers',
                description=f'Total: {len(servers)} server(s)',
                color=Color.blue()
            )
            
            for server in servers:
                weeks = server['current_age_days'] // 7
                embed.add_field(
                    name=f'🏔️ {server["display_name"]}',
                    value=f'**{server["current_age_days"]}** days ({weeks} weeks)\n'
                          f'Reference: {server["reference_type"]}\n'
                          f'Updated: {server["last_updated"]}',
                    inline=True
                )
            
            embed.set_footer(text='Use /server <state_id> to view full timeline')
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(f'Error in /listservers: {e}')
            await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
    
    @bot.tree.command(name="updateserver", description="🔄 Update server reference")
    async def updateserver_command(interaction: Interaction, 
                                   state_id: int,
                                   new_login_streak: int,
                                   new_reference_date: str = None):
        """Update a server's reference point"""
        try:
            if new_login_streak <= 0 or new_login_streak > 3650:
                await interaction.response.send_message('❌ Login streak must be between 1-3650!', ephemeral=True)
                return
            
            if new_reference_date is None:
                ref_date = datetime.now().strftime('%Y-%m-%d')
            else:
                try:
                    datetime.strptime(new_reference_date, '%Y-%m-%d')
                    ref_date = new_reference_date
                except ValueError:
                    await interaction.response.send_message('❌ Date must be in YYYY-MM-DD format!', ephemeral=True)
                    return
            
            guild_id = str(interaction.guild.id)
            success = update_server_reference(guild_id, state_id, ref_date, new_login_streak)
            
            if success:
                await interaction.response.send_message(
                    f'✅ Updated **State {state_id}**!\n\n'
                    f'New reference: {new_login_streak} days on {ref_date}\n'
                    f'Use `/server {state_id}` to view updated timeline.',
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(f'❌ State **{state_id}** not found!', ephemeral=True)
                
        except Exception as e:
            print(f'Error in /updateserver: {e}')
            await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
    
    @bot.tree.command(name="deleteserver", description="🗑️ Remove a server from tracking")
    async def deleteserver_command(interaction: Interaction, state_id: int):
        """Delete a tracked server"""
        try:
            guild_id = str(interaction.guild.id)
            success = delete_server(guild_id, state_id)
            
            if success:
                await interaction.response.send_message(f'✅ Deleted **State {state_id}** from tracking.', ephemeral=True)
            else:
                await interaction.response.send_message(f'❌ State **{state_id}** not found!', ephemeral=True)
                
        except Exception as e:
            print(f'Error in /deleteserver: {e}')
            await interaction.response.send_message(f'❌ Error: {str(e)}', ephemeral=True)
