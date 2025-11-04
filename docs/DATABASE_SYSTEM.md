# 📊 Database-Backed Server Tracking System

## Overview
The bot now uses SQLite database to track servers with **automatic age calculation** based on reference points.

## Key Concept: Reference Point Tracking
Instead of recalculating every time, the system stores:
- **Reference date**: When you checked the VIP streak
- **Reference value**: What the VIP login streak was on that date
- **Current calculation**: Current age = Reference value + (Today - Reference date)

## Database Schema

```sql
CREATE TABLE servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id TEXT NOT NULL,               -- Discord server ID
    state_id INTEGER NOT NULL,            -- WOS state number (e.g., 1780)
    state_name TEXT,                      -- Optional friendly name
    reference_date TEXT NOT NULL,         -- YYYY-MM-DD when checked
    reference_value INTEGER NOT NULL,     -- Login streak on that date
    reference_type TEXT NOT NULL,         -- 'login_streak', 'castle_fight', etc.
    added_by TEXT NOT NULL,               -- User who added it
    added_at TEXT NOT NULL,               -- Timestamp
    UNIQUE(guild_id, state_id)           -- One entry per state per Discord server
)
```

## Commands

### `/addserver <state_id> <login_streak> [name] [date]`
Add a state to track automatically.

**Examples:**
```
/addserver 1780 407
/addserver 1780 407 MyMainState
/addserver 1780 407 MyMainState 2024-11-01
```

**What it saves:**
- State ID: 1780
- Today's date: 2024-11-01
- Login streak today: 407 days
- Server started: 2024-11-01 - 407 days = ~2024-08-21

### `/server <state_id>`
View current age of a tracked state.

**Examples:**
```
/server 1780
```

**What it does:**
1. Looks up State 1780 in database
2. Finds: Reference date = 2024-11-01, Reference value = 407
3. Calculates: Days since reference = Today - 2024-11-01 = 0 days (if checked same day)
4. Current age = 407 + 0 = 407 days
5. Shows full timeline with upcoming events

**Tomorrow (2024-11-02):**
- Days since reference = 1
- Current age = 407 + 1 = 408 days (automatically!)

### `/listservers`
List all tracked states with current ages.

**Example output:**
```
📋 Your Tracked Servers
Total: 3 server(s)

🏔️ MyMain (State 1780)
407 days (58 weeks)
Reference: login_streak
Updated: 2024-11-01

🏔️ State 2456
285 days (40 weeks)
Reference: login_streak
Updated: 2024-10-15
```

### `/updateserver <state_id> <new_streak> [date]`
Recalibrate tracking when you check VIP streak again.

**Use case:** If you forgot to track for a week, check streak again and update.

**Examples:**
```
/updateserver 1780 414          (Checked today, streak is now 414)
/updateserver 1780 414 2024-11-08   (Checked on specific date)
```

### `/deleteserver <state_id>`
Stop tracking a state.

**Examples:**
```
/deleteserver 1780
```

## Benefits

✅ **Auto-updating**: Set once, check anytime  
✅ **Multi-server**: Track unlimited states  
✅ **Accurate**: Based on your actual login streak  
✅ **Flexible**: Update reference point anytime  
✅ **State ID based**: Standard WOS identifier  
✅ **Optional names**: Add friendly names if you want

## Example Workflow

### Day 1 (2024-11-01):
```
1. Check VIP streak in game: 407 days
2. /addserver 1780 407 MyMainState
   ✅ State 1780 tracked!
```

### Day 7 (2024-11-08):
```
/server 1780
📅 Current Server Age: 414 days (407 + 7)
```

### Day 30 (2024-12-01):
```
/server 1780
📅 Current Server Age: 437 days (407 + 30)
```

### Recalibration (if needed):
```
1. Check VIP streak again: 437 days
2. /updateserver 1780 437
   ✅ Updated! Now tracking from new reference point
```

## File Structure

```
data/
  servers.db         # SQLite database
  servers.json       # Legacy (old system)
database.py          # Database functions
bot.py              # Bot commands
```

## Migration from Old System

Old system (JSON file):
- Manual recalculation every time
- Saved server name + start date
- No automatic updates

New system (SQLite):
- Automatic age calculation
- Saved reference point
- Auto-updates daily
- State ID based (standard)

Both systems coexist - old `/age` command still works for one-time calculations.
