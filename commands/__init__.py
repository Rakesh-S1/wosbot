"""
Command modules package
Import all command setup functions here for easy registration
"""
from commands.age_commands import setup_age_commands
from commands.server_commands import setup_server_commands
from commands.help_commands import setup_help_commands
from commands.resource_commands import setup_resource_commands


async def setup_all_commands(bot):
    """
    Register all command modules with the bot
    
    Args:
        bot: Discord bot instance
    """
    await setup_age_commands(bot)
    await setup_server_commands(bot)
    await setup_help_commands(bot)
    await setup_resource_commands(bot)
    print('✅ All commands registered successfully')


__all__ = [
    'setup_all_commands',
    'setup_age_commands',
    'setup_server_commands',
    'setup_help_commands',
    'setup_resource_commands'
]
