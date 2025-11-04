"""
Test script to verify sublevel filtering logic for /buildingcost command
Tests various from/to level combinations to ensure correct behavior
"""
import sqlite3
import re

def parse_level(level_str):
    """Parse level string like '3', '3.1', '3-1', 'FC 3.1' and return (main_level, sublevel)"""
    # Strip any leading 'FC' or 'Level' prefix
    clean = re.sub(r'^(?:FC|Level)\s*', '', level_str.strip(), flags=re.I)
    
    # Match main level and optional sublevel (separated by ., -, or space)
    match = re.match(r'^(\d+)(?:[.\s-](\d+))?$', clean)
    if not match:
        return None, None
    
    main_level = int(match.group(1))
    sublevel = int(match.group(2)) if match.group(2) else None
    return main_level, sublevel

def test_range(building_slug, from_level, to_level):
    """Test a specific range and show what levels are included"""
    print(f"\n{'='*80}")
    print(f"TEST: {building_slug} from:{from_level} to:{to_level}")
    print(f"{'='*80}")
    
    # Parse levels
    from_main, from_sub = parse_level(from_level)
    to_main, to_sub = parse_level(to_level)
    
    print(f"Parsed FROM: main={from_main}, sub={from_sub}")
    print(f"Parsed TO: main={to_main}, sub={to_sub}")
    
    # Connect to database
    conn = sqlite3.connect('data/buildings.db')
    cur = conn.cursor()
    
    # Get building_id
    cur.execute("SELECT id, name FROM buildings WHERE slug = ?", (building_slug,))
    result = cur.fetchone()
    if not result:
        print(f"❌ Building not found: {building_slug}")
        conn.close()
        return
    
    building_id, building_name = result
    print(f"Building: {building_name} (ID: {building_id})")
    
    # Query all levels in the range
    cur.execute("""
        SELECT level_text, meat, wood, coal, iron, steel, fire_crystals, fire_crystal_shards, refined_fire_crystals, time_seconds 
        FROM levels 
        WHERE building_id = ? AND level_int >= ? AND level_int <= ?
        ORDER BY id
    """, (building_id, from_main, to_main))
    
    print(f"\n{'Level':<15} {'Meat':<12} {'Fire Crystals':<15} {'Time':<15} {'Included?':<10}")
    print("-" * 80)
    
    totals = {'meat': 0, 'fire_crystals': 0, 'time_seconds': 0}
    included_count = 0
    
    for row in cur.fetchall():
        level_text, meat, wood, coal, iron, steel, fire_crystals, fire_crystal_shards, refined_fire_crystals, time_seconds = row
        
        # Parse the level_text to determine main level and sublevel
        level_match = re.match(r'^(?:FC\s*|Level\s*)?(\d+)([.\s-](\d+))?', level_text, re.I)
        if not level_match:
            continue
        
        current_main = int(level_match.group(1))
        current_sub = int(level_match.group(3)) if level_match.group(3) else None
        
        # Apply filtering logic (same as in resource_commands.py)
        included = True
        reason = ""
        
        # Skip if before from_level
        if current_main == from_main:
            if from_sub is not None:
                # User specified from sublevel (e.g., 3.2) - means user is AT 3.2
                if current_sub is None:
                    # Skip main level 3 if user is at 3.2
                    included = False
                    reason = f"Skip main level (from={from_level})"
                elif current_sub <= from_sub:
                    # Skip the current sublevel and all sublevels before it
                    included = False
                    reason = f"Skip sublevel <= {from_sub} (user is at {from_level})"
            else:
                # User specified just main level (e.g., 3) - skip the main level itself
                if current_sub is None:
                    included = False
                    reason = f"Skip main level (user is at {from_level})"
        
        # Skip if after to_level
        if current_main == to_main:
            if to_sub is not None:
                # User specified to sublevel (e.g., 4.2)
                if current_sub is not None and current_sub > to_sub:
                    # Skip sublevels after the specified one
                    included = False
                    reason = f"Skip sublevel after {to_sub}"
            else:
                # User specified just main level (e.g., 4)
                # Include main level but skip its sublevels
                if current_sub is not None:
                    included = False
                    reason = f"Skip sublevel (to={to_level})"
        
        # Format time
        hrs = time_seconds // 3600 if time_seconds else 0
        if hrs >= 24:
            days = hrs // 24
            remaining_hrs = hrs % 24
            time_str = f"{days}d {remaining_hrs}h"
        else:
            time_str = f"{hrs}h"
        
        # Format output
        meat_str = f"{meat/1_000_000:.0f}M" if meat else "0"
        fc_str = f"{fire_crystals}" if fire_crystals else "0"
        
        status = "✓ YES" if included else "✗ NO"
        if not included:
            status += f" ({reason})"
        
        print(f"{level_text:<15} {meat_str:<12} {fc_str:<15} {time_str:<15} {status}")
        
        if included:
            totals['meat'] += meat or 0
            totals['fire_crystals'] += fire_crystals or 0
            totals['time_seconds'] += time_seconds or 0
            included_count += 1
    
    conn.close()
    
    # Print summary
    print("-" * 80)
    print(f"\n📊 SUMMARY:")
    print(f"   Included levels: {included_count}")
    print(f"   Total Meat: {totals['meat']/1_000_000:.1f}M")
    print(f"   Total Fire Crystals: {totals['fire_crystals']}")
    
    hrs = totals['time_seconds'] // 3600
    if hrs >= 24:
        days = hrs // 24
        remaining_hrs = hrs % 24
        print(f"   Total Time: {days} days {remaining_hrs} hours ({hrs} hours)")
    else:
        print(f"   Total Time: {hrs} hours")

def main():
    print("SUBLEVEL LOGIC TEST SCRIPT")
    print("Testing Fire Crystal Command Center upgrade calculations")
    
    # Test Case 1: from:3 to:3.1 (should include only FC 3-1)
    test_range("fire-crystal-command-center", "3", "3.1")
    
    # Test Case 2: from:3 to:4 (should include FC 3-1, 3-2, 3-3, 3-4, and FC 4)
    test_range("fire-crystal-command-center", "3", "4")
    
    # Test Case 3: from:3.2 to:3.4 (should include FC 3-2, 3-3, 3-4 only)
    test_range("fire-crystal-command-center", "3.2", "3.4")
    
    # Test Case 4: from:3.2 to:4.1 (should include FC 3-2, 3-3, 3-4, FC 4, FC 4-1)
    test_range("fire-crystal-command-center", "3.2", "4.1")
    
    # Test Case 5: from:3 to:3 (edge case - should include nothing since user is at 3)
    test_range("fire-crystal-command-center", "3", "3")
    
    print(f"\n{'='*80}")
    print("✅ All tests complete!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
