# 👥 Flames CC Squad Management

## Overview

This system manages player identities across different scorecard formats to ensure consistent data aggregation.

## Problem

Different scorecards use different name formats:
- **"Bilal"** vs **"M.Bilal"** vs **"Muhammad Bilal"**
- **"Leo"** vs **"Leonardo"**
- **"A.Rehman"** vs **"Abdul Rehman"** vs **"Rehman"**

Without normalization, these would be counted as different players in analytics!

## Solution

### 1. Squad Database (`flames_squad.json`)

Central database containing:
- **Unique Player IDs** (P001, P002, etc.)
- **Full official names**
- **All name variations** (common_names)
- **Player roles** (Batsman, Bowler, All-rounder, Wicketkeeper)
- **Playing styles** (batting/bowling)

### 2. Name Mapper (`player_name_mapper.py`)

Python module that:
- ✅ Normalizes raw scorecard names
- ✅ Maps variations to unique player IDs
- ✅ Extracts player names from dismissal info
- ✅ Identifies unknown players
- ✅ Allows adding new players

## Current Squad

| ID | Full Name | Common Names | Role |
|----|-----------|--------------|------|
| P001 | Abdul Majid | Majid, Abdul Majid, A.Majid | Batsman (Captain) |
| P002 | Bilal | Bilal, M.Bilal, Muhammad Bilal | All-rounder |
| P003 | Hassan | Hassan, M.Hassan | Batsman |
| P004 | Sufi | Sufi, M.Sufi | All-rounder |
| P005 | Abdal | Abdal, Abdul, Abdal Sheikh | Batsman |
| P006 | Leo | Leo, Leonardo | Batsman |
| P007 | Danish | Danish, Adeel Danish | Batsman |
| P008 | Sameer | Sameer, M.Sameer | Bowler |
| P009 | Nehal | Nehal, M.Nehal | Bowler |
| P010 | A.Rehman | A.Rehman, Rehman, Abdul Rehman | Bowler |
| P011 | Zain | Zain, Zain Hassan, M.Zain | Bowler |

## Usage

### In Data Extraction

```python
from player_name_mapper import PlayerNameMapper

# Initialize mapper
mapper = PlayerNameMapper()

# Normalize a player name
raw_name = "s\nSR\nHassan\nc Bilal b Saif"
result = mapper.normalize_player_name(raw_name)

print(result)
# {
#     'player_id': 'P003',
#     'full_name': 'Hassan',
#     'raw_name': 's\nSR\nHassan\nc Bilal b Saif',
#     'normalized_name': 'Hassan'
# }
```

### Finding Unknown Players

```python
# Scan extracted data for unknown players
unknown = mapper.get_all_unknown_players(extracted_data)
print(f"Unknown players: {unknown}")
```

### Adding New Players

```python
# Add a new player when discovered
mapper.add_new_player(
    full_name="Azhar Khan",
    common_names=["Azhar", "A.Khan", "Azhar Khan"],
    role="Batsman",
    batting_style="Right-hand bat",
    bowling_style=None
)
```

## Benefits

1. **Consistent Analytics**: Same player counted correctly across all matches
2. **Automatic Aggregation**: Stats automatically roll up to unique player IDs
3. **Cross-Format Support**: Works with Format 1, 2, 3 scorecards
4. **Easy Updates**: Add new players or name variations anytime
5. **Data Quality**: Identifies typos and unknown names

## Workflow

### When Processing New Scorecards:

1. **Extract raw data** from PDF
2. **Normalize player names** using mapper
3. **Check for unknowns** 
4. **Add new players** if needed
5. **Store with player IDs** for aggregation

### Example Output:

**Before Normalization:**
```json
{
  "name": "s\nSR\nHassan\nc Bilal b Saif",
  "runs": 26,
  "balls": 21
}
```

**After Normalization:**
```json
{
  "player_id": "P003",
  "full_name": "Hassan",
  "runs": 26,
  "balls": 21,
  "raw_name": "s\nSR\nHassan\nc Bilal b Saif"
}
```

## Maintenance

### Adding Name Variations

Edit `flames_squad.json`:

```json
{
  "player_id": "P002",
  "full_name": "Bilal",
  "common_names": [
    "Bilal",
    "M.Bilal",
    "Muhammad Bilal",
    "Bilal Ahmed"  // Add new variation
  ]
}
```

Update `name_mapping`:

```json
"name_mapping": {
  "Bilal Ahmed": "P002"  // Add mapping
}
```

### Handling Opponent Players

The same system works for opponent players. When extracting opponent data:
- Unknown opponents get placeholder IDs (OPP_001, OPP_002, etc.)
- Can be optionally tracked if needed for head-to-head stats

## Future Enhancements

- [ ] Auto-detect similar names (fuzzy matching)
- [ ] Jersey number tracking
- [ ] Historical stats migration
- [ ] Player photos/avatars
- [ ] Career statistics per player

---

*Squad Management System v1.0*  
*Last Updated: October 20, 2025*

