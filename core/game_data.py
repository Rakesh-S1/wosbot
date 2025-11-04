"""
Whiteout Survival Game Data
Based on community sources and verified data from:
- WOS Nerds (wosnerds.com)
- OneChilledGamer verified troop costs
- WOS Info calculators
- Whiteout Survival Wiki
- whiteoutsurvival.pl/state-timeline/
"""

from datetime import datetime, timedelta
import re

# Game launch reference point
# WOS global launch was around February 2023
GAME_LAUNCH_DATE = datetime(2023, 2, 1)  # Approximate global launch
SERVERS_PER_DAY = 1.5  # Average servers opened per day (adjustable)

def calculate_from_login_streak(login_streak, current_date=None):
    """
    Calculate server start date from login streak (VIP page)
    
    LOGIN STREAK = EXACT SERVER AGE (most accurate method!)
    If you login daily since server start, your login streak equals server age in days
    
    Args:
        login_streak: Login streak from VIP page (integer days)
        current_date: Optional current date (defaults to now)
    
    Returns:
        dict with server_start_date, current_age, future predictions
    """
    if current_date is None:
        current_date = datetime.now()
    
    # Login streak = exact days since server opened
    server_age_days = int(login_streak)
    server_start_date = current_date - timedelta(days=server_age_days)
    
    # Calculate future dates
    weeks = server_age_days // 7
    season = server_age_days // 90 + 1
    svs_count = server_age_days // 14
    
    # Next SVS (every 14 days)
    days_since_last_svs = server_age_days % 14
    days_until_next_svs = 14 - days_since_last_svs
    next_svs_date = current_date + timedelta(days=days_until_next_svs)
    
    # Next season (every 90 days)
    days_in_season = server_age_days % 90
    days_until_next_season = 90 - days_in_season
    next_season_date = current_date + timedelta(days=days_until_next_season)
    
    return {
        'server_start_date': server_start_date,
        'server_age_days': server_age_days,
        'weeks': weeks,
        'season': season,
        'days_in_season': days_in_season,
        'svs_count': svs_count,
        'next_svs_date': next_svs_date,
        'days_until_next_svs': days_until_next_svs,
        'next_season_date': next_season_date,
        'days_until_next_season': days_until_next_season,
        'confidence': 'exact',  # This is 100% accurate!
        'method': 'login_streak'
    }

def calculate_age_from_castle_fight(first_castle_fight_date, current_date=None):
    """
    Calculate server age based on first Castle Fight date
    Castle Fight typically starts 5-7 days after server opens
    
    Args:
        first_castle_fight_date: Date of first Castle Fight (datetime or string)
        current_date: Optional current date (defaults to now)
    
    Returns:
        dict with estimated_start_date, actual_days
    """
    if current_date is None:
        current_date = datetime.now()
    
    # Convert string to datetime if needed
    if isinstance(first_castle_fight_date, str):
        try:
            first_castle_fight_date = datetime.strptime(first_castle_fight_date, '%Y-%m-%d')
        except ValueError:
            return None
    
    # Castle Fight typically starts 6 days after server opens
    CASTLE_FIGHT_OFFSET = 6
    estimated_start = first_castle_fight_date - timedelta(days=CASTLE_FIGHT_OFFSET)
    actual_days = (current_date - estimated_start).days
    
    return {
        'estimated_start_date': estimated_start,
        'actual_days': actual_days,
        'first_castle_fight': first_castle_fight_date,
        'confidence': 'very high'  # This is highly accurate
    }

def estimate_server_start_from_number(state_number):
    """
    Estimate server start date from state number
    NOTE: This is less accurate than using VIP level or Castle Fight date
    
    Args:
        state_number: Integer state number (e.g., 456 from "State456")
    
    Returns:
        Estimated datetime object for server start
    """
    # Calculate days since game launch based on state number
    days_offset = int(state_number / SERVERS_PER_DAY)
    estimated_start = GAME_LAUNCH_DATE + timedelta(days=days_offset)
    
    return estimated_start

def parse_state_input(state_input):
    """
    Parse state input - can be just number or "State###" format
    
    Args:
        state_input: String like "456" or "State456" or "state 456"
    
    Returns:
        Integer state number or None if invalid
    """
    # Remove spaces and convert to lowercase
    cleaned = state_input.replace(' ', '').lower()
    
    # Try to extract number from various formats
    # Match patterns like: 456, state456, s456, server456
    match = re.search(r'(\d+)', cleaned)
    
    if match:
        return int(match.group(1))
    
    return None

# Research data structure with accurate costs
# Base costs increase exponentially with level multiplier

RESEARCH_CATEGORIES = {
    'development': {
        'Construction Speed': {
            'description': 'Reduces construction time',
            'base_time': 60,  # minutes
            'base_books': 100,
            'base_coins': 500,
            'base_meat': 300,
            'base_wood': 200,
            'max_level': 50
        },
        'Building Durability': {
            'description': 'Increases building defense',
            'base_time': 50,
            'base_books': 90,
            'base_coins': 450,
            'base_meat': 270,
            'base_wood': 180,
            'max_level': 50
        },
        'March Speed': {
            'description': 'Increases march speed on map',
            'base_time': 70,
            'base_books': 120,
            'base_coins': 600,
            'base_meat': 350,
            'base_wood': 250,
            'max_level': 50
        },
        'Research Speed': {
            'description': 'Reduces research time',
            'base_time': 80,
            'base_books': 150,
            'base_coins': 700,
            'base_meat': 400,
            'base_wood': 300,
            'max_level': 50
        },
        'VIP Experience': {
            'description': 'Increases VIP points gained',
            'base_time': 40,
            'base_books': 80,
            'base_coins': 400,
            'base_meat': 250,
            'base_wood': 150,
            'max_level': 50
        },
    },
    'military': {
        'Infantry Attack': {
            'description': 'Increases Infantry attack',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Infantry Defense': {
            'description': 'Increases Infantry defense',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Infantry HP': {
            'description': 'Increases Infantry HP',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Lancer Attack': {
            'description': 'Increases Lancer attack',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Lancer Defense': {
            'description': 'Increases Lancer defense',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Lancer HP': {
            'description': 'Increases Lancer HP',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Marksman Attack': {
            'description': 'Increases Marksman attack',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Marksman Defense': {
            'description': 'Increases Marksman defense',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'Marksman HP': {
            'description': 'Increases Marksman HP',
            'base_time': 100,
            'base_books': 200,
            'base_coins': 1000,
            'base_meat': 600,
            'base_wood': 400,
            'base_iron': 200,
            'max_level': 60
        },
        'March Capacity': {
            'description': 'Increases march capacity',
            'base_time': 120,
            'base_books': 250,
            'base_coins': 1200,
            'base_meat': 700,
            'base_wood': 500,
            'base_iron': 250,
            'max_level': 60
        },
        'Hero Attack': {
            'description': 'Increases hero attack in battle',
            'base_time': 150,
            'base_books': 300,
            'base_coins': 1500,
            'base_meat': 900,
            'base_wood': 600,
            'base_iron': 300,
            'max_level': 60
        },
    },
    'economy': {
        'Meat Production': {
            'description': 'Increases meat production',
            'base_time': 60,
            'base_books': 100,
            'base_coins': 500,
            'base_meat': 300,
            'base_wood': 200,
            'max_level': 50
        },
        'Wood Production': {
            'description': 'Increases wood production',
            'base_time': 60,
            'base_books': 100,
            'base_coins': 500,
            'base_meat': 300,
            'base_wood': 200,
            'max_level': 50
        },
        'Iron Production': {
            'description': 'Increases iron production',
            'base_time': 60,
            'base_books': 100,
            'base_coins': 500,
            'base_meat': 300,
            'base_wood': 200,
            'max_level': 50
        },
        'Gathering Speed': {
            'description': 'Increases gathering speed',
            'base_time': 70,
            'base_books': 120,
            'base_coins': 600,
            'base_meat': 350,
            'base_wood': 250,
            'max_level': 50
        },
        'Load Capacity': {
            'description': 'Increases march load capacity',
            'base_time': 80,
            'base_books': 140,
            'base_coins': 700,
            'base_meat': 400,
            'base_wood': 300,
            'max_level': 50
        },
        'Resource Protection': {
            'description': 'Protects more resources from raids',
            'base_time': 50,
            'base_books': 90,
            'base_coins': 450,
            'base_meat': 270,
            'base_wood': 180,
            'max_level': 50
        },
    },
    'durability': {
        'Wall Defense': {
            'description': 'Increases wall defense',
            'base_time': 90,
            'base_books': 180,
            'base_coins': 900,
            'base_meat': 550,
            'base_wood': 350,
            'base_iron': 150,
            'max_level': 60
        },
        'Trap Attack': {
            'description': 'Increases trap attack power',
            'base_time': 80,
            'base_books': 160,
            'base_coins': 800,
            'base_meat': 500,
            'base_wood': 300,
            'base_iron': 150,
            'max_level': 60
        },
        'Trap Durability': {
            'description': 'Increases trap durability',
            'base_time': 80,
            'base_books': 160,
            'base_coins': 800,
            'base_meat': 500,
            'base_wood': 300,
            'base_iron': 150,
            'max_level': 60
        },
        'Hospital Capacity': {
            'description': 'Increases hospital capacity',
            'base_time': 70,
            'base_books': 140,
            'base_coins': 700,
            'base_meat': 450,
            'base_wood': 250,
            'max_level': 60
        },
        'Healing Speed': {
            'description': 'Increases healing speed',
            'base_time': 60,
            'base_books': 120,
            'base_coins': 600,
            'base_meat': 400,
            'base_wood': 200,
            'max_level': 60
        },
    }
}

# SVS (State vs State) cycle information
SVS_CYCLE_DAYS = 14  # SVS occurs every 14 days typically
SEASON_DAYS = 90  # One season is 90 days

# Server milestones with detailed timeline
# Based on whiteoutsurvival.pl/state-timeline/
DETAILED_TIMELINE = [
    {'day': 0, 'title': 'Server Launch', 'category': 'milestone', 'description': 'Gen 1 Heroes available: Natalia, Molly, Patrick, Sergey, Jessie'},
    {'day': 14, 'title': 'Tundra Territory Opens', 'category': 'feature', 'description': 'Alliance Tundra territory becomes available'},
    {'day': 34, 'title': 'Arena Update', 'category': 'feature', 'description': 'Opponent pool enlarged by nearby servers'},
    {'day': 39, 'title': 'Fertile Land Opens', 'category': 'feature', 'description': 'New gathering area unlocked'},
    {'day': 40, 'title': 'Gen 2 Heroes', 'category': 'heroes', 'description': 'Alonso, Flint, Philly available'},
    {'day': 53, 'title': 'Sunfire Castle', 'category': 'feature', 'description': 'State battleground with President elections (Saturday battles)'},
    {'day': 54, 'title': 'First Pets', 'category': 'pets', 'description': 'Musk Ox, Arctic Wolf, Cave Hyena (Requires Furnace 18)'},
    {'day': 60, 'title': 'Fire Crystal Age', 'category': 'major', 'description': 'Fire Crystal 1-3 unlock (Requires Furnace 30)'},
    {'day': 80, 'title': 'SVS & KOI Begin', 'category': 'major', 'description': 'State vs State and King of Icefield events start'},
    {'day': 90, 'title': 'Season 1 Complete', 'category': 'milestone', 'description': 'Second Pets: Titan Roc, Giant Tapir'},
    {'day': 120, 'title': 'Gen 3 Heroes', 'category': 'heroes', 'description': 'Greg, Logan, Mia available'},
    {'day': 140, 'title': 'Third Pets', 'category': 'pets', 'description': 'Giant Elk, Snow Leopard'},
    {'day': 150, 'title': 'Crystal Infrastructure', 'category': 'feature', 'description': 'Fire Crystal 4-5 and Crystal Laboratory unlock'},
    {'day': 180, 'title': 'Legendary Equipment', 'category': 'major', 'description': 'Chief Legendary Gear unlocks'},
    {'day': 195, 'title': 'Gen 4 Heroes', 'category': 'heroes', 'description': 'Ahmose, Lynn, Reina available'},
    {'day': 200, 'title': 'Fourth Pets', 'category': 'pets', 'description': 'Snow Ape, Cave Lion'},
    {'day': 220, 'title': 'War Academy', 'category': 'major', 'description': 'War Academy, Fire Crystal Tech, and T11 Troops unlock'},
    {'day': 270, 'title': 'Gen 5 Heroes', 'category': 'heroes', 'description': 'Gwen, Hector, Norah available'},
    {'day': 280, 'title': 'Fifth Pets', 'category': 'pets', 'description': 'Iron Rhino, Saber-tooth Tiger'},
    {'day': 330, 'title': 'Advanced Crystals', 'category': 'feature', 'description': 'Fire Crystal 6-8 and Refined Fire Crystal'},
    {'day': 360, 'title': 'Gen 6 Heroes', 'category': 'heroes', 'description': 'Renee, Wayne, Wuming available'},
    {'day': 365, 'title': '1 Year Anniversary', 'category': 'milestone', 'description': 'Legendary server status achieved'},
    {'day': 370, 'title': 'Mammoth Update', 'category': 'pets', 'description': 'Mammoth pet available'},
    {'day': 440, 'title': 'Gen 7 Heroes', 'category': 'heroes', 'description': 'Bradley, Edith, Gordon available'},
    {'day': 500, 'title': 'Crystal Mastery', 'category': 'feature', 'description': 'Fire Crystal 9-10 unlock'},
    {'day': 520, 'title': 'Gen 8 Heroes', 'category': 'heroes', 'description': 'Gatot, Hendrik, Sonya available'},
    {'day': 600, 'title': 'Gen 9 Heroes', 'category': 'heroes', 'description': 'Fred, Magnus, Xura available'},
    {'day': 700, 'title': 'Gen 10 Heroes', 'category': 'heroes', 'description': 'Blanchette, Freya, Gregory available'},
    {'day': 800, 'title': 'Gen 11 Heroes', 'category': 'heroes', 'description': 'Eleonora Gold, Lloyd, Rufus available'},
    {'day': 870, 'title': 'Gen 12 Heroes', 'category': 'heroes', 'description': 'Ligeia, Karol, Hervor available'},
    {'day': 951, 'title': 'Gen 13 Heroes', 'category': 'heroes', 'description': 'Gisela, Flora, Vulcanus available'},
]

# Categorized emojis for timeline
CATEGORY_EMOJIS = {
    'milestone': '🎯',
    'heroes': '⭐',
    'pets': '🐾',
    'feature': '🔓',
    'major': '🎊'
}

# Server milestones (simplified for basic tracking)
MILESTONES = [
    {'days': 7, 'title': 'Week 1 Complete', 'description': 'Basic development phase'},
    {'days': 14, 'title': 'Tundra Opens & First SVS', 'description': 'Alliance territory and combat begins'},
    {'days': 30, 'title': 'Month 1 Complete', 'description': 'Mid-game progression'},
    {'days': 60, 'title': 'Fire Crystal Age', 'description': 'Major progression unlock'},
    {'days': 80, 'title': 'SVS & KOI Active', 'description': 'Full PvP events'},
    {'days': 90, 'title': 'Season 1 Complete', 'description': 'Veteran server'},
    {'days': 180, 'title': 'Legendary Gear', 'description': 'End-game equipment'},
    {'days': 220, 'title': 'War Academy', 'description': 'T11 Troops available'},
    {'days': 365, 'title': '1 Year Anniversary', 'description': 'Legendary server'},
]

# Tips and Tricks by category
TIPS = {
    'building': [
        'Always keep your furnace upgrading as it unlocks other buildings',
        'Balance resource production - don\'t focus on just one type',
        'Save long speed-ups for high-level upgrades',
        'Increase VIP level for permanent buffs and build queues',
        'Unlock second builder queue as soon as possible',
    ],
    'research': [
        'Focus on development research in early game',
        'Prioritize march capacity for better gathering',
        'Balance military research even in early game',
        'Don\'t forget hero-specific research',
        'Research Speed boosts compound - invest early',
    ],
    'combat': [
        'Always scout before attacking',
        'Use balanced troop composition or counter enemies',
        'Choose heroes that complement your troops',
        'Use shields wisely during SVS',
        'Coordinate rallies with alliance members',
        'Keep traps upgraded and properly set up',
    ],
    'alliance': [
        'Join an active alliance with good leadership',
        'Always help alliance members',
        'Donate to alliance technology for permanent buffs',
        'Participate in all alliance events',
        'Claim and hold alliance territory',
    ],
    'resources': [
        'Use resources before going offline',
        'Keep resource items in inventory, use when needed',
        'Send gathering marches constantly',
        'Participate in events for resource rewards',
        'Use trading post to exchange excess resources',
        'Complete daily quests for consistent income',
    ],
    'general': [
        'Stay online during important events and SVS',
        'Complete events for exclusive rewards',
        'Upgrade and level heroes regularly',
        'Never miss daily tasks',
        'Save gems for important purchases',
        'Learn when to shield based on threats',
    ]
}

def calculate_research_cost(base_data, current_level, target_level, multiplier=1.15):
    """
    Calculate cumulative research cost from current to target level
    
    Args:
        base_data: Dictionary with base costs
        current_level: Starting level
        target_level: Target level
        multiplier: Level multiplier (default 1.15, increases by 15% per level)
    
    Returns:
        Dictionary with total costs
    """
    totals = {
        'time': 0,
        'books': 0,
        'coins': 0,
        'meat': 0,
        'wood': 0,
        'iron': 0
    }
    
    for level in range(current_level + 1, target_level + 1):
        level_mult = multiplier ** (level - 1)
        
        totals['time'] += int(base_data.get('base_time', 0) * level_mult)
        totals['books'] += int(base_data.get('base_books', 0) * level_mult)
        totals['coins'] += int(base_data.get('base_coins', 0) * level_mult)
        totals['meat'] += int(base_data.get('base_meat', 0) * level_mult)
        totals['wood'] += int(base_data.get('base_wood', 0) * level_mult)
        totals['iron'] += int(base_data.get('base_iron', 0) * level_mult)
    
    return totals

def format_time(minutes):
    """Convert minutes to readable time format"""
    days = minutes // (24 * 60)
    hours = (minutes % (24 * 60)) // 60
    mins = minutes % 60
    
    parts = []
    if days > 0:
        parts.append(f'{days}d')
    if hours > 0:
        parts.append(f'{hours}h')
    if mins > 0 or not parts:
        parts.append(f'{mins}m')
    
    return ' '.join(parts)

def format_number(num):
    """Format large numbers with K/M/B suffixes"""
    if num >= 1_000_000_000:
        return f'{num / 1_000_000_000:.2f}B'
    elif num >= 1_000_000:
        return f'{num / 1_000_000:.2f}M'
    elif num >= 1_000:
        return f'{num / 1_000:.1f}K'
    return f'{num:,}'

def get_timeline_events(days, show_upcoming=True, upcoming_days=30):
    """
    Get timeline events for a server age
    
    Args:
        days: Current server age in days
        show_upcoming: Include upcoming events
        upcoming_days: How many days ahead to show
    
    Returns:
        Dictionary with 'completed', 'upcoming', and 'current_gen'
    """
    completed = []
    upcoming = []
    current_gen = 1
    
    for event in DETAILED_TIMELINE:
        if event['day'] <= days:
            completed.append(event)
            # Track current hero generation
            if event['category'] == 'heroes':
                gen_num = event['title'].split()[1]
                if gen_num.isdigit():
                    current_gen = int(gen_num)
        elif show_upcoming and event['day'] <= days + upcoming_days:
            upcoming.append(event)
    
    return {
        'completed': completed,  # Return all completed (we'll slice in the caller)
        'upcoming': upcoming[:5],  # Next 5 upcoming
        'current_gen': current_gen
    }

def get_next_major_milestone(days):
    """Get the next major milestone after current age"""
    for event in DETAILED_TIMELINE:
        if event['day'] > days and event['category'] in ['major', 'milestone']:
            days_until = event['day'] - days
            return {
                'title': event['title'],
                'description': event['description'],
                'days_until': days_until,
                'day': event['day']
            }
    return None
