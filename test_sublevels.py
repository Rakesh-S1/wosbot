import sqlite3

db = sqlite3.connect('data/buildings.db')
cur = db.cursor()

# Get FC Command Center
cur.execute('SELECT id FROM buildings WHERE slug = "fire-crystal-command-center"')
building_id = cur.fetchone()[0]

# Get levels 3-4
cur.execute('''
    SELECT level_text, meat, fire_crystals, time_seconds
    FROM levels
    WHERE building_id = ? AND level_int IN (3, 4)
    ORDER BY id
''', (building_id,))

print("FC Command Center Levels 3-4:")
print("-" * 60)
for level_text, meat, fc, time_sec in cur.fetchall():
    hours = time_sec / 3600
    days = int(hours // 24)
    hrs = int(hours % 24)
    print(f"{level_text:<12} Meat: {meat/1e6:>5.1f}M  FC: {fc:>4}  Time: {days}d {hrs:02d}h")

db.close()

print("\n" + "=" * 60)
print("Test Cases:")
print("=" * 60)
print("1. from:3 to:3.1   -> Should include: FC 3.1 only")
print("2. from:3 to:4     -> Should include: FC 3.1-3.4, FC 4 (not FC 4.1+)")
print("3. from:3.2 to:3.4 -> Should include: FC 3.2, 3.3, 3.4")
print("4. from:3.2 to:4.1 -> Should include: FC 3.2-3.4, FC 4, FC 4.1")
