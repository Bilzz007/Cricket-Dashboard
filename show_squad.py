import json

with open('flames_squad.json', 'r', encoding='utf-8') as f:
    squad = json.load(f)

print('=' * 80)
print('                    FLAMES CC CURRENT SQUAD')
print('=' * 80)
print()

for i, player in enumerate(squad['squad'], 1):
    print(f'{i}. Player ID: {player["player_id"]}')
    print(f'   Full Name: {player["full_name"]}')
    print(f'   Common Names: {", ".join(player["common_names"])}')
    print(f'   Role: {player["role"]}')
    print(f'   Batting Style: {player["batting_style"] or "Not specified"}')
    print(f'   Bowling Style: {player["bowling_style"] or "Not specified"}')
    print(f'   Captain: {"Yes" if player["is_captain"] else "No"}')
    print(f'   Wicketkeeper: {"Yes" if player["is_wicketkeeper"] else "No"}')
    print()

print('=' * 80)
print(f'Total Players: {len(squad["squad"])}')
print('=' * 80)
print()
print('PLEASE PROVIDE FOR EACH PLAYER:')
print('- Correct Full Name')
print('- All possible name variations (short names, nicknames, etc.)')
print('- Role (Batsman/Bowler/All-rounder/Wicketkeeper)')
print('- Batting Style (Right-hand bat / Left-hand bat)')
print('- Bowling Style (if applicable)')
print('- Is Captain? (Yes/No)')
print('- Is Wicketkeeper? (Yes/No)')

