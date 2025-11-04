"""
Scrape all research data from WhiteoutSurvival wiki
Creates data/research.db with all research types
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import time

# Base URL
BASE_URL = "https://www.whiteoutsurvival.wiki"
RESEARCH_URL = f"{BASE_URL}/research/"

def init_database():
    """Initialize the research database"""
    conn = sqlite3.connect('data/research.db')
    cur = conn.cursor()
    
    # Research categories/types table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS research_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Research items table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS research_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category_id INTEGER,
            description TEXT,
            icon_url TEXT,
            FOREIGN KEY (category_id) REFERENCES research_categories (id)
        )
    ''')
    
    # Research levels table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS research_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            research_id INTEGER NOT NULL,
            level INTEGER NOT NULL,
            meat INTEGER,
            wood INTEGER,
            coal INTEGER,
            iron INTEGER,
            steel INTEGER,
            time_seconds INTEGER,
            research_center_level INTEGER,
            prerequisites TEXT,
            effect TEXT,
            power INTEGER,
            FOREIGN KEY (research_id) REFERENCES research_items (id),
            UNIQUE(research_id, level)
        )
    ''')
    
    conn.commit()
    return conn

def parse_time_string(time_str):
    """Parse time string like '00:01:48' or '1d 02' to seconds"""
    if not time_str or time_str.strip() == '':
        return 0
    
    time_str = time_str.strip()
    
    # Handle "Xd Y" format (e.g., "1d 02", "2d 18")
    if 'd' in time_str.lower():
        parts = time_str.lower().replace('d', ' ').split()
        if len(parts) >= 2:
            try:
                days = int(parts[0])
                hours = int(parts[1])
                return days * 86400 + hours * 3600
            except:
                return 0
    
    # Handle "HH:MM:SS" format
    parts = time_str.split(':')
    if len(parts) == 3:
        try:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        except:
            return 0
    
    return 0

def parse_number(num_str):
    """Parse number strings with spaces (e.g., '5 400' -> 5400)"""
    if not num_str or num_str.strip() == '':
        return 0
    try:
        return int(num_str.replace(' ', '').replace(',', ''))
    except:
        return 0

def get_all_research_links():
    """Get all research item links from the main research page"""
    print(f"Fetching research list from {RESEARCH_URL}")
    response = requests.get(RESEARCH_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    research_links = []
    
    # Find all research links
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/research/' in href and href != '/research/' and href.endswith('/'):
            full_url = href if href.startswith('http') else BASE_URL + href
            name = link.get_text(strip=True)
            if name:
                research_links.append({
                    'name': name,
                    'url': full_url,
                    'slug': href.split('/')[-2]
                })
    
    # Remove duplicates
    unique_links = {}
    for item in research_links:
        if item['slug'] not in unique_links:
            unique_links[item['slug']] = item
    
    print(f"Found {len(unique_links)} unique research items")
    return list(unique_links.values())

def scrape_research_page(url, name, slug):
    """Scrape a single research page"""
    print(f"  Scraping: {name}")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {
            'name': name,
            'slug': slug,
            'description': '',
            'icon_url': '',
            'levels': []
        }
        
        # Get description
        desc_section = soup.find('div', {'id': 'description'})
        if desc_section:
            desc_p = desc_section.find_next('p')
            if desc_p:
                data['description'] = desc_p.get_text(strip=True)
        
        # Get icon URL
        icon = soup.find('img', {'class': 'post_image'})
        if not icon:
            icon = soup.find('img', src=re.compile(r'science_icon'))
        if icon:
            data['icon_url'] = icon.get('src', '')
        
        # Find the requirements table
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue
            
            # Check if this looks like a research levels table
            headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
            
            # Parse data rows
            for row in rows[1:]:
                cells = row.find_all('td')
                if len(cells) < 6:  # Level, Prerequisites, Resources, Time, Bonus, Power
                    continue
                
                try:
                    level = parse_number(cells[0].get_text(strip=True))
                    if level == 0:
                        continue
                    
                    # Prerequisites cell (Research Center level + other research)
                    prereq_text = cells[1].get_text(strip=True)
                    rc_level_match = re.search(r'Research Center (\d+)', prereq_text)
                    rc_level = int(rc_level_match.group(1)) if rc_level_match else 0
                    
                    # Resources - parse img tags and their corresponding span values
                    resource_cell = cells[2]
                    meat = wood = coal = iron = steel = 0
                    
                    imgs = resource_cell.find_all('img')
                    spans = resource_cell.find_all('span')
                    
                    for i, img in enumerate(imgs):
                        if i < len(spans):
                            value_text = spans[i].get_text(strip=True)
                            value = parse_number(value_text)
                            
                            # Match resource by icon filename
                            src = img.get('src', '')
                            if 'item_icon_102' in src:  # Meat
                                meat = value
                            elif 'item_icon_103' in src:  # Wood
                                wood = value
                            elif 'item_icon_104' in src:  # Coal
                                coal = value
                            elif 'item_icon_105' in src:  # Iron
                                iron = value
                            elif 'item_icon_106' in src:  # Steel
                                steel = value
                    
                    # Time
                    time_str = cells[3].get_text(strip=True)
                    time_seconds = parse_time_string(time_str)
                    
                    # Effect
                    effect = cells[4].get_text(strip=True) if len(cells) > 4 else ''
                    
                    # Power
                    power = parse_number(cells[5].get_text(strip=True)) if len(cells) > 5 else 0
                    
                    data['levels'].append({
                        'level': level,
                        'research_center_level': rc_level,
                        'prerequisites': prereq_text,
                        'meat': meat,
                        'wood': wood,
                        'coal': coal,
                        'iron': iron,
                        'steel': steel,
                        'time_seconds': time_seconds,
                        'effect': effect,
                        'power': power
                    })
                except Exception as e:
                    print(f"    Error parsing row: {e}")
                    continue
        
        return data if data['levels'] else None
        
    except Exception as e:
        print(f"    Error scraping {url}: {e}")
        return None

def categorize_research(name):
    """Determine research category based on name"""
    name_lower = name.lower()
    
    if any(word in name_lower for word in ['lancer', 'marksman', 'infantry', 'armor', 'upgrade', 'training']):
        return 'Military'
    elif any(word in name_lower for word in ['battle', 'combat', 'attack', 'defense', 'formation', 'tactics']):
        return 'War Academy'
    elif any(word in name_lower for word in ['construction', 'research', 'gathering', 'load', 'march']):
        return 'Development'
    elif any(word in name_lower for word in ['meat', 'wood', 'coal', 'iron', 'steel', 'production', 'gathering']):
        return 'Economy'
    else:
        return 'Other'

def save_to_database(conn, research_data_list):
    """Save all research data to database"""
    cur = conn.cursor()
    
    # Get or create categories
    categories = {}
    for data in research_data_list:
        if not data:
            continue
        category_name = categorize_research(data['name'])
        if category_name not in categories:
            slug = category_name.lower().replace(' ', '-')
            cur.execute('INSERT OR IGNORE INTO research_categories (name, slug) VALUES (?, ?)',
                       (category_name, slug))
            conn.commit()
            cur.execute('SELECT id FROM research_categories WHERE slug = ?', (slug,))
            categories[category_name] = cur.fetchone()[0]
    
    saved_count = 0
    for data in research_data_list:
        if not data or not data['levels']:
            continue
        
        try:
            category_name = categorize_research(data['name'])
            category_id = categories[category_name]
            
            # Insert research item
            cur.execute('''
                INSERT OR REPLACE INTO research_items (name, slug, category_id, description, icon_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['name'], data['slug'], category_id, data['description'], data['icon_url']))
            
            research_id = cur.lastrowid
            
            # Insert levels
            for level_data in data['levels']:
                cur.execute('''
                    INSERT OR REPLACE INTO research_levels 
                    (research_id, level, meat, wood, coal, iron, steel, time_seconds, 
                     research_center_level, prerequisites, effect, power)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    research_id, level_data['level'], level_data['meat'], level_data['wood'],
                    level_data['coal'], level_data['iron'], level_data['steel'],
                    level_data['time_seconds'], level_data['research_center_level'],
                    level_data['prerequisites'], level_data['effect'], level_data['power']
                ))
            
            conn.commit()
            saved_count += 1
            print(f"  Saved {data['name']} ({len(data['levels'])} levels)")
            
        except Exception as e:
            print(f"  ✗ Error saving {data['name']}: {e}")
            conn.rollback()
    
    return saved_count

def main():
    print("="*60)
    print("WhiteoutSurvival Research Scraper")
    print("="*60)
    
    # Initialize database
    conn = init_database()
    print("Database initialized")
    
    # Get all research links
    research_links = get_all_research_links()
    
    if not research_links:
        print("✗ No research items found!")
        return
    
    # Scrape each research page
    print(f"\nScraping {len(research_links)} research items...")
    research_data_list = []
    
    for i, item in enumerate(research_links, 1):
        print(f"[{i}/{len(research_links)}]", end=" ")
        data = scrape_research_page(item['url'], item['name'], item['slug'])
        if data:
            research_data_list.append(data)
        time.sleep(0.5)  # Be nice to the server
    
    # Save to database
    print(f"\n\nSaving to database...")
    saved_count = save_to_database(conn, research_data_list)
    
    # Summary
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM research_items')
    total_research = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM research_levels')
    total_levels = cur.fetchone()[0]
    cur.execute('SELECT research_categories.name, COUNT(*) as cnt FROM research_categories JOIN research_items ON research_categories.id = research_items.category_id GROUP BY research_categories.name')
    categories = cur.fetchall()
    
    print("\n" + "="*60)
    print("SCRAPING COMPLETE!")
    print("="*60)
    print(f"Total research items: {total_research}")
    print(f"Total levels: {total_levels}")
    print(f"\nBy category:")
    for cat_name, count in categories:
        print(f"  {cat_name}: {count} items")
    print("="*60)
    
    conn.close()

if __name__ == '__main__':
    main()
