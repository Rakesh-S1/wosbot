"""
Scrape building pages from whiteoutsurvival.wiki and populate SQLite DB.
Usage:
  python tools/scrape_buildings.py

Creates data/buildings.db with tables:
 - buildings(id INTEGER PK, slug TEXT UNIQUE, name TEXT)
 - levels(id PK, building_id, level_text, level_int, meat, wood, coal, iron, steel, shards, time_seconds, prerequisites, raw_resources)

This script is heuristic and may need tuning for edge-case table formats.
"""
import re
import sqlite3
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.whiteoutsurvival.wiki"
BUILDINGS_INDEX = BASE + "/buildings/"
DB_PATH = "data/buildings.db"

NUM_MULTIPLIER = {
    'k': 1_000,
    'K': 1_000,
    'm': 1_000_000,
    'M': 1_000_000,
}


def parse_amount(s: str):
    if not s:
        return None
    s = s.strip().replace(',', '')
    # Remove non-breaking spaces
    s = s.replace('\xa0', '')
    m = re.match(r"^([\d.,]+)\s*([kKmM])?$", s)
    if not m:
        # try to extract leading number
        m2 = re.search(r"([\d.,]+)\s*([kKmM])?", s)
        if not m2:
            return None
        m = m2
    num = float(m.group(1))
    if m.group(2):
        num = int(num * NUM_MULTIPLIER.get(m.group(2), 1))
    else:
        # if number is integer-like
        if '.' in str(num):
            num = int(num)
        else:
            num = int(num)
    return int(num)


def parse_timecell(s: str):
    if not s:
        return None
    s = s.strip()
    # examples: '00:10:00', '1d 03:12:00', '2d 00:00:00'
    days = 0
    m = re.search(r"(\d+)d", s)
    if m:
        days = int(m.group(1))
    # find hh:mm:ss
    m2 = re.search(r"(\d{1,2}:\d{2}:\d{2})", s)
    if m2:
        parts = m2.group(1).split(":")
        hh, mm, ss = int(parts[0]), int(parts[1]), int(parts[2])
        return days * 86400 + hh * 3600 + mm * 60 + ss
    # fallback: try to parse number of seconds
    m3 = re.search(r"(\d+)s", s)
    if m3:
        return int(m3.group(1))
    return None


def extract_resource_list(cell_text: str):
    # split on whitespace, commas
    parts = re.split(r"[\s,]+", cell_text.strip())
    vals = []
    for p in parts:
        if p == '':
            continue
        parsed = parse_amount(p)
        if parsed is not None:
            vals.append(parsed)
        else:
            # sometimes resources include plain integers (shards): allow integers
            digits = re.search(r"(\d+)", p)
            if digits:
                vals.append(int(digits.group(1)))
    return vals


def normalize_slug(url: str):
    # get last part
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]


def create_db(conn):
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS buildings (
        id INTEGER PRIMARY KEY,
        slug TEXT UNIQUE,
        name TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS levels (
        id INTEGER PRIMARY KEY,
        building_id INTEGER,
        level_text TEXT,
        level_int INTEGER,
        meat INTEGER,
        wood INTEGER,
        coal INTEGER,
        iron INTEGER,
        steel INTEGER,
        fire_crystals INTEGER,
        fire_crystal_shards INTEGER,
        refined_fire_crystals INTEGER,
        time_seconds INTEGER,
        prerequisites TEXT,
        raw_resources TEXT,
        FOREIGN KEY(building_id) REFERENCES buildings(id)
    )
    ''')
    conn.commit()


def find_building_links(session):
    r = session.get(BUILDINGS_INDEX, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/buildings/' in href:
            full = urljoin(BASE, href)
            links.add(full)
    return sorted(links)


def parse_building_page(session, url):
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1')
    name = title.get_text(strip=True) if title else normalize_slug(url).replace('-', ' ').title()

    # Find tables and extract data rows more carefully
    tables = soup.find_all('table')
    rows_data = []
    
    for table in tables:
        # Look for header row to identify columns
        header_row = table.find('tr')
        if not header_row:
            continue
            
        headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
        
        # Skip if this doesn't look like a building level table
        # Good tables have "level" column and resource-like columns
        has_level = any('level' in h or 'lv' in h or h.isdigit() for h in headers)
        has_resources = any('cost' in h or 'resources' in h or 'meat' in h or 'wood' in h for h in headers)
        
        if not (has_level or has_resources or len(headers) >= 3):
            continue
        
        # Process data rows (skip header)
        for tr in table.find_all('tr')[1:]:
            tds = tr.find_all(['td', 'th'])
            if len(tds) < 2:
                continue
                
            texts = [td.get_text(" ", strip=True) for td in tds]
            
            # First cell should look like a level (number, "Level X", or "FC X")
            first = texts[0]
            if not first:
                continue
                
            # Must have digit or FC pattern
            if not (re.search(r"^\d+$", first) or 
                   re.search(r"^Level\s+\d+", first, re.I) or
                   re.search(r"^Lv\.?\s*\d+", first, re.I) or
                   re.search(r"^FC\s*\d", first, re.I)):
                continue
            
            # Must have at least 3 cells (level, resources, time typically)
            if len(texts) < 3:
                continue
                
            rows_data.append(texts)

    # Parse rows into structured entries
    entries = []
    for cells in rows_data:
        try:
            level_text = cells[0]
            
            # Extract numeric level
            m = re.search(r"(\d+)", level_text)
            level_int = int(m.group(1)) if m else None
            
            # Standard table format: [Level, Prerequisites, Resources, Time, Power]
            # But some tables omit columns or reorder them
            
            resource_cell = None
            time_cell = None
            prereq_cell = None
            
            # Strategy: identify each column type
            for i, c in enumerate(cells[1:], 1):
                c_lower = c.lower()
                
                # Time column: has HH:MM:SS or "Xd HH:MM:SS"
                if re.search(r"\d{1,2}:\d{2}:\d{2}", c):
                    time_cell = c
                    continue
                
                # Prerequisites: contains "Lv" or "Level" or "FC" with building names
                # Examples: "Furnace Lv. 10", "Embassy FC 1 Lancer Camp FC-1"
                if re.search(r"\b(Lv\.?\s*\d+|FC\s*\d+|FC-\d+)", c, re.I) and not re.search(r"^(FC\s*\d+[\-.]?\d*)$", c, re.I):
                    prereq_cell = c
                    continue
                
                # Resource cell: has multiple numbers with k/M or multiple space-separated numbers
                resource_count = len(re.findall(r"\d+\.?\d*[kKmM]", c))
                if resource_count >= 2:
                    resource_cell = c
                    continue
                
                # Also check for cells with multiple plain numbers (early levels)
                plain_nums = re.findall(r"\b\d+\b", c)
                if len(plain_nums) >= 2 and not prereq_cell:
                    # Could be resources - but check it's not power (single number at end)
                    if i < len(cells) - 1:  # Not last column
                        resource_cell = c
            
            # Fallback logic if standard detection failed
            if not resource_cell and len(cells) >= 4:
                # Typical: [level, prereq, resources, time, power]
                prereq_cell = cells[1] if re.search(r"Lv", cells[1], re.I) else None
                resource_cell = cells[2] if len(cells) > 2 else None
                time_cell = cells[3] if len(cells) > 3 and ':' in cells[3] else None
            
            if not resource_cell:
                continue  # Skip rows without resource data
                
            raw_resources = resource_cell
            resource_vals = extract_resource_list(raw_resources)
            
            # Assign resources in standard order
            # Standard buildings: meat, wood, coal, iron, [steel]
            # War Academy/FC buildings: meat, wood, coal, iron, fire_crystal_shards, [steel], [refined_fire_crystals]
            meat = wood = coal = iron = steel = fire_crystals = fire_crystal_shards = refined_fire_crystals = None
            
            is_fc_building = 'fire-crystal' in url or 'war-academy' in url or 'FC' in level_text.upper()
            
            if is_fc_building:
                # FC buildings order: meat, wood, coal, iron, fire_crystals, refined_fire_crystals
                if len(resource_vals) >= 1:
                    meat = resource_vals[0]
                if len(resource_vals) >= 2:
                    wood = resource_vals[1]
                if len(resource_vals) >= 3:
                    coal = resource_vals[2]
                if len(resource_vals) >= 4:
                    iron = resource_vals[3]
                if len(resource_vals) >= 5:
                    fire_crystals = resource_vals[4]
                if len(resource_vals) >= 6:
                    refined_fire_crystals = resource_vals[5]
            else:
                # Standard buildings: meat, wood, coal, iron, steel
                if len(resource_vals) >= 1:
                    meat = resource_vals[0]
                if len(resource_vals) >= 2:
                    wood = resource_vals[1]
                if len(resource_vals) >= 3:
                    coal = resource_vals[2]
                if len(resource_vals) >= 4:
                    iron = resource_vals[3]
                if len(resource_vals) >= 5:
                    steel = resource_vals[4]
            
            time_seconds = parse_timecell(time_cell) if time_cell else None
            prerequisites = prereq_cell or ''
            
            entries.append({
                'level_text': level_text,
                'level_int': level_int,
                'meat': meat,
                'wood': wood,
                'coal': coal,
                'iron': iron,
                'steel': steel,
                'fire_crystals': fire_crystals,
                'fire_crystal_shards': fire_crystal_shards,
                'refined_fire_crystals': refined_fire_crystals,
                'time_seconds': time_seconds,
                'prerequisites': prerequisites,
                'raw_resources': raw_resources,
            })
        except Exception as e:
            print(f"Failed parsing row {cells[:3]}... : {e}")
            
    return name, entries


def save_building(conn, slug, name, entries):
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO buildings(slug, name) VALUES (?, ?)', (slug, name))
    conn.commit()
    cur.execute('SELECT id FROM buildings WHERE slug = ?', (slug,))
    row = cur.fetchone()
    if not row:
        raise RuntimeError('Failed to insert building ' + slug)
    bid = row[0]
    ins = []
    for e in entries:
        ins.append((bid, e['level_text'], e['level_int'], e['meat'], e['wood'], e['coal'], e['iron'], e['steel'], e['fire_crystals'], e['fire_crystal_shards'], e['refined_fire_crystals'], e['time_seconds'], e['prerequisites'], e['raw_resources']))
    cur.executemany('''
        INSERT INTO levels(building_id, level_text, level_int, meat, wood, coal, iron, steel, fire_crystals, fire_crystal_shards, refined_fire_crystals, time_seconds, prerequisites, raw_resources)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', ins)
    conn.commit()


def main():
    session = requests.Session()
    conn = sqlite3.connect(DB_PATH)
    create_db(conn)
    
    # Clean existing data
    cur = conn.cursor()
    cur.execute('DELETE FROM levels')
    cur.execute('DELETE FROM buildings')
    conn.commit()
    
    links = find_building_links(session)
    print('Found', len(links), 'building links')
    
    # Filter to English main building pages only
    filtered = []
    for url in links:
        # Skip non-English (/de/, /fr/, etc) and index pages
        if '/buildings/' in url and not any(f'/{lang}/' in url for lang in ['de', 'es', 'fr', 'ja', 'ko', 'pt', 'tw', 'arb']):
            # Must end with a building slug, not just /buildings/
            if url.rstrip('/') != 'https://www.whiteoutsurvival.wiki/buildings':
                filtered.append(url)
    
    print(f'Filtered to {len(filtered)} English building pages')
    
    for url in filtered:
        try:
            print('Processing', url)
            name, entries = parse_building_page(session, url)
            slug = normalize_slug(url)
            if not entries:
                print('  ⚠ No entries parsed for', slug)
                continue
            save_building(conn, slug, name, entries)
            print(f'  ✓ Saved {len(entries)} levels for {name}')
            # be polite
            time.sleep(1)
        except Exception as e:
            print('  ✗ Error for', url, e)

    conn.close()
    print('Done. DB at', DB_PATH)

if __name__ == '__main__':
    main()
