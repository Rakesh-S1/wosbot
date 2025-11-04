import sqlite3
from typing import Optional
import re

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


def parse_level(level_str):
    """Parse level string and return (main_level, sublevel) tuple"""
    level_str = str(level_str).strip()
    
    # Remove "FC" or "Level" prefix if present
    level_str = re.sub(r'^(?:FC|Level)\s*', '', level_str, flags=re.I)
    
    # Match patterns: "3", "3.1", "3-1", "3 1"
    match = re.match(r'^(\d+)(?:[.\s-](\d+))?$', level_str)
    if not match:
        return None, None
    
    main_level = int(match.group(1))
    sublevel = int(match.group(2)) if match.group(2) else None
    return main_level, sublevel


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
            
            # Return string values instead of integers
            result = [app_commands.Choice(name=str(lvl), value=str(lvl)) for lvl in levels[:25]]
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
                try:
                    # Parse from_level to get the main level
                    from_main, from_sub = parse_level(from_level)
                    if from_main is not None:
                        levels = [lvl for lvl in levels if lvl >= from_main]
                except:
                    pass  # If parsing fails, show all levels
            
            # Filter based on user input
            if current:
                levels = [lvl for lvl in levels if str(lvl).startswith(current)]
            
            # Return string values instead of integers
            result = [app_commands.Choice(name=str(lvl), value=str(lvl)) for lvl in levels[:25]]
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
        from_level="Start level (e.g., 3 or 3.1)",
        to_level="End level (e.g., 4 or 4.2)"
    )
    @app_commands.autocomplete(
        building=building_autocomplete,
        from_level=from_level_autocomplete,
        to_level=to_level_autocomplete
    )
    async def buildingcost(interaction: discord.Interaction, building: str, from_level: str, to_level: str):
        """Calculate total resources and time to upgrade a building between levels."""
        await interaction.response.defer()
        
        # Parse level strings (support formats like "3", "3.1", "3-1", "FC 3.1")
        from_main, from_sub = parse_level(from_level)
        to_main, to_sub = parse_level(to_level)
        
        if from_main is None or to_main is None:
            await interaction.followup.send("❌ Invalid level format. Use formats like: 3, 3.1, 3-1")
            return
        
        if from_main < 1 or to_main < from_main:
            await interaction.followup.send("❌ Invalid level range. Ensure 1 <= from_level <= to_level")
            return
        
        if from_main == to_main and from_sub is not None and to_sub is not None and to_sub < from_sub:
            await interaction.followup.send("❌ Invalid sublevel range within the same main level")
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
        
        # Query all levels in the range
        cur.execute("""
            SELECT level_text, meat, wood, coal, iron, steel, fire_crystals, fire_crystal_shards, refined_fire_crystals, time_seconds 
            FROM levels 
            WHERE building_id = ? AND level_int >= ? AND level_int <= ?
            ORDER BY id
        """, (building_id, from_main, to_main))
        
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
            
            # Parse the level_text to determine main level and sublevel
            import re
            level_match = re.match(r'^(?:FC\s*|Level\s*)?(\d+)([.\s-](\d+))?', level_text, re.I)
            if not level_match:
                continue
            
            current_main = int(level_match.group(1))
            current_sub = int(level_match.group(3)) if level_match.group(3) else None
            
            # Apply filtering based on from_level and to_level
            # Skip if before from_level
            if current_main == from_main:
                if from_sub is not None:
                    # User specified from sublevel (e.g., 3.2) - means user is AT 3.2
                    if current_sub is None:
                        # Skip main level 3 if user is at 3.2
                        continue
                    elif current_sub <= from_sub:
                        # Skip the current sublevel and all sublevels before it
                        continue
                else:
                    # User specified just main level (e.g., 3) - skip the main level itself
                    if current_sub is None:
                        continue
            
            # Skip if after to_level
            if current_main == to_main:
                if to_sub is not None:
                    # User specified to sublevel (e.g., 4.2)
                    if current_sub is not None and current_sub > to_sub:
                        # Skip sublevels after the specified one
                        continue
                else:
                    # User specified just main level (e.g., 4)
                    # Include main level but skip its sublevels
                    if current_sub is not None:
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

