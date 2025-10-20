#!/usr/bin/env python3
"""
Comprehensive Cricket Data Extractors for Flames CC Dashboard
Handles all PDF formats: Full Scorecard, CricHeroes, Spartan, and Unknown formats
"""

import os
import json
import re
from pathlib import Path
import fitz  # PyMuPDF
from datetime import datetime

class CricketDataExtractor:
    def __init__(self):
        self.extracted_data = {
            "matches": [],
            "players": {},
            "statistics": {
                "total_matches": 0,
                "total_wins": 0,
                "total_losses": 0,
                "total_draws": 0,
                "win_rate": 0.0
            },
            "extraction_metadata": {
                "extraction_date": datetime.now().isoformat(),
                "total_files_processed": 0,
                "successful_extractions": 0,
                "failed_extractions": 0
            }
        }
        
        # Player name normalization
        self.player_mapping = {
            "bilal": "Bilal Ahmed",
            "safi": "Safi Ahmed", 
            "nehal": "Nehal Ahmed",
            "hassan": "Hassan Khan",
            "ali": "Ali Raza",
            "ahmed": "Ahmed Shah",
            "umar": "Umar Farooq",
            "zain": "Zain Malik",
            "tariq": "Tariq Hassan",
            "khalid": "Khalid Mehmood",
            "yousuf": "Yousuf Ahmed"
        }

    def extract_from_filename(self, filename):
        """Extract basic match info from filename"""
        match_info = {
            "filename": filename,
            "match_number": None,
            "date": None,
            "opponent": None,
            "venue": None
        }
        
        # Pattern 1: "08 - 27-Feb-21 - Sledgers VS Flames.pdf"
        pattern1 = r"(\d+)\s*-\s*(\d{1,2}-[A-Za-z]{3}-\d{2})\s*-\s*(.+?)\s*VS\s*Flames"
        match1 = re.search(pattern1, filename, re.IGNORECASE)
        if match1:
            match_info["match_number"] = int(match1.group(1))
            match_info["date"] = match1.group(2)
            match_info["opponent"] = match1.group(3).strip()
            return match_info
        
        # Pattern 2: "Scorecard_10640768.pdf" (CricHeroes format)
        if filename.startswith("Scorecard_"):
            match_info["match_number"] = filename.replace("Scorecard_", "").replace(".pdf", "")
            match_info["opponent"] = "Unknown (CricHeroes Format)"
            return match_info
        
        # Pattern 3: "Spartans VS Alpha CC.pdf"
        pattern3 = r"(.+?)\s*VS\s*(.+)"
        match3 = re.search(pattern3, filename, re.IGNORECASE)
        if match3:
            match_info["opponent"] = match3.group(2).replace(".pdf", "").strip()
            return match_info
        
        return match_info

    def extract_full_scorecard_format(self, pdf_path, match_info):
        """Extract data from Full Scorecard format PDFs"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            match_data = {
                "match_info": match_info,
                "format": "full_scorecard",
                "innings": [],
                "players": {},
                "extras": {},
                "result": "Unknown"
            }
            
            # Extract match result
            result_patterns = [
                r"Result:\s*(.+?)(?:\n|$)",
                r"Flames\s+(?:won|lost|drew)",
                r"(?:won|lost|drew)\s+by\s+(\d+)\s+(?:runs|wickets)"
            ]
            
            for pattern in result_patterns:
                result_match = re.search(pattern, text, re.IGNORECASE)
                if result_match:
                    match_data["result"] = result_match.group(0)
                    break
            
            # Extract innings data
            innings_pattern = r"(\d+st|\d+nd)\s+Innings"
            innings_matches = re.findall(innings_pattern, text, re.IGNORECASE)
            
            for i, innings_num in enumerate(innings_matches):
                innings_data = {
                    "innings_number": innings_num,
                    "team": "Flames" if i == 0 else "Opponent",
                    "runs": 0,
                    "wickets": 0,
                    "overs": 0,
                    "batsmen": [],
                    "bowlers": []
                }
                
                # Extract runs and wickets
                score_pattern = r"(\d{1,3})/(\d{1,2})"
                score_match = re.search(score_pattern, text)
                if score_match:
                    innings_data["runs"] = int(score_match.group(1))
                    innings_data["wickets"] = int(score_match.group(2))
                
                # Extract overs
                overs_pattern = r"(\d{1,2}\.\d)\s+overs?"
                overs_match = re.search(overs_pattern, text)
                if overs_match:
                    innings_data["overs"] = float(overs_match.group(1))
                
                match_data["innings"].append(innings_data)
            
            # Extract player performances
            player_lines = re.findall(r"([A-Za-z\s]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)", text)
            
            for player_line in player_lines:
                if len(player_line) >= 6:
                    player_name = player_line[0].strip()
                    runs = int(player_line[1])
                    balls = int(player_line[2])
                    fours = int(player_line[3])
                    sixes = int(player_line[4])
                    strike_rate = float(player_line[5])
                    
                    # Normalize player name
                    normalized_name = self.normalize_player_name(player_name)
                    
                    if normalized_name not in match_data["players"]:
                        match_data["players"][normalized_name] = {
                            "batting": {"runs": 0, "balls": 0, "fours": 0, "sixes": 0, "strike_rate": 0.0},
                            "bowling": {"overs": 0.0, "runs": 0, "wickets": 0, "maidens": 0, "economy": 0.0},
                            "fielding": {"catches": 0, "stumpings": 0, "run_outs": 0}
                        }
                    
                    match_data["players"][normalized_name]["batting"]["runs"] += runs
                    match_data["players"][normalized_name]["batting"]["balls"] += balls
                    match_data["players"][normalized_name]["batting"]["fours"] += fours
                    match_data["players"][normalized_name]["batting"]["sixes"] += sixes
                    match_data["players"][normalized_name]["batting"]["strike_rate"] = strike_rate
            
            return match_data
            
        except Exception as e:
            print(f"Error extracting from {pdf_path}: {e}")
            return None

    def extract_cricheroes_format(self, pdf_path, match_info):
        """Extract data from CricHeroes format PDFs"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            match_data = {
                "match_info": match_info,
                "format": "cricheroes",
                "innings": [],
                "players": {},
                "extras": {},
                "result": "Unknown"
            }
            
            # CricHeroes specific patterns
            # Extract team names
            team_pattern = r"Team\s+(\d+):\s*(.+?)(?:\n|$)"
            team_matches = re.findall(team_pattern, text, re.IGNORECASE)
            
            for team_match in team_matches:
                team_name = team_match[1].strip()
                if "Flames" in team_name or "Raftaar" in team_name:
                    match_data["team_name"] = team_name
            
            # Extract player performances
            player_pattern = r"([A-Za-z\s]+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)"
            player_matches = re.findall(player_pattern, text)
            
            for player_match in player_matches:
                if len(player_match) >= 6:
                    player_name = player_match[0].strip()
                    runs = int(player_match[1])
                    balls = int(player_match[2])
                    fours = int(player_match[3])
                    sixes = int(player_match[4])
                    strike_rate = float(player_match[5])
                    
                    normalized_name = self.normalize_player_name(player_name)
                    
                    if normalized_name not in match_data["players"]:
                        match_data["players"][normalized_name] = {
                            "batting": {"runs": 0, "balls": 0, "fours": 0, "sixes": 0, "strike_rate": 0.0},
                            "bowling": {"overs": 0.0, "runs": 0, "wickets": 0, "maidens": 0, "economy": 0.0},
                            "fielding": {"catches": 0, "stumpings": 0, "run_outs": 0}
                        }
                    
                    match_data["players"][normalized_name]["batting"]["runs"] += runs
                    match_data["players"][normalized_name]["batting"]["balls"] += balls
                    match_data["players"][normalized_name]["batting"]["fours"] += fours
                    match_data["players"][normalized_name]["batting"]["sixes"] += sixes
                    match_data["players"][normalized_name]["batting"]["strike_rate"] = strike_rate
            
            return match_data
            
        except Exception as e:
            print(f"Error extracting CricHeroes format from {pdf_path}: {e}")
            return None

    def extract_spartan_format(self, pdf_path, match_info):
        """Extract data from Spartan format PDFs"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            match_data = {
                "match_info": match_info,
                "format": "spartan",
                "innings": [],
                "players": {},
                "extras": {},
                "result": "Unknown"
            }
            
            # Spartan format specific extraction
            # Look for common patterns in Spartan scorecards
            
            # Extract basic match info
            score_pattern = r"(\d{1,3})/(\d{1,2})\s+in\s+(\d{1,2}\.\d)\s+overs?"
            score_matches = re.findall(score_pattern, text, re.IGNORECASE)
            
            for i, score_match in enumerate(score_matches):
                innings_data = {
                    "innings_number": f"{i+1}st" if i == 0 else f"{i+1}nd",
                    "team": "Flames" if i == 0 else "Opponent",
                    "runs": int(score_match[0]),
                    "wickets": int(score_match[1]),
                    "overs": float(score_match[2]),
                    "batsmen": [],
                    "bowlers": []
                }
                match_data["innings"].append(innings_data)
            
            return match_data
            
        except Exception as e:
            print(f"Error extracting Spartan format from {pdf_path}: {e}")
            return None

    def normalize_player_name(self, raw_name):
        """Normalize player names to standard format"""
        # Clean the name
        name = raw_name.strip().lower()
        
        # Remove common suffixes/prefixes
        name = re.sub(r'\s+(c|b|run out|st|lbw|bowled|caught|not out)', '', name)
        
        # Check against known player mappings
        for short_name, full_name in self.player_mapping.items():
            if short_name in name or any(part in name for part in short_name.split()):
                return full_name
        
        # If no match found, return cleaned original
        return raw_name.strip().title()

    def process_all_pdfs(self):
        """Process all PDFs in both Old Data and New Data folders"""
        print("Starting comprehensive PDF extraction...")
        
        # Process Old Data folder
        old_data_path = Path("Flames/Old Data")
        if old_data_path.exists():
            print(f"Processing Old Data folder: {old_data_path}")
            old_pdfs = list(old_data_path.glob("*.pdf"))
            print(f"Found {len(old_pdfs)} PDFs in Old Data")
            
            for pdf_file in old_pdfs:
                print(f"  Processing: {pdf_file.name}")
                self.process_single_pdf(pdf_file)
        
        # Process New Data folder
        new_data_path = Path("Flames/New data")
        if new_data_path.exists():
            print(f"Processing New Data folder: {new_data_path}")
            new_pdfs = list(new_data_path.glob("*.pdf"))
            print(f"Found {len(new_pdfs)} PDFs in New Data")
            
            for pdf_file in new_pdfs:
                print(f"  Processing: {pdf_file.name}")
                self.process_single_pdf(pdf_file)
        
        # Calculate statistics
        self.calculate_statistics()
        
        print(f"Extraction complete! Processed {self.extracted_data['extraction_metadata']['total_files_processed']} files")
        print(f"Successful extractions: {self.extracted_data['extraction_metadata']['successful_extractions']}")
        print(f"Failed extractions: {self.extracted_data['extraction_metadata']['failed_extractions']}")

    def process_single_pdf(self, pdf_path):
        """Process a single PDF file"""
        self.extracted_data["extraction_metadata"]["total_files_processed"] += 1
        
        try:
            # Extract basic info from filename
            match_info = self.extract_from_filename(pdf_path.name)
            
            # Determine format and extract accordingly
            if "Scorecard_" in pdf_path.name:
                match_data = self.extract_cricheroes_format(pdf_path, match_info)
            elif "Spartans" in pdf_path.name or "Alpha" in pdf_path.name:
                match_data = self.extract_spartan_format(pdf_path, match_info)
            else:
                match_data = self.extract_full_scorecard_format(pdf_path, match_info)
            
            if match_data:
                self.extracted_data["matches"].append(match_data)
                self.extracted_data["extraction_metadata"]["successful_extractions"] += 1
                
                # Update player statistics
                self.update_player_statistics(match_data)
            else:
                self.extracted_data["extraction_metadata"]["failed_extractions"] += 1
                
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            self.extracted_data["extraction_metadata"]["failed_extractions"] += 1

    def update_player_statistics(self, match_data):
        """Update overall player statistics from match data"""
        for player_name, player_data in match_data["players"].items():
            if player_name not in self.extracted_data["players"]:
                self.extracted_data["players"][player_name] = {
                    "total_matches": 0,
                    "total_runs": 0,
                    "total_wickets": 0,
                    "total_catches": 0,
                    "total_stumpings": 0,
                    "total_run_outs": 0,
                    "batting_average": 0.0,
                    "bowling_average": 0.0,
                    "strike_rate": 0.0,
                    "economy_rate": 0.0
                }
            
            player_stats = self.extracted_data["players"][player_name]
            player_stats["total_matches"] += 1
            
            # Update batting stats
            if "batting" in player_data:
                batting = player_data["batting"]
                player_stats["total_runs"] += batting.get("runs", 0)
                player_stats["strike_rate"] = batting.get("strike_rate", 0.0)
            
            # Update bowling stats
            if "bowling" in player_data:
                bowling = player_data["bowling"]
                player_stats["total_wickets"] += bowling.get("wickets", 0)
                player_stats["economy_rate"] = bowling.get("economy", 0.0)
            
            # Update fielding stats
            if "fielding" in player_data:
                fielding = player_data["fielding"]
                player_stats["total_catches"] += fielding.get("catches", 0)
                player_stats["total_stumpings"] += fielding.get("stumpings", 0)
                player_stats["total_run_outs"] += fielding.get("run_outs", 0)

    def calculate_statistics(self):
        """Calculate overall team statistics"""
        total_matches = len(self.extracted_data["matches"])
        wins = 0
        losses = 0
        draws = 0
        
        for match in self.extracted_data["matches"]:
            result = match.get("result", "").lower()
            if "won" in result:
                wins += 1
            elif "lost" in result:
                losses += 1
            elif "draw" in result:
                draws += 1
        
        self.extracted_data["statistics"] = {
            "total_matches": total_matches,
            "total_wins": wins,
            "total_losses": losses,
            "total_draws": draws,
            "win_rate": round((wins / total_matches * 100), 2) if total_matches > 0 else 0.0
        }

    def save_data(self, filename="comprehensive_cricket_database.json"):
        """Save extracted data to JSON file"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to: {filename}")

def main():
    print("Flames CC - Comprehensive Cricket Data Extraction")
    print("=" * 60)
    
    extractor = CricketDataExtractor()
    extractor.process_all_pdfs()
    extractor.save_data()
    
    # Print summary
    stats = extractor.extracted_data["statistics"]
    print(f"\nExtraction Summary:")
    print(f"Total Matches: {stats['total_matches']}")
    print(f"Wins: {stats['total_wins']}")
    print(f"Losses: {stats['total_losses']}")
    print(f"Draws: {stats['total_draws']}")
    print(f"Win Rate: {stats['win_rate']}%")
    print(f"Total Players: {len(extractor.extracted_data['players'])}")

if __name__ == "__main__":
    main()
