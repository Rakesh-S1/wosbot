"""
Database module for server tracking
Stores server reference points for accurate age tracking
"""
import sqlite3
import os
from datetime import datetime, timedelta

DB_FILE = 'data/servers.db'

def init_database():
    """Initialize the database with required tables"""
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Servers table - stores server reference points
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id TEXT NOT NULL,
            state_id INTEGER NOT NULL,
            state_name TEXT,
            reference_date TEXT NOT NULL,
            reference_value INTEGER NOT NULL,
            reference_type TEXT NOT NULL,
            added_by TEXT NOT NULL,
            added_at TEXT NOT NULL,
            UNIQUE(guild_id, state_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_server(guild_id: str, state_id: int, reference_date: str, 
               reference_value: int, reference_type: str, added_by: str, state_name: str = None):
    """
    Add or update a server in the database
    
    Args:
        guild_id: Discord guild ID
        state_id: State/server number (e.g., 1780)
        reference_date: Date when reference was taken (YYYY-MM-DD)
        reference_value: Value on reference date (e.g., login streak day 407)
        reference_type: Type of reference (login_streak, castle_fight, custom)
        added_by: User ID who added it
        state_name: Optional friendly name for the state
    
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        added_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT OR REPLACE INTO servers 
            (guild_id, state_id, state_name, reference_date, reference_value, reference_type, added_by, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (guild_id, state_id, state_name, reference_date, reference_value, reference_type, added_by, added_at))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding server: {e}")
        return False

def get_server(guild_id: str, state_id: int):
    """
    Get server information and calculate current age
    
    Args:
        guild_id: Discord guild ID
        state_id: State/server number
    
    Returns:
        Dictionary with server info and calculated current age, or None if not found
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT state_id, state_name, reference_date, reference_value, reference_type, added_by, added_at
            FROM servers
            WHERE guild_id = ? AND state_id = ?
        ''', (guild_id, state_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        state_id_db, state_name, reference_date_str, reference_value, reference_type, added_by, added_at = result
        
        # Calculate current values
        reference_date = datetime.strptime(reference_date_str, '%Y-%m-%d')
        today = datetime.now()
        days_since_reference = (today - reference_date).days
        
        # Current age calculation
        current_age_days = reference_value + days_since_reference
        
        # Calculate server start date
        server_start_date = reference_date - timedelta(days=reference_value)
        
        return {
            'state_id': state_id_db,
            'state_name': state_name,
            'reference_date': reference_date_str,
            'reference_value': reference_value,
            'reference_type': reference_type,
            'days_since_reference': days_since_reference,
            'current_age_days': current_age_days,
            'server_start_date': server_start_date,
            'added_by': added_by,
            'added_at': added_at
        }
    except Exception as e:
        print(f"Error getting server: {e}")
        return None

def list_servers(guild_id: str):
    """
    List all servers for a guild with current ages
    
    Returns:
        List of dictionaries with server info
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT state_id, state_name, reference_date, reference_value, reference_type
            FROM servers
            WHERE guild_id = ?
            ORDER BY state_id
        ''', (guild_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        servers = []
        today = datetime.now()
        
        for state_id, state_name, ref_date_str, ref_value, ref_type in results:
            ref_date = datetime.strptime(ref_date_str, '%Y-%m-%d')
            days_since = (today - ref_date).days
            current_age = ref_value + days_since
            
            display_name = f"State {state_id}" if not state_name else f"{state_name} ({state_id})"
            
            servers.append({
                'state_id': state_id,
                'state_name': state_name,
                'display_name': display_name,
                'current_age_days': current_age,
                'reference_type': ref_type,
                'last_updated': ref_date_str
            })
        
        return servers
    except Exception as e:
        print(f"Error listing servers: {e}")
        return []

def delete_server(guild_id: str, state_id: int):
    """Delete a server from the database by state ID"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM servers
            WHERE guild_id = ? AND state_id = ?
        ''', (guild_id, state_id))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    except Exception as e:
        print(f"Error deleting server: {e}")
        return False

def update_server_reference(guild_id: str, state_id: int, new_reference_date: str, 
                            new_reference_value: int):
    """
    Update the reference point for a server (when user checks VIP streak again)
    
    This recalibrates the tracking if streak was updated
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE servers
            SET reference_date = ?, reference_value = ?, added_at = ?
            WHERE guild_id = ? AND state_id = ?
        ''', (new_reference_date, new_reference_value, datetime.now().isoformat(), 
              guild_id, state_id))
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    except Exception as e:
        print(f"Error updating server: {e}")
        return False
