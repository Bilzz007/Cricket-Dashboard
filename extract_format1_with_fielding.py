import fitz
import re
import json

def extract_format1_with_fielding(pdf_path):
    """Extract ALL data including fielding statistics from Format 1 PDF"""
    print(f"=== EXTRACTING COMPLETE DATA WITH FIELDING ===")
    print(f"File: {pdf_path}\n")
    
    doc = fitz.open(pdf_path)
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())
    doc.close()
    
    full_text = '\n'.join(pages_text)
    
    match_data = {
        'filename': pdf_path.split('/')[-1],
        'format_type': 'FULL_SCORECARD',
        'match_info': {},
        'batting': {
            'opponent': [],
            'flames': []
        },
        'bowling': {
            'flames': [],
            'opponent': []
        },
        'fielding': {
            'flames': {},  # Will store: {player_name: {catches: X, stumpings: Y, run_outs: Z}}
            'opponent': {}
        }
    }
    
    # Extract basic match info
    print("MATCH INFORMATION:")
    print("=" * 70)
    
    lines = pages_text[0].split('\n')
    if lines[0].strip():
        match_data['match_info']['series'] = lines[0].strip()
        print(f"Series: {lines[0].strip()}")
    
    # Opponent from filename
    filename = match_data['filename']
    if ' - ' in filename:
        parts = filename.split(' - ')
        if len(parts) >= 3:
            opponent = parts[2].replace('.pdf', '').replace(' VS Flames', '').replace(' VS FLames', '').replace(' Vs FLames', '').strip()
            match_data['match_info']['opponent'] = opponent
            print(f"Opponent: {opponent}")
        if len(parts) >= 2:
            date = parts[1].strip()
            match_data['match_info']['date'] = date
            print(f"Date: {date}")
    
    # Venue - extract just the ground name
    for line in lines:
        if 'Ground' in line and len(line) < 50:
            venue = line.strip()
            # Clean up venue if it has date attached
            venue = re.sub(r'\s+\d{2}-\w{3}-\d{4}', '', venue)
            if venue and venue != match_data['match_info']['series']:
                match_data['match_info']['venue'] = venue
                print(f"Venue: {venue}")
                break
    
    # Scores and Extras
    scores = re.findall(r'(\w+):(\d+)/(\d+)', full_text)
    print(f"\nMATCH SCORES:")
    print("=" * 70)
    for team, runs, wickets in scores:
        if 'Flames' in team or 'flames' in team:
            match_data['match_info']['flames_score'] = int(runs)
            match_data['match_info']['flames_wickets'] = int(wickets)
            print(f"Flames: {runs}/{wickets}")
            
            # Extract Flames extras
            extras_match = re.search(r'Flames:' + runs + r'/\d+.*?EXTRAS:\s*(\d+)\s*\(B:(\d+)\s+LB:(\d+)\s+NB:(\d+)\s+WD:(\d+)\)', full_text)
            if extras_match:
                match_data['match_info']['flames_extras'] = {
                    'total': int(extras_match.group(1)),
                    'byes': int(extras_match.group(2)),
                    'leg_byes': int(extras_match.group(3)),
                    'no_balls': int(extras_match.group(4)),
                    'wides': int(extras_match.group(5))
                }
                print(f"  Extras: {extras_match.group(1)} (B:{extras_match.group(2)}, LB:{extras_match.group(3)}, NB:{extras_match.group(4)}, WD:{extras_match.group(5)})")
        else:
            match_data['match_info']['opponent_score'] = int(runs)
            match_data['match_info']['opponent_wickets'] = int(wickets)
            print(f"{match_data['match_info']['opponent']}: {runs}/{wickets}")
            
            # Extract opponent extras
            extras_match = re.search(r'(\w+):' + runs + r'/\d+.*?EXTRAS:\s*(\d+)\s*\(B:(\d+)\s+LB:(\d+)\s+NB:(\d+)\s+WD:(\d+)\)', full_text)
            if extras_match:
                match_data['match_info']['opponent_extras'] = {
                    'total': int(extras_match.group(2)),
                    'byes': int(extras_match.group(3)),
                    'leg_byes': int(extras_match.group(4)),
                    'no_balls': int(extras_match.group(5)),
                    'wides': int(extras_match.group(6))
                }
                print(f"  Extras: {extras_match.group(2)} (B:{extras_match.group(3)}, LB:{extras_match.group(4)}, NB:{extras_match.group(5)}, WD:{extras_match.group(6)})")
    
    # Result
    result = re.search(r'Result:\s*(.+)', full_text)
    if result:
        result_text = result.group(1).strip()
        match_data['match_info']['result_text'] = result_text
        if 'Flames won' in result_text or 'flames won' in result_text:
            match_data['match_info']['result'] = 'Win'
        else:
            match_data['match_info']['result'] = 'Loss'
        print(f"\nResult: {result_text}")
        print(f"Outcome: {match_data['match_info']['result']}")
    
    # Helper function to extract fielder from dismissal
    def extract_fielding_info(dismissal_text):
        """Extract fielder name and dismissal type from dismissal text"""
        fielder = None
        dismissal_type = None
        
        # Pattern: "c FielderName b BowlerName"
        catch_match = re.search(r'c\s+([A-Za-z.]+)', dismissal_text)
        if catch_match:
            fielder = catch_match.group(1).strip()
            dismissal_type = 'catch'
        
        # Pattern: "stumped FielderName b BowlerName" or "stumped b BowlerName"
        stumping_match = re.search(r'stumped\s+(?:([A-Za-z.]+)\s+)?b', dismissal_text)
        if stumping_match and stumping_match.group(1):
            fielder = stumping_match.group(1).strip()
            dismissal_type = 'stumping'
        
        # Pattern: "run out (FielderName)"
        runout_match = re.search(r'run out\s*\(([A-Za-z.]+)\)', dismissal_text)
        if runout_match:
            fielder = runout_match.group(1).strip()
            dismissal_type = 'run_out'
        
        return fielder, dismissal_type
    
    # Helper function to update fielding stats
    def update_fielding_stats(fielding_dict, fielder, dismissal_type):
        """Update fielding statistics for a player"""
        if fielder:
            if fielder not in fielding_dict:
                fielding_dict[fielder] = {
                    'catches': 0,
                    'stumpings': 0,
                    'run_outs': 0
                }
            
            if dismissal_type == 'catch':
                fielding_dict[fielder]['catches'] += 1
            elif dismissal_type == 'stumping':
                fielding_dict[fielder]['stumpings'] += 1
            elif dismissal_type == 'run_out':
                fielding_dict[fielder]['run_outs'] += 1
    
    # Extract batting stats with fielding analysis
    batting_pattern = r'([A-Za-z][A-Za-z.\s]+?(?:c |b |stumped |not out|run out)[^\n]+?)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n([\d.]+)'
    
    print(f"\n{match_data['match_info']['opponent'].upper()} BATTING:")
    print("=" * 70)
    print(f"{'Player':<40} {'R':<5} {'B':<5} {'4s':<5} {'6s':<5} {'SR':<8}")
    print("-" * 70)
    
    opponent_batting_matches = re.findall(batting_pattern, pages_text[0])
    
    for match in opponent_batting_matches:
        name_dismissal = match[0].strip()
        runs = int(match[1])
        balls = int(match[2])
        dots = int(match[3])
        fours = int(match[4])
        sixes = int(match[5])
        sr = float(match[6])
        
        # Extract fielding info (Flames players who took catches/stumpings)
        fielder, dismissal_type = extract_fielding_info(name_dismissal)
        if fielder:
            update_fielding_stats(match_data['fielding']['flames'], fielder, dismissal_type)
        
        batsman = {
            'name': name_dismissal,
            'runs': runs,
            'balls': balls,
            'fours': fours,
            'sixes': sixes,
            'strike_rate': sr
        }
        match_data['batting']['opponent'].append(batsman)
        print(f"{name_dismissal:<40} {runs:<5} {balls:<5} {fours:<5} {sixes:<5} {sr:<8.1f}")
    
    # Flames batting
    print(f"\nFLAMES BATTING:")
    print("=" * 70)
    print(f"{'Player':<40} {'R':<5} {'B':<5} {'4s':<5} {'6s':<5} {'SR':<8}")
    print("-" * 70)
    
    if len(pages_text) >= 3:
        flames_batting_matches = re.findall(batting_pattern, pages_text[2])
        
        for match in flames_batting_matches:
            name_dismissal = match[0].strip()
            runs = int(match[1])
            balls = int(match[2])
            dots = int(match[3])
            fours = int(match[4])
            sixes = int(match[5])
            sr = float(match[6])
            
            # Extract fielding info (Opponent players who took catches/stumpings)
            fielder, dismissal_type = extract_fielding_info(name_dismissal)
            if fielder:
                update_fielding_stats(match_data['fielding']['opponent'], fielder, dismissal_type)
            
            batsman = {
                'name': name_dismissal,
                'runs': runs,
                'balls': balls,
                'fours': fours,
                'sixes': sixes,
                'strike_rate': sr
            }
            match_data['batting']['flames'].append(batsman)
            print(f"{name_dismissal:<40} {runs:<5} {balls:<5} {fours:<5} {sixes:<5} {sr:<8.1f}")
    
    # Extract bowling stats (clean version - only actual bowlers)
    print(f"\nFLAMES BOWLING:")
    print("=" * 70)
    print(f"{'Bowler':<20} {'O':<6} {'R':<6} {'W':<6} {'M':<6} {'Econ':<8}")
    print("-" * 70)
    
    # Find bowling section in page 1
    bowling_start = pages_text[0].find('Bowler\nO\nR\nW\nM\nECO')
    if bowling_start != -1:
        # Find the end of bowling section (before "No\nRuns\nOver")
        bowling_end = pages_text[0].find('No\nRuns\nOver', bowling_start)
        if bowling_end == -1:
            bowling_end = bowling_start + 1000
        
        bowling_section = pages_text[0][bowling_start:bowling_end]
        
        # Split into lines and parse
        lines = bowling_section.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Check if this is a bowler name (starts with capital letter, reasonable length)
            if line and line[0].isupper() and 2 <= len(line) <= 20 and line not in ['Bowler', 'No', 'Runs', 'Over', 'Batsman']:
                try:
                    # Next 5-6 lines should be: O, R, W, M, ECO, ...
                    if i + 5 < len(lines):
                        name = line
                        overs = float(lines[i+1].strip())
                        runs = int(lines[i+2].strip())
                        wickets = int(lines[i+3].strip())
                        maidens = int(lines[i+4].strip())
                        economy = float(lines[i+5].strip())
                        
                        # Validate data makes sense
                        if 0 <= overs <= 20 and 0 <= runs <= 200 and 0 <= wickets <= 10:
                            bowler = {
                                'name': name,
                                'overs': overs,
                                'runs': runs,
                                'wickets': wickets,
                                'maidens': maidens,
                                'economy': economy
                            }
                            match_data['bowling']['flames'].append(bowler)
                            print(f"{name:<20} {overs:<6} {runs:<6} {wickets:<6} {maidens:<6} {economy:<8.2f}")
                except:
                    pass
            i += 1
    
    # Opponent bowling from page 3
    print(f"\n{match_data['match_info']['opponent'].upper()} BOWLING:")
    print("=" * 70)
    print(f"{'Bowler':<20} {'O':<6} {'R':<6} {'W':<6} {'M':<6} {'Econ':<8}")
    print("-" * 70)
    
    if len(pages_text) >= 3:
        bowling_start = pages_text[2].find('Bowler\nO\nR\nW\nM\nECO')
        if bowling_start != -1:
            bowling_end = pages_text[2].find('No\nRuns\nOver', bowling_start)
            if bowling_end == -1:
                bowling_end = bowling_start + 1000
            
            bowling_section = pages_text[2][bowling_start:bowling_end]
            
            lines = bowling_section.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line and line[0].isupper() and 2 <= len(line) <= 20 and line not in ['Bowler', 'No', 'Runs', 'Over', 'Batsman']:
                    try:
                        if i + 5 < len(lines):
                            name = line
                            overs = float(lines[i+1].strip())
                            runs = int(lines[i+2].strip())
                            wickets = int(lines[i+3].strip())
                            maidens = int(lines[i+4].strip())
                            economy = float(lines[i+5].strip())
                            
                            if 0 <= overs <= 20 and 0 <= runs <= 200 and 0 <= wickets <= 10:
                                bowler = {
                                    'name': name,
                                    'overs': overs,
                                    'runs': runs,
                                    'wickets': wickets,
                                    'maidens': maidens,
                                    'economy': economy
                                }
                                match_data['bowling']['opponent'].append(bowler)
                                print(f"{name:<20} {overs:<6} {runs:<6} {wickets:<6} {maidens:<6} {economy:<8.2f}")
                    except:
                        pass
                i += 1
    
    # Display fielding statistics
    print(f"\nFLAMES FIELDING:")
    print("=" * 70)
    print(f"{'Fielder':<20} {'Catches':<10} {'Stumpings':<12} {'Run Outs':<10} {'Total':<8}")
    print("-" * 70)
    
    # Sort by total dismissals
    flames_fielders = sorted(
        match_data['fielding']['flames'].items(),
        key=lambda x: x[1]['catches'] + x[1]['stumpings'] + x[1]['run_outs'],
        reverse=True
    )
    
    for fielder, stats in flames_fielders:
        total = stats['catches'] + stats['stumpings'] + stats['run_outs']
        print(f"{fielder:<20} {stats['catches']:<10} {stats['stumpings']:<12} {stats['run_outs']:<10} {total:<8}")
    
    print(f"\n{match_data['match_info']['opponent'].upper()} FIELDING:")
    print("=" * 70)
    print(f"{'Fielder':<20} {'Catches':<10} {'Stumpings':<12} {'Run Outs':<10} {'Total':<8}")
    print("-" * 70)
    
    opponent_fielders = sorted(
        match_data['fielding']['opponent'].items(),
        key=lambda x: x[1]['catches'] + x[1]['stumpings'] + x[1]['run_outs'],
        reverse=True
    )
    
    for fielder, stats in opponent_fielders:
        total = stats['catches'] + stats['stumpings'] + stats['run_outs']
        print(f"{fielder:<20} {stats['catches']:<10} {stats['stumpings']:<12} {stats['run_outs']:<10} {total:<8}")
    
    # Save to JSON
    with open('format1_with_fielding.json', 'w', encoding='utf-8') as f:
        json.dump(match_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print(f"Total Opponent Batsmen: {len(match_data['batting']['opponent'])}")
    print(f"Total Flames Batsmen: {len(match_data['batting']['flames'])}")
    print(f"Total Flames Bowlers: {len(match_data['bowling']['flames'])}")
    print(f"Total Opponent Bowlers: {len(match_data['bowling']['opponent'])}")
    print(f"Total Flames Fielders: {len(match_data['fielding']['flames'])}")
    print(f"Total Opponent Fielders: {len(match_data['fielding']['opponent'])}")
    print("=" * 70)
    print("Complete extraction with fielding saved to: format1_with_fielding.json")
    print("=" * 70)
    
    return match_data

# Test on the Format 1 PDF
extract_format1_with_fielding('Flames/Old Data/08 - 27-Feb-21 - Sledgers VS Flames.pdf')
