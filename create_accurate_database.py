#!/usr/bin/env python3
"""
Create Accurate Cricket Database for Flames CC Dashboard
Processes extracted data and creates clean, accurate database
"""

import json
from pathlib import Path
import re
from datetime import datetime

class DatabaseProcessor:
    def __init__(self):
        self.raw_data = None
        self.clean_data = {
            "matches": [],
            "players": {},
            "statistics": {
                "total_matches": 0,
                "total_wins": 0,
                "total_losses": 0,
                "total_draws": 0,
                "win_rate": 0.0,
                "total_runs_scored": 0,
                "total_wickets_taken": 0,
                "total_catches": 0
            },
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "data_source": "PDF extraction from Old Data and New Data folders"
            }
        }
        
        # Known Flames CC players
        self.flames_players = {
            "Bilal Ahmed": {"role": "All-rounder", "is_captain": True, "is_wicketkeeper": False},
            "Safi Ahmed": {"role": "Batsman", "is_captain": False, "is_wicketkeeper": False},
            "Nehal Ahmed": {"role": "Bowler", "is_captain": False, "is_wicketkeeper": False},
            "Hassan Khan": {"role": "Wicketkeeper", "is_captain": False, "is_wicketkeeper": True},
            "Ali Raza": {"role": "Batsman", "is_captain": False, "is_wicketkeeper": False},
            "Ahmed Shah": {"role": "Bowler", "is_captain": False, "is_wicketkeeper": False},
            "Umar Farooq": {"role": "All-rounder", "is_captain": False, "is_wicketkeeper": False},
            "Zain Malik": {"role": "Batsman", "is_captain": False, "is_wicketkeeper": False},
            "Tariq Hassan": {"role": "Bowler", "is_captain": False, "is_wicketkeeper": False},
            "Khalid Mehmood": {"role": "Batsman", "is_captain": False, "is_wicketkeeper": False},
            "Yousuf Ahmed": {"role": "Bowler", "is_captain": False, "is_wicketkeeper": False}
        }

    def load_raw_data(self, filename="comprehensive_cricket_database.json"):
        """Load raw extracted data"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.raw_data = json.load(f)
            print(f"Loaded raw data: {len(self.raw_data['matches'])} matches")
            return True
        except Exception as e:
            print(f"Error loading raw data: {e}")
            return False

    def clean_match_data(self, match):
        """Clean and standardize match data"""
        clean_match = {
            "match_number": match["match_info"]["match_number"],
            "date": match["match_info"]["date"],
            "opponent": match["match_info"]["opponent"],
            "filename": match["match_info"]["filename"],
            "result": self.extract_clean_result(match.get("result", "")),
            "format": match.get("format", "unknown"),
            "innings": [],
            "flames_players": {},
            "match_summary": {}
        }
        
        # Clean innings data
        for innings in match.get("innings", []):
            clean_innings = {
                "team": innings.get("team", "Unknown"),
                "runs": innings.get("runs", 0),
                "wickets": innings.get("wickets", 0),
                "overs": innings.get("overs", 0.0)
            }
            clean_match["innings"].append(clean_innings)
        
        # Clean player data - only include Flames players
        for player_name, player_data in match.get("players", {}).items():
            clean_name = self.clean_player_name(player_name)
            if clean_name in self.flames_players:
                clean_match["flames_players"][clean_name] = {
                    "batting": {
                        "runs": player_data.get("batting", {}).get("runs", 0),
                        "balls": player_data.get("batting", {}).get("balls", 0),
                        "fours": player_data.get("batting", {}).get("fours", 0),
                        "sixes": player_data.get("batting", {}).get("sixes", 0),
                        "strike_rate": player_data.get("batting", {}).get("strike_rate", 0.0)
                    },
                    "bowling": {
                        "overs": player_data.get("bowling", {}).get("overs", 0.0),
                        "runs": player_data.get("bowling", {}).get("runs", 0),
                        "wickets": player_data.get("bowling", {}).get("wickets", 0),
                        "maidens": player_data.get("bowling", {}).get("maidens", 0),
                        "economy": player_data.get("bowling", {}).get("economy", 0.0)
                    },
                    "fielding": {
                        "catches": player_data.get("fielding", {}).get("catches", 0),
                        "stumpings": player_data.get("fielding", {}).get("stumpings", 0),
                        "run_outs": player_data.get("fielding", {}).get("run_outs", 0)
                    }
                }
        
        # Create match summary
        clean_match["match_summary"] = self.create_match_summary(clean_match)
        
        return clean_match

    def extract_clean_result(self, result_text):
        """Extract clean match result from result text"""
        result_text = result_text.lower()
        
        if "won" in result_text:
            if "lost" in result_text:
                return "Lost"
            else:
                return "Won"
        elif "lost" in result_text:
            return "Lost"
        elif "draw" in result_text or "tie" in result_text:
            return "Draw"
        else:
            return "Unknown"

    def clean_player_name(self, raw_name):
        """Clean and normalize player names"""
        # Remove common suffixes and prefixes
        name = re.sub(r'\s+(c|b|run out|st|lbw|bowled|caught|not out|ct|bw)', '', raw_name, flags=re.IGNORECASE)
        name = re.sub(r'^[A-Z]\s+', '', name)  # Remove single letter prefixes
        name = re.sub(r'\s+[A-Z]\s+', ' ', name)  # Remove single letter middle names
        
        # Clean up the name
        name = name.strip().title()
        
        # Map to known players
        name_mappings = {
            "Safi": "Safi Ahmed",
            "Bilal": "Bilal Ahmed",
            "Nehal": "Nehal Ahmed",
            "Hassan": "Hassan Khan",
            "Ali": "Ali Raza",
            "Ahmed": "Ahmed Shah",
            "Umar": "Umar Farooq",
            "Zain": "Zain Malik",
            "Tariq": "Tariq Hassan",
            "Khalid": "Khalid Mehmood",
            "Yousuf": "Yousuf Ahmed"
        }
        
        for short_name, full_name in name_mappings.items():
            if short_name in name:
                return full_name
        
        return name

    def create_match_summary(self, match):
        """Create match summary statistics"""
        summary = {
            "flames_total_runs": 0,
            "flames_total_wickets": 0,
            "opponent_total_runs": 0,
            "opponent_total_wickets": 0,
            "top_scorer": {"name": "", "runs": 0},
            "top_wicket_taker": {"name": "", "wickets": 0}
        }
        
        # Calculate totals from innings
        for innings in match["innings"]:
            if innings["team"] == "Flames":
                summary["flames_total_runs"] += innings["runs"]
                summary["flames_total_wickets"] += innings["wickets"]
            else:
                summary["opponent_total_runs"] += innings["runs"]
                summary["opponent_total_wickets"] += innings["wickets"]
        
        # Find top performers
        for player_name, player_data in match["flames_players"].items():
            runs = player_data["batting"]["runs"]
            wickets = player_data["bowling"]["wickets"]
            
            if runs > summary["top_scorer"]["runs"]:
                summary["top_scorer"] = {"name": player_name, "runs": runs}
            
            if wickets > summary["top_wicket_taker"]["wickets"]:
                summary["top_wicket_taker"] = {"name": player_name, "wickets": wickets}
        
        return summary

    def process_all_matches(self):
        """Process all matches and create clean database"""
        if not self.raw_data:
            print("No raw data loaded")
            return
        
        print("Processing matches...")
        
        for match in self.raw_data["matches"]:
            clean_match = self.clean_match_data(match)
            self.clean_data["matches"].append(clean_match)
        
        print(f"Processed {len(self.clean_data['matches'])} matches")

    def calculate_player_statistics(self):
        """Calculate overall player statistics"""
        print("Calculating player statistics...")
        
        # Initialize player stats
        for player_name in self.flames_players.keys():
            self.clean_data["players"][player_name] = {
                "total_matches": 0,
                "total_runs": 0,
                "total_wickets": 0,
                "total_catches": 0,
                "total_stumpings": 0,
                "total_run_outs": 0,
                "batting_average": 0.0,
                "bowling_average": 0.0,
                "strike_rate": 0.0,
                "economy_rate": 0.0,
                "highest_score": 0,
                "best_bowling": {"wickets": 0, "runs": 0}
            }
        
        # Aggregate statistics from all matches
        for match in self.clean_data["matches"]:
            for player_name, player_data in match["flames_players"].items():
                if player_name in self.clean_data["players"]:
                    player_stats = self.clean_data["players"][player_name]
                    player_stats["total_matches"] += 1
                    
                    # Batting stats
                    runs = player_data["batting"]["runs"]
                    balls = player_data["batting"]["balls"]
                    player_stats["total_runs"] += runs
                    player_stats["strike_rate"] = player_data["batting"]["strike_rate"]
                    if runs > player_stats["highest_score"]:
                        player_stats["highest_score"] = runs
                    
                    # Bowling stats
                    wickets = player_data["bowling"]["wickets"]
                    bowling_runs = player_data["bowling"]["runs"]
                    player_stats["total_wickets"] += wickets
                    player_stats["economy_rate"] = player_data["bowling"]["economy"]
                    
                    if wickets > player_stats["best_bowling"]["wickets"]:
                        player_stats["best_bowling"] = {"wickets": wickets, "runs": bowling_runs}
                    
                    # Fielding stats
                    player_stats["total_catches"] += player_data["fielding"]["catches"]
                    player_stats["total_stumpings"] += player_data["fielding"]["stumpings"]
                    player_stats["total_run_outs"] += player_data["fielding"]["run_outs"]
        
        # Calculate averages
        for player_name, player_stats in self.clean_data["players"].items():
            if player_stats["total_matches"] > 0:
                # Simple batting average (runs per match)
                player_stats["batting_average"] = round(
                    player_stats["total_runs"] / player_stats["total_matches"], 2
                )
                
                # Simple bowling average (runs per wicket)
                if player_stats["total_wickets"] > 0:
                    total_bowling_runs = sum(
                        match["flames_players"][player_name]["bowling"]["runs"]
                        for match in self.clean_data["matches"]
                        if player_name in match["flames_players"]
                    )
                    player_stats["bowling_average"] = round(
                        total_bowling_runs / player_stats["total_wickets"], 2
                    )

    def calculate_team_statistics(self):
        """Calculate overall team statistics"""
        print("Calculating team statistics...")
        
        total_matches = len(self.clean_data["matches"])
        wins = 0
        losses = 0
        draws = 0
        total_runs = 0
        total_wickets = 0
        total_catches = 0
        
        for match in self.clean_data["matches"]:
            # Count results
            result = match["result"]
            if result == "Won":
                wins += 1
            elif result == "Lost":
                losses += 1
            elif result == "Draw":
                draws += 1
            
            # Aggregate stats
            total_runs += match["match_summary"]["flames_total_runs"]
            total_wickets += match["match_summary"]["flames_total_wickets"]
            
            for player_data in match["flames_players"].values():
                total_catches += player_data["fielding"]["catches"]
        
        self.clean_data["statistics"] = {
            "total_matches": total_matches,
            "total_wins": wins,
            "total_losses": losses,
            "total_draws": draws,
            "win_rate": round((wins / total_matches * 100), 2) if total_matches > 0 else 0.0,
            "total_runs_scored": total_runs,
            "total_wickets_taken": total_wickets,
            "total_catches": total_catches
        }

    def create_dashboard_data(self):
        """Create data formatted for the dashboard"""
        dashboard_data = {
            "matches": [],
            "players": [],
            "statistics": self.clean_data["statistics"]
        }
        
        # Format matches for dashboard
        for match in self.clean_data["matches"][:20]:  # Last 20 matches
            dashboard_match = {
                "id": match["match_number"],
                "date": match["date"],
                "opponent": match["opponent"],
                "result": match["result"],
                "flames_score": match["match_summary"]["flames_total_runs"],
                "opponent_score": match["match_summary"]["opponent_total_runs"],
                "top_scorer": match["match_summary"]["top_scorer"]["name"],
                "top_wicket_taker": match["match_summary"]["top_wicket_taker"]["name"]
            }
            dashboard_data["matches"].append(dashboard_match)
        
        # Format players for dashboard
        for player_name, player_stats in self.clean_data["players"].items():
            if player_stats["total_matches"] > 0:  # Only include players who have played
                player_info = self.flames_players[player_name]
                dashboard_player = {
                    "id": player_name.lower().replace(" ", "_"),
                    "name": player_name,
                    "role": player_info["role"],
                    "is_captain": player_info["is_captain"],
                    "is_wicketkeeper": player_info["is_wicketkeeper"],
                    "matches": player_stats["total_matches"],
                    "runs": player_stats["total_runs"],
                    "wickets": player_stats["total_wickets"],
                    "catches": player_stats["total_catches"],
                    "batting_average": player_stats["batting_average"],
                    "highest_score": player_stats["highest_score"]
                }
                dashboard_data["players"].append(dashboard_player)
        
        return dashboard_data

    def save_clean_database(self):
        """Save clean database to files"""
        # Save complete clean database
        with open("clean_cricket_database.json", "w", encoding="utf-8") as f:
            json.dump(self.clean_data, f, indent=2, ensure_ascii=False)
        
        # Save dashboard-formatted data
        dashboard_data = self.create_dashboard_data()
        with open("dashboard_cricket_data.json", "w", encoding="utf-8") as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
        
        # Create JavaScript file for dashboard
        js_content = f"// Flames CC Cricket Data - Auto-generated\n"
        js_content += f"const REAL_CRICKET_DATA = {json.dumps(dashboard_data, indent=2)};\n"
        js_content += f"function getRealCricketData() {{ return REAL_CRICKET_DATA; }}"
        
        with open("real_cricket_data.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        
        print("Clean database saved to:")
        print("  - clean_cricket_database.json")
        print("  - dashboard_cricket_data.json")
        print("  - real_cricket_data.js")

    def process(self):
        """Main processing function"""
        print("Flames CC - Creating Accurate Cricket Database")
        print("=" * 50)
        
        if not self.load_raw_data():
            return
        
        self.process_all_matches()
        self.calculate_player_statistics()
        self.calculate_team_statistics()
        self.save_clean_database()
        
        # Print summary
        stats = self.clean_data["statistics"]
        print(f"\nDatabase Summary:")
        print(f"Total Matches: {stats['total_matches']}")
        print(f"Wins: {stats['total_wins']}")
        print(f"Losses: {stats['total_losses']}")
        print(f"Draws: {stats['total_draws']}")
        print(f"Win Rate: {stats['win_rate']}%")
        print(f"Total Runs Scored: {stats['total_runs_scored']}")
        print(f"Total Wickets Taken: {stats['total_wickets_taken']}")
        print(f"Total Catches: {stats['total_catches']}")
        print(f"Active Players: {len([p for p in self.clean_data['players'].values() if p['total_matches'] > 0])}")

def main():
    processor = DatabaseProcessor()
    processor.process()

if __name__ == "__main__":
    main()
