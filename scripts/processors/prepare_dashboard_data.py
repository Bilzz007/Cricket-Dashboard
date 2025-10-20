#!/usr/bin/env python3
"""
Prepare aggregated data for dashboard integration
"""

import json
from collections import defaultdict, Counter

def prepare_dashboard_data():
    """Prepare aggregated data for dashboard"""
    
    print("=== PREPARING DASHBOARD DATA ===\n")
    
    # Load database
    with open("cricket_database_cricheroes.json", 'r') as f:
        database = json.load(f)
    
    matches = database["matches"]
    
    print(f"Processing {len(matches)} matches...\n")
    
    # Initialize aggregated data
    dashboard_data = {
        "summary": {
            "total_matches": 0,
            "flames_matches": 0,
            "raftaar_matches": 0,
            "wins": 0,
            "losses": 0,
            "total_runs": 0,
            "total_wickets": 0,
            "highest_score": {"score": 0, "opponent": "", "date": ""},
            "lowest_score": {"score": 999, "opponent": "", "date": ""}
        },
        "players": {},
        "matches": [],
        "recent_form": []
    }
    
    # Separate Flames and Raftaar matches
    our_team_names = ['flames', 'raftaar']
    
    for match in matches:
        team1 = match['match_info'].get('team1', '').lower()
        team2 = match['match_info'].get('team2', '').lower()
        
        # Check if this is our team's match
        is_our_match = False
        our_team = ""
        opponent = ""
        
        for team_name in our_team_names:
            if team_name in team1:
                is_our_match = True
                our_team = match['match_info'].get('team1', '')
                opponent = match['match_info'].get('team2', '')
                break
            elif team_name in team2:
                is_our_match = True
                our_team = match['match_info'].get('team2', '')
                opponent = match['match_info'].get('team1', '')
                break
        
        if not is_our_match:
            continue
        
        # Process match
        process_match(match, our_team, opponent, dashboard_data)
    
    # Calculate final stats
    finalize_stats(dashboard_data)
    
    # Save dashboard data
    with open("dashboard_data.json", 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print("\nDashboard data saved to: dashboard_data.json")
    
    # Print summary
    print_summary(dashboard_data)
    
    return dashboard_data

def process_match(match, our_team, opponent, dashboard_data):
    """Process individual match data"""
    
    team1 = match['match_info'].get('team1', '').lower()
    team2 = match['match_info'].get('team2', '').lower()
    result = match['match_info'].get('result', '').lower()
    
    # Determine if Flames or Raftaar
    is_flames = 'flames' in our_team.lower()
    is_raftaar = 'raftaar' in our_team.lower()
    
    if is_flames:
        dashboard_data["summary"]["flames_matches"] += 1
    elif is_raftaar:
        dashboard_data["summary"]["raftaar_matches"] += 1
    
    dashboard_data["summary"]["total_matches"] += 1
    
    # Determine if we batted first or second
    first_innings_team = match['first_innings']['batting_team'].lower()
    our_team_lower = our_team.lower()
    
    batted_first = any(name in first_innings_team for name in ['flames', 'raftaar'])
    
    if batted_first:
        our_batting = match['first_innings']['batting']
        our_bowling = match['second_innings']['bowling']
        our_score = match['first_innings']['score']
        opponent_score = match['second_innings']['score']
    else:
        our_batting = match['second_innings']['batting']
        our_bowling = match['first_innings']['bowling']
        our_score = match['second_innings']['score']
        opponent_score = match['first_innings']['score']
    
    # Extract runs from score (e.g., "127/9" -> 127)
    try:
        our_runs = int(our_score.split('/')[0]) if '/' in our_score else 0
        opponent_runs = int(opponent_score.split('/')[0]) if '/' in opponent_score else 0
    except:
        our_runs = 0
        opponent_runs = 0
    
    dashboard_data["summary"]["total_runs"] += our_runs
    
    # Determine win/loss
    if our_team.lower() in result or ('flames' in result and is_flames) or ('raftaar' in result and is_raftaar):
        if 'won' in result:
            dashboard_data["summary"]["wins"] += 1
    else:
        if 'won' in result:
            dashboard_data["summary"]["losses"] += 1
    
    # Track highest and lowest scores
    if our_runs > dashboard_data["summary"]["highest_score"]["score"]:
        dashboard_data["summary"]["highest_score"] = {
            "score": our_runs,
            "opponent": opponent,
            "date": match['match_info'].get('date', '')
        }
    
    if our_runs < dashboard_data["summary"]["lowest_score"]["score"] and our_runs > 0:
        dashboard_data["summary"]["lowest_score"] = {
            "score": our_runs,
            "opponent": opponent,
            "date": match['match_info'].get('date', '')
        }
    
    # Process player stats
    process_player_stats(our_batting, our_bowling, dashboard_data)
    
    # Add to matches list
    dashboard_data["matches"].append({
        "tournament": match['match_info'].get('tournament', ''),
        "opponent": opponent,
        "our_score": our_score,
        "opponent_score": opponent_score,
        "result": match['match_info'].get('result', ''),
        "date": match['match_info'].get('date', ''),
        "venue": match['match_info'].get('venue', '')
    })

def process_player_stats(batting_records, bowling_records, dashboard_data):
    """Process player statistics"""
    
    # Process batting
    for bat in batting_records:
        player = bat['player']
        
        if player not in dashboard_data["players"]:
            dashboard_data["players"][player] = {
                "name": player,
                "batting": {
                    "matches": 0,
                    "innings": 0,
                    "runs": 0,
                    "balls": 0,
                    "fours": 0,
                    "sixes": 0,
                    "highest_score": 0,
                    "dismissals": 0,
                    "not_outs": 0
                },
                "bowling": {
                    "matches": 0,
                    "overs": 0,
                    "runs": 0,
                    "wickets": 0,
                    "best_figures": ""
                },
                "fielding": {
                    "catches": 0
                }
            }
        
        player_data = dashboard_data["players"][player]
        
        # Update batting stats
        player_data["batting"]["innings"] += 1
        
        try:
            runs = int(bat['runs'])
            balls = int(bat['balls'])
            fours = int(bat['fours'])
            sixes = int(bat['sixes'])
            
            player_data["batting"]["runs"] += runs
            player_data["batting"]["balls"] += balls
            player_data["batting"]["fours"] += fours
            player_data["batting"]["sixes"] += sixes
            
            if runs > player_data["batting"]["highest_score"]:
                player_data["batting"]["highest_score"] = runs
            
            if bat['dismissal_type'] == 'not_out':
                player_data["batting"]["not_outs"] += 1
            else:
                player_data["batting"]["dismissals"] += 1
        except:
            pass
    
    # Process bowling
    for bowl in bowling_records:
        bowler = bowl['bowler']
        
        if bowler not in dashboard_data["players"]:
            dashboard_data["players"][bowler] = {
                "name": bowler,
                "batting": {
                    "matches": 0,
                    "innings": 0,
                    "runs": 0,
                    "balls": 0,
                    "fours": 0,
                    "sixes": 0,
                    "highest_score": 0,
                    "dismissals": 0,
                    "not_outs": 0
                },
                "bowling": {
                    "matches": 0,
                    "overs": 0,
                    "runs": 0,
                    "wickets": 0,
                    "best_figures": ""
                },
                "fielding": {
                    "catches": 0
                }
            }
        
        player_data = dashboard_data["players"][bowler]
        
        # Update bowling stats
        player_data["bowling"]["matches"] += 1
        
        try:
            overs = float(bowl['overs'])
            runs = int(bowl['runs'])
            wickets = int(bowl['wickets'])
            
            player_data["bowling"]["overs"] += overs
            player_data["bowling"]["runs"] += runs
            player_data["bowling"]["wickets"] += wickets
        except:
            pass

def finalize_stats(dashboard_data):
    """Finalize calculated statistics"""
    
    # Calculate player averages and strike rates
    for player_name, player in dashboard_data["players"].items():
        # Batting average
        if player["batting"]["dismissals"] > 0:
            player["batting"]["average"] = round(player["batting"]["runs"] / player["batting"]["dismissals"], 2)
        else:
            player["batting"]["average"] = player["batting"]["runs"]
        
        # Batting strike rate
        if player["batting"]["balls"] > 0:
            player["batting"]["strike_rate"] = round((player["batting"]["runs"] / player["batting"]["balls"]) * 100, 2)
        else:
            player["batting"]["strike_rate"] = 0
        
        # Bowling average
        if player["bowling"]["wickets"] > 0:
            player["bowling"]["average"] = round(player["bowling"]["runs"] / player["bowling"]["wickets"], 2)
        else:
            player["bowling"]["average"] = 0
        
        # Bowling economy
        if player["bowling"]["overs"] > 0:
            player["bowling"]["economy"] = round(player["bowling"]["runs"] / player["bowling"]["overs"], 2)
        else:
            player["bowling"]["economy"] = 0
    
    # Calculate win percentage
    total = dashboard_data["summary"]["total_matches"]
    if total > 0:
        dashboard_data["summary"]["win_percentage"] = round((dashboard_data["summary"]["wins"] / total) * 100, 2)
    else:
        dashboard_data["summary"]["win_percentage"] = 0

def print_summary(dashboard_data):
    """Print summary statistics"""
    
    print("\n" + "="*80)
    print("DASHBOARD DATA SUMMARY")
    print("="*80)
    
    summary = dashboard_data["summary"]
    
    print(f"\nMATCH STATISTICS:")
    print(f"  Total Matches: {summary['total_matches']}")
    print(f"  Flames Matches: {summary['flames_matches']}")
    print(f"  Raftaar Matches: {summary['raftaar_matches']}")
    print(f"  Wins: {summary['wins']}")
    print(f"  Losses: {summary['losses']}")
    print(f"  Win %: {summary['win_percentage']}%")
    
    print(f"\nTEAM STATISTICS:")
    print(f"  Total Runs Scored: {summary['total_runs']}")
    print(f"  Highest Score: {summary['highest_score']['score']} vs {summary['highest_score']['opponent']}")
    print(f"  Lowest Score: {summary['lowest_score']['score']} vs {summary['lowest_score']['opponent']}")
    
    print(f"\nPLAYER STATISTICS:")
    print(f"  Total Players: {len(dashboard_data['players'])}")
    
    # Top run scorers
    top_scorers = sorted(dashboard_data["players"].items(), 
                        key=lambda x: x[1]["batting"]["runs"], 
                        reverse=True)[:5]
    
    print(f"\n  Top 5 Run Scorers:")
    for i, (name, stats) in enumerate(top_scorers, 1):
        print(f"    {i}. {name}: {stats['batting']['runs']} runs @ {stats['batting']['average']}")
    
    # Top wicket takers
    top_bowlers = sorted(dashboard_data["players"].items(), 
                        key=lambda x: x[1]["bowling"]["wickets"], 
                        reverse=True)[:5]
    
    print(f"\n  Top 5 Wicket Takers:")
    for i, (name, stats) in enumerate(top_bowlers, 1):
        if stats['bowling']['wickets'] > 0:
            print(f"    {i}. {name}: {stats['bowling']['wickets']} wickets @ {stats['bowling']['average']}")

if __name__ == "__main__":
    prepare_dashboard_data()
