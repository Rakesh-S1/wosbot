"""
Core functionality package
Contains game data and database logic
"""
from core.game_data import (
    calculate_from_login_streak,
    get_timeline_events,
    estimate_server_start_from_number,
    GAME_LAUNCH_DATE,
    DETAILED_TIMELINE
)
from core.database import (
    init_database,
    add_server,
    get_server,
    list_servers,
    delete_server,
    update_server_reference
)


__all__ = [
    # Game data functions
    'calculate_from_login_streak',
    'get_timeline_events',
    'estimate_server_start_from_number',
    'GAME_LAUNCH_DATE',
    'DETAILED_TIMELINE',
    
    # Database functions
    'init_database',
    'add_server',
    'get_server',
    'list_servers',
    'delete_server',
    'update_server_reference'
]
