import sqlite3
from typing import Optional

import discord
from discord import app_commands

DB_PATH = "data/buildings.db"

# Custom emoji IDs from Discord server
EMOJIS = {
    'meat': '<:meat:1434975469832376412>',
    'wood': '<:wood:1434975478581825556>',
    'coal': '<:coal:1434975460705440014>',
    'iron': '<:iron:1434975466892169306>',
    'steel': '<:steel:1434975476228821012>',
    'firecrystal': '<:firecrystal:1434975464455143484>',
    'refinedfc': '<:refinedfc:1434975472919249006>',
}


def format_num(n: Optional[int]) -> str:
    if n is None:
        return "-"
    for unit in ['','K','M','B']:
        if abs(n) < 1000:
            return f"{n}{unit}"
        n = n // 1000
    return str(n)


async def setup_resource_commands(bot: discord.Client):
    """Register building cost calculator command."""
    
    # Autocomplete for building names
    async def building_autocomplete(interaction: discord.Interaction, current: str):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT slug, name FROM buildings ORDER BY name")
            buildings = cur.fetchall()
            conn.close()
            
            # Filter based on user input (if empty, show all)
            if not current:
                matches = [
                    app_commands.Choice(name=name, value=slug)
                    for slug, name in buildings
                ]
            else:
                current_lower = current.lower()
                matches = [
                    app_commands.Choice(name=name, value=slug)
                    for slug, name in buildings
                    if current_lower in slug.lower() or current_lower in name.lower()
                ]
            
            result = matches[:25]  # Discord limit
            print(f"Building autocomplete: current='{current}', returning {len(result)} choices")
            return result
        except Exception as e:
            print(f"❌ Error in building_autocomplete: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    # Autocomplete for from_level
    async def from_level_autocomplete(interaction: discord.Interaction, current: str):
        try:
            # Get the building from the interaction namespace
            building = interaction.namespace.building
            print(f"From_level autocomplete: building='{building}', current='{current}'")
            
            if not building:
                print("  -> No building selected yet")
                return []
            
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT level_int FROM levels 
                WHERE building_id = (SELECT id FROM buildings WHERE slug = ?)
                ORDER BY level_int
            """, (building,))
            levels = [row[0] for row in cur.fetchall()]
            conn.close()
            
            # Filter based on user input
            if current:
                levels = [lvl for lvl in levels if str(lvl).startswith(current)]
            
            result = [app_commands.Choice(name=str(lvl), value=lvl) for lvl in levels[:25]]
            print(f"  -> Returning {len(result)} level choices")
            return result
        except Exception as e:
            print(f"❌ Error in from_level_autocomplete: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    # Autocomplete for to_level
    async def to_level_autocomplete(interaction: discord.Interaction, current: str):
        try:
            # Get the building and from_level from the interaction namespace
            building = interaction.namespace.building
            from_level = interaction.namespace.from_level
            print(f"To_level autocomplete: building='{building}', from_level={from_level}, current='{current}'")
            
            if not building:
                print("  -> No building selected yet")
                return []
            
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT level_int FROM levels 
                WHERE building_id = (SELECT id FROM buildings WHERE slug = ?)
                ORDER BY level_int
            """, (building,))
            levels = [row[0] for row in cur.fetchall()]
            conn.close()
            
            # Filter to show only levels >= from_level if from_level is set
            if from_level:
                levels = [lvl for lvl in levels if lvl >= from_level]
            
            # Filter based on user input
            if current:
                levels = [lvl for lvl in levels if str(lvl).startswith(current)]
            
            result = [app_commands.Choice(name=str(lvl), value=lvl) for lvl in levels[:25]]
            print(f"  -> Returning {len(result)} level choices")
            return result
        except Exception as e:
            print(f"❌ Error in to_level_autocomplete: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    @bot.tree.command(name="buildingcost", description="Calculate building upgrade costs (including War Academy)")
    @app_commands.describe(
        building="Building slug (e.g., furnace, infantry-camp, war-academy)",
        from_level="Start level (inclusive)",
        to_level="End level (inclusive)"
    )
    @app_commands.autocomplete(
        building=building_autocomplete,
        from_level=from_level_autocomplete,
        to_level=to_level_autocomplete
    )
    async def buildingcost(interaction: discord.Interaction, building: str, from_level: int, to_level: int):
        """Calculate total resources and time to upgrade a building between levels."""
        await interaction.response.defer()
        
        if from_level < 1 or to_level < from_level:
            await interaction.followup.send("❌ Invalid level range. Ensure 1 <= from_level <= to_level")
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM buildings WHERE slug = ?", (building,))
        row = cur.fetchone()
        if not row:
            await interaction.followup.send(f"❌ Building '{building}' not found in database.")
            conn.close()
            return
            
        building_id, name = row
        
        # For FC buildings, we need special handling:
        # From level X to level Y means: all X sublevels + main Y level (but not Y sublevels)
        # We query levels where level_int is in range, then filter out sublevels of to_level
        cur.execute("""
            SELECT level_text, meat, wood, coal, iron, steel, fire_crystals, fire_crystal_shards, refined_fire_crystals, time_seconds 
            FROM levels 
            WHERE building_id = ? AND level_int >= ? AND level_int <= ?
            ORDER BY id
        """, (building_id, from_level, to_level))
        totals = {
            'meat': 0,
            'wood': 0,
            'coal': 0,
            'iron': 0,
            'steel': 0,
            'fire_crystals': 0,
            'fire_crystal_shards': 0,
            'refined_fire_crystals': 0,
            'time_seconds': 0,
        }
        found = False
        for r in cur.fetchall():
            level_text, meat, wood, coal, iron, steel, fire_crystals, fire_crystal_shards, refined_fire_crystals, time_seconds = r
            
            # Parse level to determine if it's a main level or sublevel
            import re
            # Match patterns like "FC 6", "FC 6.1", "FC 6-1", "6", "6.1", "Level 6", etc.
            level_match = re.match(r'^(?:FC\s*|Level\s*)?(\d+)([.\s-]\d+)?', level_text, re.I)
            if not level_match:
                continue
            
            main_level = int(level_match.group(1))
            is_sublevel = level_match.group(2) is not None  # Has .1, -1, etc.
            
            # Logic: from=6 means "I'm AT 6, start from 6.1"
            # So skip the main from_level itself (e.g., skip "FC 6")
            if main_level == from_level and not is_sublevel:
                continue
            
            # Logic: to=7 means "stop at main level 7"
            # So skip sublevels of to_level (e.g., skip "FC 7.1, 7.2, etc.")
            if main_level == to_level and is_sublevel:
                continue
            
            found = True
            totals['meat'] += meat or 0
            totals['wood'] += wood or 0
            totals['coal'] += coal or 0
            totals['iron'] += iron or 0
            totals['steel'] += steel or 0
            totals['fire_crystals'] += fire_crystals or 0
            totals['fire_crystal_shards'] += fire_crystal_shards or 0
            totals['refined_fire_crystals'] += refined_fire_crystals or 0
            totals['time_seconds'] += time_seconds or 0

        conn.close()

        if not found:
            await interaction.followup.send(f"❌ No level rows found for {name} in range {from_level}-{to_level}.")
            return

        hrs = totals['time_seconds'] // 3600
        
        # Format time display
        if hrs >= 24:
            days = hrs // 24
            remaining_hrs = hrs % 24
            if remaining_hrs > 0:
                time_str = f"{days:,} days {remaining_hrs} hours"
            else:
                time_str = f"{days:,} days"
        else:
            time_str = f"{hrs:,} hours"
        
        embed = discord.Embed(
            title=f"🏗️ {name} Upgrade Cost",
            description=f"Level {from_level} → {to_level}",
            color=discord.Color.blue()
        )
        embed.add_field(name=f"{EMOJIS['meat']} Meat", value=format_num(totals['meat']), inline=True)
        embed.add_field(name=f"{EMOJIS['wood']} Wood", value=format_num(totals['wood']), inline=True)
        embed.add_field(name=f"{EMOJIS['coal']} Coal", value=format_num(totals['coal']), inline=True)
        embed.add_field(name=f"{EMOJIS['iron']} Iron", value=format_num(totals['iron']), inline=True)
        
        if totals['steel'] > 0:
            embed.add_field(name=f"{EMOJIS['steel']} Steel", value=format_num(totals['steel']), inline=True)
        if totals['fire_crystals'] > 0:
            embed.add_field(name=f"{EMOJIS['firecrystal']} Fire Crystals", value=format_num(totals['fire_crystals']), inline=True)
        if totals['fire_crystal_shards'] > 0:
            embed.add_field(name="💎 FC Shards", value=format_num(totals['fire_crystal_shards']), inline=True)
        if totals['refined_fire_crystals'] > 0:
            embed.add_field(name=f"{EMOJIS['refinedfc']} Refined FC", value=format_num(totals['refined_fire_crystals']), inline=True)
            
        embed.add_field(name="⏰ Total Time", value=time_str, inline=False)
        embed.set_footer(text="⚠️ Times are base values (no buffs applied) | Data from WhiteoutSurvival.wiki")

        await interaction.followup.send(embed=embed)

