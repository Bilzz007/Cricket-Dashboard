#!/usr/bin/env python3
"""
Integrate real data into advanced_dashboard.html
"""

import json

def integrate_advanced_dashboard():
    """Integrate real data into the advanced dashboard"""
    
    print("=== INTEGRATING DATA INTO ADVANCED DASHBOARD ===\n")
    
    # Load dashboard data
    with open("dashboard_data.json", 'r') as f:
        data = json.load(f)
    
    # Load the advanced dashboard template
    with open("advanced_dashboard.html", 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert data to JavaScript
    js_data = json.dumps(data, indent=4)
    
    # Create the data injection script
    data_script = f'''
    <script>
        // Real extracted data from 129 CricHeroes PDFs
        const REAL_CRICKET_DATA = {js_data};
        
        // Initialize with real data
        window.addEventListener('DOMContentLoaded', function() {{
            console.log('Loading real cricket data...');
            loadRealData();
        }});
        
        function loadRealData() {{
            const summary = REAL_CRICKET_DATA.summary;
            const players = Object.values(REAL_CRICKET_DATA.players);
            const matches = REAL_CRICKET_DATA.matches;
            
            // Update header stats
            document.getElementById('headerMatches').textContent = summary.total_matches;
            document.getElementById('headerWinRate').textContent = summary.win_percentage + '%';
            document.getElementById('headerPlayers').textContent = Object.keys(REAL_CRICKET_DATA.players).length;
            
            // Update overview stats
            if (document.getElementById('totalMatches')) {{
                document.getElementById('totalMatches').textContent = summary.total_matches;
            }}
            if (document.getElementById('winRate')) {{
                document.getElementById('winRate').textContent = summary.win_percentage + '%';
            }}
            if (document.getElementById('totalWins')) {{
                document.getElementById('totalWins').textContent = summary.wins;
            }}
            if (document.getElementById('totalLosses')) {{
                document.getElementById('totalLosses').textContent = summary.losses;
            }}
            if (document.getElementById('totalRuns')) {{
                document.getElementById('totalRuns').textContent = summary.total_runs.toLocaleString();
            }}
            if (document.getElementById('totalPlayers')) {{
                document.getElementById('totalPlayers').textContent = Object.keys(REAL_CRICKET_DATA.players).length;
            }}
            
            console.log('Real data loaded successfully!');
            console.log('Total Matches:', summary.total_matches);
            console.log('Win Rate:', summary.win_percentage + '%');
            console.log('Total Players:', Object.keys(REAL_CRICKET_DATA.players).length);
        }}
    </script>
    '''
    
    # Insert the data script before </body>
    html_content = html_content.replace('</body>', data_script + '\n</body>')
    
    # Save the updated dashboard
    with open("flames_dashboard.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Advanced dashboard updated with real data!")
    print("File: flames_dashboard.html")
    print(f"Data: {data['summary']['total_matches']} matches, {len(data['players'])} players")
    print("\nThe dashboard is ready to use!")

if __name__ == "__main__":
    integrate_advanced_dashboard()

