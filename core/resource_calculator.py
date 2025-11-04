"""
Building Cost Database for Whiteout Survival
Comprehensive database of all building upgrade costs from level 1-30
War Academy uses separate FC (Fire Crystal) system: FC 1 to FC 10
Data source: WhiteoutSurvival.wiki (Official Wiki)
"""

# ============================================================================
# REGULAR BUILDINGS (Levels 1-30)
# ============================================================================

BUILDING_COSTS = {
    "furnace": {
        1: {"meat": 0, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 0},
        2: {"meat": 180, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 6},
        3: {"meat": 805, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 60},
        4: {"meat": 1800, "wood": 360, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 180},
        5: {"meat": 7600, "wood": 1500, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 600},
        6: {"meat": 19000, "wood": 3800, "coal": 960, "iron": 0, "steel": 0, "time_seconds": 1800},
        7: {"meat": 69000, "wood": 13000, "coal": 3400, "iron": 0, "steel": 0, "time_seconds": 3600},
        8: {"meat": 120000, "wood": 25000, "coal": 6300, "iron": 0, "steel": 0, "time_seconds": 9000},
        9: {"meat": 260000, "wood": 52000, "coal": 13000, "iron": 0, "steel": 0, "time_seconds": 16200},
        10: {"meat": 460000, "wood": 92000, "coal": 23000, "iron": 0, "steel": 0, "time_seconds": 21600},
        11: {"meat": 1300000, "wood": 1300000, "coal": 260000, "iron": 65000, "steel": 0, "time_seconds": 27000},
        12: {"meat": 1600000, "wood": 1600000, "coal": 330000, "iron": 84000, "steel": 0, "time_seconds": 32400},
        13: {"meat": 2300000, "wood": 2300000, "coal": 470000, "iron": 110000, "steel": 0, "time_seconds": 39600},
        14: {"meat": 3100000, "wood": 3100000, "coal": 630000, "iron": 150000, "steel": 0, "time_seconds": 50400},
        15: {"meat": 4600000, "wood": 4600000, "coal": 930000, "iron": 230000, "steel": 0, "time_seconds": 64800},
        16: {"meat": 5900000, "wood": 5900000, "coal": 1100000, "iron": 290000, "steel": 0, "time_seconds": 109680},
        17: {"meat": 9300000, "wood": 9300000, "coal": 1800000, "iron": 460000, "steel": 0, "time_seconds": 131640},
        18: {"meat": 12000000, "wood": 12000000, "coal": 2500000, "iron": 620000, "steel": 0, "time_seconds": 157980},
        19: {"meat": 15000000, "wood": 15000000, "coal": 3100000, "iron": 780000, "steel": 0, "time_seconds": 236400},
        20: {"meat": 21000000, "wood": 21000000, "coal": 4300000, "iron": 1000000, "steel": 0, "time_seconds": 295080},
        21: {"meat": 27000000, "wood": 27000000, "coal": 5400000, "iron": 1300000, "steel": 0, "time_seconds": 385140},
        22: {"meat": 36000000, "wood": 36000000, "coal": 7200000, "iron": 1800000, "steel": 0, "time_seconds": 571740},
        23: {"meat": 44000000, "wood": 44000000, "coal": 8900000, "iron": 2200000, "steel": 0, "time_seconds": 803280},
        24: {"meat": 60000000, "wood": 60000000, "coal": 12000000, "iron": 3000000, "steel": 0, "time_seconds": 1129980},
        25: {"meat": 81000000, "wood": 81000000, "coal": 16000000, "iron": 4000000, "steel": 0, "time_seconds": 1579320},
        26: {"meat": 100000000, "wood": 100000000, "coal": 21000000, "iron": 5200000, "steel": 0, "time_seconds": 1818360},
        27: {"meat": 140000000, "wood": 140000000, "coal": 24000000, "iron": 7400000, "steel": 0, "time_seconds": 2189580},
        28: {"meat": 190000000, "wood": 190000000, "coal": 39000000, "iron": 9900000, "steel": 0, "time_seconds": 2513520},
        29: {"meat": 240000000, "wood": 240000000, "coal": 49000000, "iron": 12000000, "steel": 0, "time_seconds": 2890920},
        30: {"meat": 300000000, "wood": 300000000, "coal": 60000000, "iron": 15000000, "steel": 0, "time_seconds": 3459420},
    },
    
    "infantry_camp": {
        1: {"meat": 0, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 2},
        2: {"meat": 140, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 9},
        3: {"meat": 645, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 45},
        4: {"meat": 1400, "wood": 285, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 135},
        5: {"meat": 6000, "wood": 1200, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 270},
        6: {"meat": 15000, "wood": 3000, "coal": 765, "iron": 0, "steel": 0, "time_seconds": 540},
        7: {"meat": 55000, "wood": 11000, "coal": 2700, "iron": 0, "steel": 0, "time_seconds": 1080},
        8: {"meat": 100000, "wood": 20000, "coal": 5000, "iron": 0, "steel": 0, "time_seconds": 1620},
        9: {"meat": 200000, "wood": 41000, "coal": 10000, "iron": 0, "steel": 0, "time_seconds": 2430},
        10: {"meat": 360000, "wood": 73000, "coal": 18000, "iron": 0, "steel": 0, "time_seconds": 3240},
        11: {"meat": 460000, "wood": 460000, "coal": 92000, "iron": 23000, "steel": 0, "time_seconds": 4050},
        12: {"meat": 580000, "wood": 580000, "coal": 110000, "iron": 29000, "steel": 0, "time_seconds": 4860},
        13: {"meat": 830000, "wood": 830000, "coal": 160000, "iron": 41000, "steel": 0, "time_seconds": 5940},
        14: {"meat": 1100000, "wood": 1100000, "coal": 220000, "iron": 55000, "steel": 0, "time_seconds": 7560},
        15: {"meat": 1600000, "wood": 1600000, "coal": 320000, "iron": 81000, "steel": 0, "time_seconds": 9720},
        16: {"meat": 2000000, "wood": 2000000, "coal": 410000, "iron": 100000, "steel": 0, "time_seconds": 16440},
        17: {"meat": 3200000, "wood": 3200000, "coal": 650000, "iron": 160000, "steel": 0, "time_seconds": 19740},
        18: {"meat": 4300000, "wood": 4300000, "coal": 870000, "iron": 210000, "steel": 0, "time_seconds": 23700},
        19: {"meat": 5400000, "wood": 5400000, "coal": 1000000, "iron": 270000, "steel": 0, "time_seconds": 35550},
        20: {"meat": 7500000, "wood": 7500000, "coal": 1500000, "iron": 370000, "steel": 0, "time_seconds": 44430},
        21: {"meat": 9500000, "wood": 9500000, "coal": 1900000, "iron": 470000, "steel": 0, "time_seconds": 57750},
        22: {"meat": 12000000, "wood": 12000000, "coal": 2500000, "iron": 630000, "steel": 0, "time_seconds": 86640},
        23: {"meat": 15000000, "wood": 15000000, "coal": 3100000, "iron": 490000, "steel": 0, "time_seconds": 120120},
        24: {"meat": 21000000, "wood": 21000000, "coal": 4200000, "iron": 1000000, "steel": 0, "time_seconds": 168660},
        25: {"meat": 28000000, "wood": 28000000, "coal": 5700000, "iron": 1400000, "steel": 0, "time_seconds": 237780},
        26: {"meat": 36000000, "wood": 36000000, "coal": 7300000, "iron": 1800000, "steel": 0, "time_seconds": 271020},
        27: {"meat": 52000000, "wood": 52000000, "coal": 10000000, "iron": 2600000, "steel": 0, "time_seconds": 328140},
        28: {"meat": 69000000, "wood": 69000000, "coal": 13000000, "iron": 3400000, "steel": 0, "time_seconds": 376140},
        29: {"meat": 86000000, "wood": 86000000, "coal": 17000000, "iron": 4300000, "steel": 0, "time_seconds": 432780},
        30: {"meat": 100000000, "wood": 100000000, "coal": 21000000, "iron": 5200000, "steel": 0, "time_seconds": 518400},
    },
    
    "research_center": {
        1: {"meat": 105, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 2},
        2: {"meat": 160, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 9},
        3: {"meat": 725, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 45},
        4: {"meat": 1600, "wood": 320, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 135},
        5: {"meat": 6800, "wood": 1300, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 270},
        6: {"meat": 17000, "wood": 3400, "coal": 860, "iron": 0, "steel": 0, "time_seconds": 540},
        7: {"meat": 62000, "wood": 12000, "coal": 3100, "iron": 0, "steel": 0, "time_seconds": 1080},
        8: {"meat": 110000, "wood": 22000, "coal": 5600, "iron": 0, "steel": 0, "time_seconds": 1620},
        9: {"meat": 230000, "wood": 47000, "coal": 11000, "iron": 0, "steel": 0, "time_seconds": 2430},
        10: {"meat": 410000, "wood": 82000, "coal": 20000, "iron": 0, "steel": 0, "time_seconds": 3240},
        11: {"meat": 520000, "wood": 520000, "coal": 100000, "iron": 26000, "steel": 0, "time_seconds": 4050},
        12: {"meat": 670000, "wood": 670000, "coal": 130000, "iron": 33000, "steel": 0, "time_seconds": 4860},
        13: {"meat": 950000, "wood": 950000, "coal": 190000, "iron": 47000, "steel": 0, "time_seconds": 5940},
        14: {"meat": 1200000, "wood": 1200000, "coal": 250000, "iron": 63000, "steel": 0, "time_seconds": 7560},
        15: {"meat": 1800000, "wood": 1800000, "coal": 370000, "iron": 93000, "steel": 0, "time_seconds": 9720},
        16: {"meat": 2300000, "wood": 2300000, "coal": 470000, "iron": 110000, "steel": 0, "time_seconds": 16440},
        17: {"meat": 3700000, "wood": 3700000, "coal": 740000, "iron": 180000, "steel": 0, "time_seconds": 19740},
        18: {"meat": 5000000, "wood": 5000000, "coal": 1000000, "iron": 250000, "steel": 0, "time_seconds": 23700},
        19: {"meat": 6200000, "wood": 6200000, "coal": 1200000, "iron": 310000, "steel": 0, "time_seconds": 35550},
        20: {"meat": 8600000, "wood": 8600000, "coal": 1700000, "iron": 430000, "steel": 0, "time_seconds": 44430},
        21: {"meat": 10000000, "wood": 10000000, "coal": 2100000, "iron": 540000, "steel": 0, "time_seconds": 57750},
        22: {"meat": 14000000, "wood": 14000000, "coal": 2800000, "iron": 720000, "steel": 0, "time_seconds": 86640},
        23: {"meat": 17000000, "wood": 17000000, "coal": 3500000, "iron": 890000, "steel": 0, "time_seconds": 120120},
        24: {"meat": 24000000, "wood": 24000000, "coal": 4800000, "iron": 1200000, "steel": 0, "time_seconds": 168660},
        25: {"meat": 32000000, "wood": 32000000, "coal": 6500000, "iron": 1600000, "steel": 0, "time_seconds": 237780},
        26: {"meat": 42000000, "wood": 42000000, "coal": 8400000, "iron": 2100000, "steel": 0, "time_seconds": 271020},
        27: {"meat": 59000000, "wood": 59000000, "coal": 11000000, "iron": 2900000, "steel": 0, "time_seconds": 328140},
        28: {"meat": 79000000, "wood": 79000000, "coal": 15000000, "iron": 3900000, "steel": 0, "time_seconds": 376140},
        29: {"meat": 98000000, "wood": 98000000, "coal": 19000000, "iron": 4900000, "steel": 0, "time_seconds": 432780},
        30: {"meat": 120000000, "wood": 120000000, "coal": 24000000, "iron": 6000000, "steel": 0, "time_seconds": 518400},
    },
    
    # TODO: Add these buildings with data from wiki
    "lancer_camp": {
        # Placeholder - needs data from WhiteoutSurvival.wiki
    },
    "marksman_camp": {
        # Placeholder - needs data from WhiteoutSurvival.wiki
    },
    "command_center": {
        # Placeholder - needs data from WhiteoutSurvival.wiki
    },
    "embassy": {
        # Placeholder - needs data from WhiteoutSurvival.wiki
    },
    "infirmary": {
        # Placeholder - needs data from WhiteoutSurvival.wiki
    },
}

# ============================================================================
# WAR ACADEMY (Fire Crystal System - Completely Separate)
# ============================================================================

WAR_ACADEMY_COSTS = {
    "FC 1": {"meat": 0, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "shards": 0, "time_seconds": 2},
    "FC 1-1": {"meat": 36000000, "wood": 36000000, "coal": 7200000, "iron": 1800000, "steel": 0, "shards": 71, "time_seconds": 155520},
    "FC 1-2": {"meat": 36000000, "wood": 36000000, "coal": 7200000, "iron": 1800000, "steel": 0, "shards": 71, "time_seconds": 155520},
    "FC 1-3": {"meat": 36000000, "wood": 36000000, "coal": 7200000, "iron": 1800000, "steel": 0, "shards": 71, "time_seconds": 155520},
    "FC 1-4": {"meat": 36000000, "wood": 36000000, "coal": 7200000, "iron": 1800000, "steel": 0, "shards": 71, "time_seconds": 155520},
    "FC 2": {"meat": 36000000, "wood": 36000000, "coal": 7200000, "iron": 1800000, "steel": 0, "shards": 71, "time_seconds": 155520},
    "FC 2-1": {"meat": 39000000, "wood": 39000000, "coal": 7900000, "iron": 1900000, "steel": 0, "shards": 107, "time_seconds": 189120},
    "FC 2-2": {"meat": 39000000, "wood": 39000000, "coal": 7900000, "iron": 1900000, "steel": 0, "shards": 107, "time_seconds": 189120},
    "FC 2-3": {"meat": 39000000, "wood": 39000000, "coal": 7900000, "iron": 1900000, "steel": 0, "shards": 107, "time_seconds": 189120},
    "FC 2-4": {"meat": 39000000, "wood": 39000000, "coal": 7900000, "iron": 1900000, "steel": 0, "shards": 107, "time_seconds": 189120},
    "FC 3": {"meat": 39000000, "wood": 39000000, "coal": 7900000, "iron": 1900000, "steel": 0, "shards": 107, "time_seconds": 189120},
    "FC 3-1": {"meat": 41000000, "wood": 41000000, "coal": 8200000, "iron": 2000000, "steel": 0, "shards": 126, "time_seconds": 204960},
    "FC 3-2": {"meat": 41000000, "wood": 41000000, "coal": 8200000, "iron": 2000000, "steel": 0, "shards": 126, "time_seconds": 204960},
    "FC 3-3": {"meat": 41000000, "wood": 41000000, "coal": 8200000, "iron": 2000000, "steel": 0, "shards": 126, "time_seconds": 204960},
    "FC 3-4": {"meat": 41000000, "wood": 41000000, "coal": 8200000, "iron": 2000000, "steel": 0, "shards": 126, "time_seconds": 204960},
    "FC 4": {"meat": 41000000, "wood": 41000000, "coal": 8200000, "iron": 2000000, "steel": 0, "shards": 126, "time_seconds": 204960},
    "FC 4-1": {"meat": 42000000, "wood": 42000000, "coal": 8200000, "iron": 2100000, "steel": 0, "shards": 150, "time_seconds": 241920},
    "FC 4-2": {"meat": 42000000, "wood": 42000000, "coal": 8200000, "iron": 2100000, "steel": 0, "shards": 150, "time_seconds": 241920},
    "FC 4-3": {"meat": 42000000, "wood": 42000000, "coal": 8200000, "iron": 2100000, "steel": 0, "shards": 150, "time_seconds": 241920},
    "FC 4-4": {"meat": 42000000, "wood": 42000000, "coal": 8200000, "iron": 2100000, "steel": 0, "shards": 150, "time_seconds": 241920},
    "FC 5": {"meat": 42000000, "wood": 42000000, "coal": 8200000, "iron": 2100000, "steel": 0, "shards": 150, "time_seconds": 241920},
    "FC 5.1": {"meat": 48000000, "wood": 48000000, "coal": 9600000, "iron": 2400000, "steel": 90, "shards": 4, "time_seconds": 259200},
    "FC 5.2": {"meat": 48000000, "wood": 48000000, "coal": 9600000, "iron": 2400000, "steel": 90, "shards": 4, "time_seconds": 259200},
    "FC 5.3": {"meat": 48000000, "wood": 48000000, "coal": 9600000, "iron": 2400000, "steel": 90, "shards": 4, "time_seconds": 259200},
    "FC 5.4": {"meat": 48000000, "wood": 48000000, "coal": 9600000, "iron": 2400000, "steel": 90, "shards": 4, "time_seconds": 259200},
    "FC 6": {"meat": 48000000, "wood": 48000000, "coal": 9600000, "iron": 2400000, "steel": 45, "shards": 9, "time_seconds": 259200},
    "FC 6.1": {"meat": 54000000, "wood": 54000000, "coal": 10000000, "iron": 2700000, "steel": 108, "shards": 6, "time_seconds": 311040},
    "FC 6.2": {"meat": 54000000, "wood": 54000000, "coal": 10000000, "iron": 2700000, "steel": 108, "shards": 6, "time_seconds": 311040},
    "FC 6.3": {"meat": 54000000, "wood": 54000000, "coal": 10000000, "iron": 2700000, "steel": 108, "shards": 6, "time_seconds": 311040},
    "FC 6.4": {"meat": 54000000, "wood": 54000000, "coal": 10000000, "iron": 2700000, "steel": 108, "shards": 6, "time_seconds": 311040},
    "FC 7": {"meat": 54000000, "wood": 54000000, "coal": 10000000, "iron": 2700000, "steel": 54, "shards": 13, "time_seconds": 311040},
    "FC 7.1": {"meat": 66000000, "wood": 66000000, "coal": 13000000, "iron": 3300000, "steel": 108, "shards": 9, "time_seconds": 345600},
    "FC 7.2": {"meat": 66000000, "wood": 66000000, "coal": 13000000, "iron": 3300000, "steel": 108, "shards": 9, "time_seconds": 345600},
    "FC 7.3": {"meat": 66000000, "wood": 66000000, "coal": 13000000, "iron": 3300000, "steel": 108, "shards": 9, "time_seconds": 345600},
    "FC 7.4": {"meat": 66000000, "wood": 66000000, "coal": 13000000, "iron": 3300000, "steel": 108, "shards": 9, "time_seconds": 345600},
    "FC 8": {"meat": 66000000, "wood": 66000000, "coal": 13000000, "iron": 3300000, "steel": 108, "shards": 9, "time_seconds": 345600},
    "FC 8.1": {"meat": 72000000, "wood": 72000000, "coal": 14000000, "iron": 3600000, "steel": 126, "shards": 13, "time_seconds": 224640},
    "FC 8.2": {"meat": 72000000, "wood": 72000000, "coal": 14000000, "iron": 3600000, "steel": 126, "shards": 13, "time_seconds": 224640},
    "FC 8.3": {"meat": 72000000, "wood": 72000000, "coal": 14000000, "iron": 3600000, "steel": 126, "shards": 13, "time_seconds": 224640},
    "FC 8.4": {"meat": 72000000, "wood": 72000000, "coal": 14000000, "iron": 3600000, "steel": 126, "shards": 13, "time_seconds": 224640},
    "FC 9": {"meat": 72000000, "wood": 72000000, "coal": 14000000, "iron": 3600000, "steel": 63, "shards": 27, "time_seconds": 224640},
    "FC 9.1": {"meat": 84000000, "wood": 84000000, "coal": 16000000, "iron": 7200000, "steel": 157, "shards": 31, "time_seconds": 345600},
    "FC 9.2": {"meat": 84000000, "wood": 84000000, "coal": 16000000, "iron": 7200000, "steel": 157, "shards": 31, "time_seconds": 345600},
    "FC 9.3": {"meat": 84000000, "wood": 84000000, "coal": 16000000, "iron": 7200000, "steel": 157, "shards": 31, "time_seconds": 345600},
    "FC 9.4": {"meat": 84000000, "wood": 84000000, "coal": 16000000, "iron": 7200000, "steel": 157, "shards": 31, "time_seconds": 345600},
    "FC 10": {"meat": 84000000, "wood": 84000000, "coal": 16000000, "iron": 7200000, "steel": 78, "shards": 63, "time_seconds": 345600},
}

# ============================================================================
# BUILDING PREREQUISITES
# ============================================================================

BUILDING_PREREQUISITES = {
    "furnace": {
        2: ["Sawmill Lv. 1"],
        3: ["Shelter 1 Lv. 2"],
        4: ["Coal Mine Lv. 3"],
        5: ["Hero Hall Shelter 3 Lv. 3"],
        6: ["Iron Mine Lv. 5"],
        7: ["Hunter's Hut Lv. 6"],
        8: ["Infantry Camp Lv. 7"],
        9: ["Embassy Lv. 8", "Infirmary Lv. 1"],
        10: ["Marksman Camp Lv. 9", "Research Center"],
        11: ["Embassy Lv. 10", "Lancer Camp Lv. 10"],
        12: ["Embassy Lv. 11", "Command Centre Lv. 1"],
        13: ["Embassy Lv. 12", "Infantry Camp Lv. 12"],
        14: ["Embassy Lv. 13", "Marksman Camp Lv. 13"],
        15: ["Embassy Lv. 14", "Lancer Camp Lv. 14"],
        16: ["Embassy Lv. 15", "Research Center Lv. 15"],
        17: ["Embassy Lv. 16", "Infantry Camp Lv. 16"],
        18: ["Embassy Lv. 17", "Marksman Camp Lv. 17"],
        19: ["Embassy Lv. 18", "Lancer Camp Lv. 18"],
        20: ["Embassy Lv. 19", "Research Center Lv. 19"],
        21: ["Embassy Lv. 20", "Infantry Camp Lv. 20"],
        22: ["Embassy Lv. 21", "Marksman Camp Lv. 21"],
        23: ["Embassy Lv. 22", "Lancer Camp Lv. 22"],
        24: ["Embassy Lv. 23", "Research Center Lv. 23"],
        25: ["Embassy Lv. 24", "Infantry Camp Lv. 24"],
        26: ["Embassy Lv. 25", "Marksman Camp Lv. 25"],
        27: ["Embassy Lv. 26", "Lancer Camp Lv. 26"],
        28: ["Embassy Lv. 27", "Research Center Lv. 27"],
        29: ["Embassy Lv. 28", "Infantry Camp Lv. 28"],
        30: ["Embassy Lv. 29", "Marksman Camp Lv. 29"],
    },
    "infantry_camp": {
        1: ["Furnace Lv. 7"],
        2: ["Furnace Lv. 7"],
        3: ["Furnace Lv. 7"],
        4: ["Furnace Lv. 7"],
        5: ["Furnace Lv. 7"],
        6: ["Furnace Lv. 7"],
        7: ["Furnace Lv. 7"],
        8: ["Furnace Lv. 8"],
        9: ["Furnace Lv. 9"],
        10: ["Furnace Lv. 10"],
        11: ["Furnace Lv. 11"],
        12: ["Furnace Lv. 12"],
        13: ["Furnace Lv. 13"],
        14: ["Furnace Lv. 14"],
        15: ["Furnace Lv. 15"],
        16: ["Furnace Lv. 16"],
        17: ["Furnace Lv. 17"],
        18: ["Furnace Lv. 18"],
        19: ["Furnace Lv. 19"],
        20: ["Furnace Lv. 20"],
        21: ["Furnace Lv. 21"],
        22: ["Furnace Lv. 22"],
        23: ["Furnace Lv. 23"],
        24: ["Furnace Lv. 24"],
        25: ["Furnace Lv. 25"],
        26: ["Furnace Lv. 26"],
        27: ["Furnace Lv. 27"],
        28: ["Furnace Lv. 28"],
        29: ["Furnace Lv. 29"],
        30: ["Furnace Lv. 30"],
    },
    "research_center": {
        1: ["Furnace Lv. 9"],
        2: ["Furnace Lv. 9"],
        3: ["Furnace Lv. 9"],
        4: ["Furnace Lv. 9"],
        5: ["Furnace Lv. 9"],
        6: ["Furnace Lv. 9"],
        7: ["Furnace Lv. 9"],
        8: ["Furnace Lv. 9"],
        9: ["Furnace Lv. 9"],
        10: ["Furnace Lv. 10"],
        11: ["Furnace Lv. 11"],
        12: ["Furnace Lv. 12"],
        13: ["Furnace Lv. 13"],
        14: ["Furnace Lv. 14"],
        15: ["Furnace Lv. 15"],
        16: ["Furnace Lv. 16"],
        17: ["Furnace Lv. 17"],
        18: ["Furnace Lv. 18"],
        19: ["Furnace Lv. 19"],
        20: ["Furnace Lv. 20"],
        21: ["Furnace Lv. 21"],
        22: ["Furnace Lv. 22"],
        23: ["Furnace Lv. 23"],
        24: ["Furnace Lv. 24"],
        25: ["Furnace Lv. 25"],
        26: ["Furnace Lv. 26"],
        27: ["Furnace Lv. 27"],
        28: ["Furnace Lv. 28"],
        29: ["Furnace Lv. 29"],
        30: ["Furnace Lv. 30"],
    },
    # TODO: Add prerequisites for other buildings
}

WAR_ACADEMY_PREREQUISITES = {
    "FC 1": ["Furnace FC 1"],
    "FC 1-1": ["Furnace FC 2"],
    "FC 1-2": ["Furnace FC 2"],
    "FC 1-3": ["Furnace FC 2"],
    "FC 1-4": ["Furnace FC 2"],
    "FC 2": ["Furnace FC 2"],
    "FC 2-1": ["Furnace FC 3"],
    "FC 2-2": ["Furnace FC 3"],
    "FC 2-3": ["Furnace FC 3"],
    "FC 2-4": ["Furnace FC 3"],
    "FC 3": ["Furnace FC 3"],
    "FC 3-1": ["Furnace FC 4"],
    "FC 3-2": ["Furnace FC 4"],
    "FC 3-3": ["Furnace FC 4"],
    "FC 3-4": ["Furnace FC 4"],
    "FC 4": ["Furnace FC 4"],
    "FC 4-1": ["Furnace FC 5"],
    "FC 4-2": ["Furnace FC 5"],
    "FC 4-3": ["Furnace FC 5"],
    "FC 4-4": ["Furnace FC 5"],
    "FC 5": ["Furnace FC 5"],
    "FC 5.1": ["Furnace FC 6"],
    "FC 5.2": ["Furnace FC 6"],
    "FC 5.3": ["Furnace FC 6"],
    "FC 5.4": ["Furnace FC 6"],
    "FC 6": ["Furnace FC 6"],
    "FC 6.1": ["Furnace FC 7"],
    "FC 6.2": ["Furnace FC 7"],
    "FC 6.3": ["Furnace FC 7"],
    "FC 6.4": ["Furnace FC 7"],
    "FC 7": ["Furnace FC 7"],
    "FC 7.1": ["Furnace FC 8"],
    "FC 7.2": ["Furnace FC 8"],
    "FC 7.3": ["Furnace FC 8"],
    "FC 7.4": ["Furnace FC 8"],
    "FC 8": ["Furnace FC 8"],
    "FC 8.1": ["Furnace FC 9"],
    "FC 8.2": ["Furnace FC 9"],
    "FC 8.3": ["Furnace FC 9"],
    "FC 8.4": ["Furnace FC 9"],
    "FC 9": ["Furnace FC 9"],
    "FC 9.1": ["Furnace FC 10"],
    "FC 9.2": ["Furnace FC 10"],
    "FC 9.3": ["Furnace FC 10"],
    "FC 9.4": ["Furnace FC 10"],
    "FC 10": ["Furnace FC 10"],
}

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def calculate_building_cost(building: str, from_level: int, to_level: int) -> dict:
    """
    Calculate total resources needed to upgrade a building from one level to another.
    
    Args:
        building: Building name (e.g., "furnace", "infantry_camp", "research_center")
        from_level: Current building level
        to_level: Target building level
    
    Returns:
        Dictionary with total resources needed
    """
    if building not in BUILDING_COSTS:
        return None
    
    if from_level >= to_level:
        return None
    
    total = {"meat": 0, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "time_seconds": 0}
    
    for level in range(from_level + 1, to_level + 1):
        if level in BUILDING_COSTS[building]:
            costs = BUILDING_COSTS[building][level]
            for resource in total:
                total[resource] += costs[resource]
    
    return total


def calculate_war_academy_cost(from_fc: str, to_fc: str) -> dict:
    """
    Calculate total resources needed to upgrade War Academy from one FC level to another.
    
    Args:
        from_fc: Current FC level (e.g., "FC 1", "FC 5.1")
        to_fc: Target FC level
    
    Returns:
        Dictionary with total resources needed (includes shards)
    """
    fc_levels = list(WAR_ACADEMY_COSTS.keys())
    
    try:
        from_index = fc_levels.index(from_fc)
        to_index = fc_levels.index(to_fc)
    except ValueError:
        return None
    
    if from_index >= to_index:
        return None
    
    total = {"meat": 0, "wood": 0, "coal": 0, "iron": 0, "steel": 0, "shards": 0, "time_seconds": 0}
    
    for i in range(from_index + 1, to_index + 1):
        fc_level = fc_levels[i]
        costs = WAR_ACADEMY_COSTS[fc_level]
        for resource in total:
            total[resource] += costs[resource]
    
    return total


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_time(seconds: int) -> str:
    """Convert seconds to readable time format (days, hours, minutes, seconds)."""
    if seconds == 0:
        return "0s"
    
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def format_number(num: int) -> str:
    """Format large numbers with K, M, B suffixes."""
    if num >= 1000000000:
        return f"{num / 1000000000:.1f}B"
    elif num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    else:
        return str(num)
