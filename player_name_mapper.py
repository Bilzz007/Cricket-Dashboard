import json
import re

class PlayerNameMapper:
    def __init__(self, squad_file='flames_squad.json'):
        """Initialize player name mapper with squad database"""
        with open(squad_file, 'r', encoding='utf-8') as f:
            self.squad_data = json.load(f)
        
        self.name_mapping = self.squad_data['name_mapping']
        self.squad = {player['player_id']: player for player in self.squad_data['squad']}
        
    def normalize_player_name(self, raw_name):
        """
        Normalize a player name from scorecard to standard player ID and full name
        
        Args:
            raw_name: Name as it appears in scorecard (may include dismissal info)
        
        Returns:
            dict: {
                'player_id': 'P001',
                'full_name': 'Abdul Majid',
                'raw_name': 'Majid\nc Bilal b Monu'
            }
        """
        # Extract just the player name (remove dismissal info)
        # Pattern: Name is usually before dismissal keywords
        dismissal_keywords = ['c ', 'b ', 'stumped', 'not out', 'run out', 'lbw', 'hit wicket']
        
        # Clean the raw name
        clean_name = raw_name.strip()
        
        # Remove common prefixes from scorecards
        clean_name = re.sub(r'^s\s+SR\s+', '', clean_name, flags=re.IGNORECASE)
        
        # Split by newlines and take the first meaningful part before dismissal
        parts = clean_name.split('\n')
        player_name = parts[0] if parts else clean_name
        
        # If first part is just formatting, try next part
        if player_name.lower() in ['s', 'sr', 'r', 'b']:
            player_name = parts[1] if len(parts) > 1 else player_name
        
        # Remove dismissal info
        for keyword in dismissal_keywords:
            if keyword in player_name:
                player_name = player_name.split(keyword)[0].strip()
                break
        
        # Clean up any remaining whitespace
        player_name = ' '.join(player_name.split())
        
        # Try to find in mapping
        player_id = self.name_mapping.get(player_name)
        
        if player_id:
            return {
                'player_id': player_id,
                'full_name': self.squad[player_id]['full_name'],
                'raw_name': raw_name,
                'normalized_name': player_name
            }
        else:
            # Return unknown player
            return {
                'player_id': None,
                'full_name': player_name,
                'raw_name': raw_name,
                'normalized_name': player_name,
                'warning': f'Unknown player: {player_name}'
            }
    
    def get_player_info(self, player_id):
        """Get full player information by ID"""
        return self.squad.get(player_id)
    
    def add_new_player(self, full_name, common_names, role='Unknown', 
                       batting_style=None, bowling_style=None):
        """
        Add a new player to the squad database
        
        Args:
            full_name: Full official name
            common_names: List of name variations
            role: Player role (Batsman/Bowler/All-rounder/Wicketkeeper)
            batting_style: Batting style description
            bowling_style: Bowling style description
        """
        # Generate new player ID
        existing_ids = [p['player_id'] for p in self.squad_data['squad']]
        id_numbers = [int(pid.replace('P', '')) for pid in existing_ids]
        new_id = f"P{max(id_numbers) + 1:03d}"
        
        # Create new player entry
        new_player = {
            'player_id': new_id,
            'full_name': full_name,
            'common_names': common_names,
            'role': role,
            'batting_style': batting_style,
            'bowling_style': bowling_style,
            'is_captain': False,
            'is_wicketkeeper': False
        }
        
        # Add to squad
        self.squad_data['squad'].append(new_player)
        self.squad[new_id] = new_player
        
        # Update name mapping
        for name in common_names:
            self.name_mapping[name] = new_id
            self.squad_data['name_mapping'][name] = new_id
        
        # Save to file
        with open('flames_squad.json', 'w', encoding='utf-8') as f:
            json.dump(self.squad_data, f, indent=2, ensure_ascii=False)
        
        print(f"Added new player: {full_name} ({new_id})")
        return new_id
    
    def get_all_unknown_players(self, extracted_data):
        """
        Scan extracted data and find all unknown players
        
        Args:
            extracted_data: Dictionary with batting/bowling/fielding data
        
        Returns:
            list: Unknown player names that need to be added
        """
        unknown_players = set()
        
        # Check batting
        for team in ['flames', 'opponent']:
            if team in extracted_data.get('batting', {}):
                for player in extracted_data['batting'][team]:
                    result = self.normalize_player_name(player['name'])
                    if result['player_id'] is None:
                        unknown_players.add(result['normalized_name'])
        
        # Check bowling
        for team in ['flames', 'opponent']:
            if team in extracted_data.get('bowling', {}):
                for player in extracted_data['bowling'][team]:
                    result = self.normalize_player_name(player['name'])
                    if result['player_id'] is None:
                        unknown_players.add(result['normalized_name'])
        
        # Check fielding
        for team in ['flames', 'opponent']:
            if team in extracted_data.get('fielding', {}):
                for player_name in extracted_data['fielding'][team].keys():
                    result = self.normalize_player_name(player_name)
                    if result['player_id'] is None:
                        unknown_players.add(result['normalized_name'])
        
        return list(unknown_players)


# Example usage
if __name__ == "__main__":
    mapper = PlayerNameMapper()
    
    # Test with some names from the extracted data
    test_names = [
        "s\nSR\nHassan\nc Bilal b Saif",
        "Majid\nc Bilal b Monu",
        "Leo\nc Adil b Haris",
        "A.Rehman",
        "Bilal"
    ]
    
    print("=== TESTING PLAYER NAME NORMALIZATION ===\n")
    for name in test_names:
        result = mapper.normalize_player_name(name)
        print(f"Raw: {name[:30]}...")
        print(f"  -> Player ID: {result['player_id']}")
        print(f"  -> Full Name: {result['full_name']}")
        if 'warning' in result:
            print(f"  -> WARNING: {result['warning']}")
        print()

