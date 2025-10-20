#!/usr/bin/env python3
"""
Comprehensive CricHeroes PDF Extractor
Handles both ALLSTAR and standard CricHeroes formats
"""

import os
import PyPDF2
import re
import json
from collections import Counter

def extract_cricheroes_pdf(pdf_path):
    """Extract comprehensive data from CricHeroes PDF"""
    
    print(f"\nExtracting: {os.path.basename(pdf_path)}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text() + "\n"
            
            # Parse the text
            match_data = parse_cricheroes_text(full_text, os.path.basename(pdf_path))
            return match_data
            
    except Exception as e:
        print(f"  Error: {e}")
        return None

def parse_cricheroes_text(text, filename):
    """Parse CricHeroes text comprehensively"""
    
    match_data = {
        "filename": filename,
        "match_info": {
            "tournament": "",
            "team1": "",
            "team2": "",
            "venue": "",
            "date": "",
            "toss": "",
            "result": ""
        },
        "first_innings": {
            "batting_team": "",
            "score": "",
            "overs": "",
            "extras": {},
            "batting": [],
            "bowling": [],
            "fall_of_wickets": []
        },
        "second_innings": {
            "batting_team": "",
            "score": "",
            "overs": "",
            "extras": {},
            "batting": [],
            "bowling": [],
            "fall_of_wickets": []
        },
        "fielding_analysis": {
            "catches_by_fielder": {},
            "wickets_by_bowler": {},
            "dismissal_types": {}
        }
    }
    
    lines = text.split('\n')
    
    # Step 1: Extract match header
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Tournament
        if 'ALLSTAR' in line or 'CHAMPIONSHIP' in line or 'LEAGUE' in line:
            match_data["match_info"]["tournament"] = line
        
        # Teams (format: "Team1 vs Team2" or "Team1 vs  Team2")
        if ' vs' in line and i < 20:  # Check in first 20 lines
            # Extract teams
            parts = line.split(' vs')
            if len(parts) >= 2:
                team1 = parts[0].strip()
                team2 = parts[1].strip()
                
                # Clean team names
                if team1 and len(team1) > 2 and len(team1) < 100:
                    match_data["match_info"]["team1"] = team1
                if team2 and len(team2) > 2 and len(team2) < 100:
                    match_data["match_info"]["team2"] = team2
        
        # Venue and Date
        if 'Played at' in line or 'Ground' in line:
            match_data["match_info"]["venue"] = line.replace('Played at', '').strip()
        
        if 'Date' in line and ('20' in line or 'UTC' in line):
            match_data["match_info"]["date"] = line.replace('Date', '').strip()
        
        # Toss
        if 'Toss:' in line or 'opt to' in line:
            match_data["match_info"]["toss"] = line.replace('Toss:', '').strip()
        
        # Result
        if 'Result' in line and ('won' in line or 'Match tied' in line or 'No result' in line):
            match_data["match_info"]["result"] = line.replace('Result', '').strip()
    
    # Step 2: Extract innings data
    innings_sections = extract_innings_sections(text)
    
    if len(innings_sections) >= 1:
        match_data["first_innings"] = parse_innings_data(innings_sections[0], "first")
    
    if len(innings_sections) >= 2:
        match_data["second_innings"] = parse_innings_data(innings_sections[1], "second")
    
    # Step 3: Extract fielding analysis
    match_data["fielding_analysis"] = analyze_fielding(match_data)
    
    return match_data

def extract_innings_sections(text):
    """Extract innings sections from text"""
    
    innings_sections = []
    
    # Split by innings markers
    innings_markers = [
        '1ST INNINGS',
        '2ND INNINGS',
        '(1st Innings)',
        '(2nd Innings)'
    ]
    
    lines = text.split('\n')
    current_section = []
    in_innings = False
    
    for line in lines:
        line_upper = line.upper()
        
        # Check if this line marks start of an innings
        if any(marker in line_upper for marker in innings_markers):
            # Save previous section if exists
            if current_section:
                innings_sections.append('\n'.join(current_section))
            
            current_section = [line]
            in_innings = True
        elif in_innings:
            current_section.append(line)
            
            # Check if we've reached the end of this innings section
            if 'Fall of Wickets' in line and len(current_section) > 20:
                innings_sections.append('\n'.join(current_section))
                current_section = []
                in_innings = False
    
    # Add last section if exists
    if current_section:
        innings_sections.append('\n'.join(current_section))
    
    return innings_sections

def parse_innings_data(innings_text, innings_type):
    """Parse individual innings data"""
    
    innings_data = {
        "batting_team": "",
        "score": "",
        "overs": "",
        "extras": {},
        "batting": [],
        "bowling": [],
        "fall_of_wickets": []
    }
    
    lines = innings_text.split('\n')
    
    # Extract batting team and score from header
    for line in lines[:5]:
        # Format: "Team 127/9 (18.0 Ov)" or "Team 128/5 (18.0 Ov) (1st Innings)"
        score_match = re.search(r'(.+?)\s+(\d+)/(\d+)\s+\((\d+\.?\d*)\s+Ov\)', line)
        if score_match:
            team = score_match.group(1).strip()
            runs = score_match.group(2)
            wickets = score_match.group(3)
            overs = score_match.group(4)
            
            # Clean team name
            team = re.sub(r'\d+(ST|ND|RD|TH) INNINGS', '', team, flags=re.IGNORECASE).strip()
            team = re.sub(r'\(.*?\)', '', team).strip()
            
            innings_data["batting_team"] = team
            innings_data["score"] = f"{runs}/{wickets}"
            innings_data["overs"] = overs
    
    # Extract extras
    for line in lines:
        extras_match = re.search(r'Extras:\s*\(([^)]+)\)\s*(\d+)', line)
        if extras_match:
            breakdown = extras_match.group(1)
            total = extras_match.group(2)
            
            innings_data["extras"] = {"total": total}
            
            # Parse breakdown (wd 13, nb 1, lb 1)
            parts = breakdown.split(',')
            for part in parts:
                part = part.strip()
                if ' ' in part:
                    extra_type, value = part.split()
                    innings_data["extras"][extra_type] = value
    
    # Extract batting data
    batting_started = False
    for line in lines:
        line = line.strip()
        
        # Check for batting section start
        if 'Batsman' in line and 'Status' in line:
            batting_started = True
            continue
        
        # Check for batting section end
        if batting_started and ('Bowler' in line or 'To Bat' in line or 'Fall of Wickets' in line):
            batting_started = False
            continue
        
        if batting_started:
            batting_record = parse_batting_line_cricheroes(line)
            if batting_record:
                innings_data["batting"].append(batting_record)
    
    # Extract bowling data
    bowling_started = False
    for line in lines:
        line = line.strip()
        
        # Check for bowling section start
        if 'Bowler' in line and ('Eco' in line or 'WD' in line):
            bowling_started = True
            continue
        
        # Check for bowling section end
        if bowling_started and ('Fall of Wickets' in line or 'To Bat' in line):
            bowling_started = False
            continue
        
        if bowling_started:
            bowling_record = parse_bowling_line_cricheroes(line)
            if bowling_record:
                innings_data["bowling"].append(bowling_record)
    
    # Extract fall of wickets
    fall_started = False
    for line in lines:
        if 'Fall of Wickets' in line:
            fall_started = True
            continue
        
        if fall_started and line.strip():
            # Parse fall of wickets line
            # Format: "22-1 (Muhammad Bilal Taak, 1.5 ov), 68-1 (Abdul Majid, 8 ov)"
            fall_matches = re.findall(r'(\d+)-(\d+)\s*\(([^,]+),\s*([^)]+)\)', line)
            for score, wicket, batsman, over in fall_matches:
                innings_data["fall_of_wickets"].append({
                    "score": score,
                    "wicket": wicket,
                    "batsman": batsman.strip(),
                    "over": over.strip()
                })
    
    return innings_data

def parse_batting_line_cricheroes(line):
    """Parse CricHeroes batting line"""
    
    # Format: "1 Abdul Majid (c) (RHB) b Imran Farooq 25 23 36 0 1 108.70"
    # Or: "1Abdul Majid (c) (RHB) b Imran Farooq 2523360 1 108.70"
    
    # Try to extract batting data
    # Pattern: Number, Name, Dismissal, Stats (R B M 4s 6s SR)
    
    # Remove leading number
    line = re.sub(r'^\d+\s*', '', line)
    
    if not line or len(line) < 10:
        return None
    
    # Try to find strike rate (last number with decimal or large number)
    sr_match = re.search(r'(\d+\.?\d*)$', line)
    if not sr_match:
        return None
    
    strike_rate = sr_match.group(1)
    remaining = line[:line.rfind(strike_rate)].strip()
    
    # Extract stats backwards (6s, 4s, M, B, R)
    stats = []
    temp = remaining
    
    for i in range(5):  # Extract 5 numbers (6s, 4s, M, B, R)
        match = re.search(r'(\d+)$', temp)
        if match:
            stats.insert(0, match.group(1))
            temp = temp[:temp.rfind(match.group(1))].strip()
        else:
            break
    
    if len(stats) < 5:
        return None
    
    runs, balls, minutes, fours, sixes = stats
    
    # Extract name and dismissal from remaining
    # Try different dismissal patterns
    dismissal_patterns = [
        (r'(.+?)\s+(c[^b]*b\s+\w+)', 'caught'),
        (r'(.+?)\s+(c&b\s+\w+)', 'caught_and_bowled'),
        (r'(.+?)\s+(b\s+\w+)', 'bowled'),
        (r'(.+?)\s+(lbw\s+b\s+\w+)', 'lbw'),
        (r'(.+?)\s+(run out[^)]*)', 'run_out'),
        (r'(.+?)\s+(stumped[^)]*)', 'stumped'),
        (r'(.+?)\s+(retired hurt)', 'retired_hurt'),
        (r'(.+?)\s+(not out)', 'not_out')
    ]
    
    player = ""
    dismissal = ""
    dismissal_type = ""
    fielder = ""
    bowler = ""
    
    for pattern, dis_type in dismissal_patterns:
        match = re.search(pattern, temp, re.IGNORECASE)
        if match:
            player = match.group(1).strip()
            dismissal = match.group(2).strip()
            dismissal_type = dis_type
            
            # Extract fielder and bowler from dismissal
            if 'c' in dismissal and 'b' in dismissal:
                fielder_match = re.search(r'c\s*(?:&|and)?\s*(\w+)', dismissal)
                bowler_match = re.search(r'b\s+(\w+)', dismissal)
                if fielder_match:
                    fielder = fielder_match.group(1)
                if bowler_match:
                    bowler = bowler_match.group(1)
            elif 'b ' in dismissal:
                bowler_match = re.search(r'b\s+(\w+)', dismissal)
                if bowler_match:
                    bowler = bowler_match.group(1)
            
            break
    
    if not player:
        # Extract first part as player name
        words = temp.split()
        if words:
            player = ' '.join(words[:2])  # Take first 2 words as name
            dismissal = "unknown"
            dismissal_type = "unknown"
    
    # Clean player name (remove tags like (c), (wk), (RHB), etc.)
    player = re.sub(r'\([^)]*\)', '', player).strip()
    
    return {
        "player": player,
        "dismissal": dismissal,
        "dismissal_type": dismissal_type,
        "fielder": fielder,
        "bowler": bowler,
        "runs": runs,
        "balls": balls,
        "minutes": minutes,
        "fours": fours,
        "sixes": sixes,
        "strike_rate": strike_rate
    }

def parse_bowling_line_cricheroes(line):
    """Parse CricHeroes bowling line"""
    
    # Format: "1 Syed Numair Haseeb (RF) 4 0 20 1 14 1 1 1 0 5.00"
    # Or: "1Syed Numair Haseeb (RF) 4020114111 0 5.00"
    
    # Remove leading number
    line = re.sub(r'^\d+\s*', '', line)
    
    if not line or len(line) < 10:
        return None
    
    # Extract economy (last number with decimal)
    eco_match = re.search(r'(\d+\.?\d*)$', line)
    if not eco_match:
        return None
    
    economy = eco_match.group(1)
    remaining = line[:line.rfind(economy)].strip()
    
    # Extract stats backwards (NB, WD, 6s, 4s, 0s, W, R, M, O)
    stats = []
    temp = remaining
    
    for i in range(8):  # Extract 8 numbers
        match = re.search(r'(\d+)$', temp)
        if match:
            stats.insert(0, match.group(1))
            temp = temp[:temp.rfind(match.group(1))].strip()
        else:
            break
    
    if len(stats) < 4:  # At least need O, M, R, W
        return None
    
    # Assign stats
    overs = stats[0] if len(stats) > 0 else "0"
    maidens = stats[1] if len(stats) > 1 else "0"
    runs = stats[2] if len(stats) > 2 else "0"
    wickets = stats[3] if len(stats) > 3 else "0"
    zeros = stats[4] if len(stats) > 4 else "0"
    fours = stats[5] if len(stats) > 5 else "0"
    sixes = stats[6] if len(stats) > 6 else "0"
    wides = stats[7] if len(stats) > 7 else "0"
    no_balls = stats[8] if len(stats) > 8 else "0"
    
    # Extract bowler name from remaining
    bowler = temp.strip()
    
    # Clean bowler name (remove tags like (RF), (RM), etc.)
    bowler = re.sub(r'\([^)]*\)', '', bowler).strip()
    
    return {
        "bowler": bowler,
        "overs": overs,
        "maidens": maidens,
        "runs": runs,
        "wickets": wickets,
        "economy": economy,
        "zeros": zeros,
        "fours": fours,
        "sixes": sixes,
        "wides": wides,
        "no_balls": no_balls
    }

def analyze_fielding(match_data):
    """Analyze fielding from match data"""
    
    fielding_analysis = {
        "catches_by_fielder": Counter(),
        "wickets_by_bowler": Counter(),
        "dismissal_types": Counter()
    }
    
    # Analyze both innings
    for innings in [match_data["first_innings"], match_data["second_innings"]]:
        for batting_record in innings["batting"]:
            dismissal_type = batting_record.get("dismissal_type", "")
            fielder = batting_record.get("fielder", "")
            bowler = batting_record.get("bowler", "")
            
            # Count dismissal types
            if dismissal_type:
                fielding_analysis["dismissal_types"][dismissal_type] += 1
            
            # Count catches
            if fielder:
                fielding_analysis["catches_by_fielder"][fielder] += 1
            
            # Count wickets by bowler (exclude not out, retired hurt)
            if bowler and dismissal_type not in ['not_out', 'retired_hurt']:
                fielding_analysis["wickets_by_bowler"][bowler] += 1
    
    # Convert Counter to dict
    fielding_analysis["catches_by_fielder"] = dict(fielding_analysis["catches_by_fielder"])
    fielding_analysis["wickets_by_bowler"] = dict(fielding_analysis["wickets_by_bowler"])
    fielding_analysis["dismissal_types"] = dict(fielding_analysis["dismissal_types"])
    
    return fielding_analysis

def test_extractor():
    """Test the extractor on sample files"""
    
    print("=== TESTING CRICHEROES EXTRACTOR ===\n")
    
    # Test on both formats
    test_files = [
        "Flames/Scorecards/13 - 26-Sep-21 -  CLASSIC XI KARACHI VS Flames.pdf",
        "Flames/Scorecards/Scorecard_10640768.pdf"
    ]
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"File not found: {test_file}")
            continue
        
        print(f"\n{'='*80}")
        print(f"Testing: {os.path.basename(test_file)}")
        print('='*80)
        
        match_data = extract_cricheroes_pdf(test_file)
        
        if match_data:
            # Display summary
            print("\nMATCH INFO:")
            for key, value in match_data["match_info"].items():
                if value:
                    print(f"  {key}: {value}")
            
            print(f"\nFIRST INNINGS ({match_data['first_innings']['batting_team']}):")
            print(f"  Score: {match_data['first_innings']['score']} in {match_data['first_innings']['overs']} overs")
            print(f"  Batting records: {len(match_data['first_innings']['batting'])}")
            print(f"  Bowling records: {len(match_data['first_innings']['bowling'])}")
            
            print(f"\nSECOND INNINGS ({match_data['second_innings']['batting_team']}):")
            print(f"  Score: {match_data['second_innings']['score']} in {match_data['second_innings']['overs']} overs")
            print(f"  Batting records: {len(match_data['second_innings']['batting'])}")
            print(f"  Bowling records: {len(match_data['second_innings']['bowling'])}")
            
            print(f"\nFIELDING ANALYSIS:")
            print(f"  Catches: {len(match_data['fielding_analysis']['catches_by_fielder'])} fielders")
            print(f"  Wickets: {len(match_data['fielding_analysis']['wickets_by_bowler'])} bowlers")
            print(f"  Dismissal types: {match_data['fielding_analysis']['dismissal_types']}")
            
            # Save to file
            output_file = f"test_{os.path.basename(test_file).replace('.pdf', '.json')}"
            with open(output_file, 'w') as f:
                json.dump(match_data, f, indent=2)
            print(f"\nSaved to: {output_file}")
        else:
            print("Extraction failed!")

if __name__ == "__main__":
    test_extractor()
