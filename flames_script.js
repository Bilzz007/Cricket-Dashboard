// Flames CC Dashboard Script

class FlamesDashboard {
    constructor() {
        this.squadData = {
            team_name: "Flames CC",
            squad: [
                {
                    id: "bilal",
                    full_name: "Bilal Ahmed",
                    common_names: ["Bilal", "Bilal Ahmed"],
                    role: "All-rounder",
                    batting_style: "Right-handed",
                    bowling_style: "Right-arm fast",
                    is_captain: true,
                    is_wicketkeeper: false,
                    stats: { runs: 1250, wickets: 45, matches: 35 }
                },
                {
                    id: "safi",
                    full_name: "Safi Ahmed",
                    common_names: ["Safi", "Safi Ahmed"],
                    role: "Batsman",
                    batting_style: "Right-handed",
                    bowling_style: "Right-arm medium",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 980, wickets: 12, matches: 32 }
                },
                {
                    id: "nehal",
                    full_name: "Nehal Ahmed",
                    common_names: ["Nehal", "Nehal Ahmed"],
                    role: "Bowler",
                    batting_style: "Right-handed",
                    bowling_style: "Right-arm fast",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 320, wickets: 68, matches: 30 }
                },
                {
                    id: "hassan",
                    full_name: "Hassan Khan",
                    common_names: ["Hassan", "Hassan Khan"],
                    role: "Wicketkeeper",
                    batting_style: "Right-handed",
                    bowling_style: "N/A",
                    is_captain: false,
                    is_wicketkeeper: true,
                    stats: { runs: 750, catches: 45, stumpings: 12, matches: 28 }
                },
                {
                    id: "ali",
                    full_name: "Ali Raza",
                    common_names: ["Ali", "Ali Raza"],
                    role: "Batsman",
                    batting_style: "Left-handed",
                    bowling_style: "Right-arm off-spin",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 890, wickets: 8, matches: 25 }
                },
                {
                    id: "ahmed",
                    full_name: "Ahmed Shah",
                    common_names: ["Ahmed", "Ahmed Shah"],
                    role: "Bowler",
                    batting_style: "Right-handed",
                    bowling_style: "Left-arm spin",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 180, wickets: 42, matches: 22 }
                },
                {
                    id: "umar",
                    full_name: "Umar Farooq",
                    common_names: ["Umar", "Umar Farooq"],
                    role: "All-rounder",
                    batting_style: "Right-handed",
                    bowling_style: "Right-arm medium",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 650, wickets: 25, matches: 20 }
                },
                {
                    id: "zain",
                    full_name: "Zain Malik",
                    common_names: ["Zain", "Zain Malik"],
                    role: "Batsman",
                    batting_style: "Right-handed",
                    bowling_style: "Right-arm leg-spin",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 720, wickets: 15, matches: 18 }
                },
                {
                    id: "tariq",
                    full_name: "Tariq Hassan",
                    common_names: ["Tariq", "Tariq Hassan"],
                    role: "Bowler",
                    batting_style: "Right-handed",
                    bowling_style: "Right-arm fast",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 150, wickets: 35, matches: 15 }
                },
                {
                    id: "khalid",
                    full_name: "Khalid Mehmood",
                    common_names: ["Khalid", "Khalid Mehmood"],
                    role: "Batsman",
                    batting_style: "Left-handed",
                    bowling_style: "Right-arm medium",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 580, wickets: 5, matches: 16 }
                },
                {
                    id: "yousuf",
                    full_name: "Yousuf Ahmed",
                    common_names: ["Yousuf", "Yousuf Ahmed"],
                    role: "Bowler",
                    batting_style: "Right-handed",
                    bowling_style: "Right-arm medium-fast",
                    is_captain: false,
                    is_wicketkeeper: false,
                    stats: { runs: 200, wickets: 28, matches: 12 }
                }
            ],
            name_mapping: {
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
            },
            notes: {
                last_updated: new Date().toISOString().split('T')[0],
                total_players: 11,
                active_squad: true
            }
        };
        
        this.init();
    }

    init() {
        console.log('🔥 Flames Dashboard Initializing...');
        this.setupTabNavigation();
        this.setupEventListeners();
        this.loadDashboardData();
        console.log('✅ Dashboard initialized successfully!');
    }

    setupTabNavigation() {
        console.log('Setting up tab navigation...');
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        console.log(`Found ${tabButtons.length} tab buttons and ${tabContents.length} tab contents`);

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                console.log(`Tab clicked: ${targetTab}`);
                
                // Remove active class from all tabs
                tabButtons.forEach(btn => {
                    btn.classList.remove('active');
                    btn.style.transform = 'scale(1)';
                });
                tabContents.forEach(content => {
                    content.classList.remove('active');
                });
                
                // Add active class to clicked tab
                button.classList.add('active');
                button.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    button.style.transform = 'scale(1)';
                }, 150);
                
                // Show target tab
                const targetContent = document.getElementById(targetTab);
                if (targetContent) {
                    targetContent.classList.add('active');
                    console.log(`✅ Tab activated: ${targetTab}`);
                    this.loadTabContent(targetTab);
                } else {
                    console.error(`❌ Target content not found: ${targetTab}`);
                }
            });
        });

        // Set initial tab
        const initialButton = document.querySelector('[data-tab="overview"]');
        if (initialButton) {
            initialButton.click();
        }
    }

    loadTabContent(tabId) {
        switch(tabId) {
            case 'overview':
                this.loadOverview();
                break;
            case 'matches':
                this.loadMatches();
                break;
            case 'players':
                this.loadPlayers();
                break;
            case 'squad':
                this.loadSquad();
                break;
            case 'analytics':
                this.loadAnalytics();
                break;
            case 'insights':
                this.loadInsights();
                break;
        }
    }

    setupEventListeners() {
        // Refresh button
        document.getElementById('refreshBtn')?.addEventListener('click', () => {
            this.refreshDashboard();
        });

        // Squad management buttons
        document.getElementById('addPlayerBtn')?.addEventListener('click', () => {
            this.addNewPlayer();
        });

        document.getElementById('saveSquadBtn')?.addEventListener('click', () => {
            this.saveSquad();
        });

        document.getElementById('exportSquadBtn')?.addEventListener('click', () => {
            this.exportSquad();
        });

        // Generate insights button
        document.getElementById('generateInsightsBtn')?.addEventListener('click', () => {
            this.generateInsights();
        });
    }

    loadDashboardData() {
        // Load initial dashboard data
        this.updateHeaderStats();
        this.loadOverview();
        
        // Load real cricket data if available
        this.loadRealCricketData();
    }

    loadRealCricketData() {
        // Try to load real cricket data
        if (typeof REAL_CRICKET_DATA !== 'undefined') {
            console.log('Loading real cricket data...');
            this.realData = REAL_CRICKET_DATA;
            this.updateWithRealData();
        } else if (typeof getRealCricketData === 'function') {
            console.log('Loading real cricket data via function...');
            this.realData = getRealCricketData();
            this.updateWithRealData();
        } else {
            console.log('No real cricket data available, using default data');
        }
    }

    updateWithRealData() {
        if (!this.realData) return;
        
        console.log('Updating dashboard with real data...');
        
        // Update header stats with real data
        const stats = this.realData.statistics;
        document.getElementById('headerMatches').textContent = stats.total_matches;
        document.getElementById('headerWinRate').textContent = `${stats.win_rate}%`;
        document.getElementById('headerPlayers').textContent = stats.total_players || this.squadData.squad.length;
        
        // Update overview stats
        document.getElementById('totalMatches').textContent = stats.total_matches;
        document.getElementById('winRate').textContent = `${stats.win_rate}%`;
        document.getElementById('totalRuns').textContent = stats.total_runs_scored.toLocaleString();
        
        // Update squad with real players
        if (this.realData.players) {
            this.updateSquadWithRealPlayers();
        }
        
        console.log('Dashboard updated with real data');
    }

    updateSquadWithRealPlayers() {
        // Update squad data with real player statistics
        this.realData.players.forEach(realPlayer => {
            const squadPlayer = this.squadData.squad.find(p => 
                p.id === realPlayer.id || p.full_name === realPlayer.name
            );
            
            if (squadPlayer) {
                // Update player stats
                squadPlayer.stats = {
                    runs: realPlayer.runs || 0,
                    wickets: realPlayer.wickets || 0,
                    matches: realPlayer.matches || 0,
                    catches: realPlayer.catches || 0,
                    batting_average: realPlayer.batting_average || 0,
                    highest_score: realPlayer.highest_score || 0
                };
            }
        });
        
        // Re-render squad if squad tab is active
        if (document.getElementById('squad').classList.contains('active')) {
            this.renderSquadCards();
            this.updateSquadStats();
        }
    }

    updateHeaderStats() {
        // Use real data if available, otherwise use defaults
        const totalMatches = this.realData ? this.realData.statistics.total_matches : 48;
        const winRate = this.realData ? this.realData.statistics.win_rate : 65;
        const totalPlayers = this.squadData.squad.length;

        document.getElementById('headerMatches').textContent = totalMatches;
        document.getElementById('headerWinRate').textContent = `${winRate}%`;
        document.getElementById('headerPlayers').textContent = totalPlayers;
    }

    loadOverview() {
        console.log('Loading overview...');
        this.createPerformanceChart();
        this.createResultsChart();
    }

    loadMatches() {
        console.log('Loading matches...');
        const matchesGrid = document.getElementById('matchesGrid');
        if (!matchesGrid) return;

        const matches = [
            { opponent: "Sledgers", date: "27-Feb-21", result: "Won", score: "145/7 vs 120/10" },
            { opponent: "Classic XI Karachi", date: "26-Sep-21", result: "Won", score: "180/5 vs 165/8" },
            { opponent: "Grace Sports", date: "17-Oct-21", result: "Lost", score: "140/9 vs 145/6" },
            { opponent: "Young Challengers", date: "24-Oct-21", result: "Won", score: "160/7 vs 155/9" },
            { opponent: "FD47", date: "31-Oct-21", result: "Won", score: "175/6 vs 170/8" },
            { opponent: "Labbaik Sports", date: "15-Nov-21", result: "Lost", score: "130/8 vs 135/7" },
            { opponent: "Gladiator CC", date: "21-Nov-21", result: "Won", score: "155/9 vs 150/10" }
        ];

        matchesGrid.innerHTML = '';
        matches.forEach(match => {
            const matchCard = document.createElement('div');
            matchCard.className = 'match-card';
            matchCard.innerHTML = `
                <h4>vs ${match.opponent}</h4>
                <p><strong>Date:</strong> ${match.date}</p>
                <p><strong>Score:</strong> ${match.score}</p>
                <div class="match-result ${match.result.toLowerCase()}">
                    ${match.result}
                </div>
            `;
            matchesGrid.appendChild(matchCard);
        });
    }

    loadPlayers() {
        console.log('Loading players...');
        const playersGrid = document.getElementById('playersGrid');
        if (!playersGrid) return;

        playersGrid.innerHTML = '';
        this.squadData.squad.forEach(player => {
            const playerCard = document.createElement('div');
            playerCard.className = 'player-card';
            playerCard.innerHTML = `
                <div class="player-info">
                    <h4>${player.full_name} ${player.is_captain ? '👑' : ''} ${player.is_wicketkeeper ? '🥅' : ''}</h4>
                    <p><strong>Role:</strong> ${player.role}</p>
                    <p><strong>Batting:</strong> ${player.batting_style}</p>
                    <p><strong>Bowling:</strong> ${player.bowling_style}</p>
                    <p><strong>Runs:</strong> ${player.stats.runs || 0}</p>
                    <p><strong>Wickets:</strong> ${player.stats.wickets || 0}</p>
                    <p><strong>Matches:</strong> ${player.stats.matches || 0}</p>
                </div>
            `;
            playersGrid.appendChild(playerCard);
        });
    }

    loadSquad() {
        console.log('Loading squad management...');
        this.updateSquadStats();
        this.renderSquadCards();
    }

    updateSquadStats() {
        const totalPlayers = this.squadData.squad.length;
        const batsmen = this.squadData.squad.filter(p => p.role.includes('Batsman') || p.role.includes('All-rounder')).length;
        const bowlers = this.squadData.squad.filter(p => p.role.includes('Bowler') || p.role.includes('All-rounder')).length;
        const allrounders = this.squadData.squad.filter(p => p.role === 'All-rounder').length;

        document.getElementById('totalPlayersCount').textContent = totalPlayers;
        document.getElementById('totalBatsmen').textContent = batsmen;
        document.getElementById('totalBowlers').textContent = bowlers;
        document.getElementById('totalAllrounders').textContent = allrounders;
    }

    renderSquadCards() {
        const squadGrid = document.getElementById('squadGrid');
        if (!squadGrid) return;

        squadGrid.innerHTML = '';
        this.squadData.squad.forEach((player, index) => {
            const playerCard = document.createElement('div');
            playerCard.className = 'player-card';
            playerCard.innerHTML = `
                <div class="player-info">
                    <h4>${player.full_name} ${player.is_captain ? '👑' : ''} ${player.is_wicketkeeper ? '🥅' : ''}</h4>
                    <p><strong>Role:</strong> ${player.role}</p>
                    <p><strong>Batting:</strong> ${player.batting_style}</p>
                    <p><strong>Bowling:</strong> ${player.bowling_style}</p>
                    <p><strong>Common Names:</strong> ${player.common_names.join(', ')}</p>
                </div>
                <div class="player-actions">
                    <button class="btn btn-primary edit-player-btn" onclick="dashboard.editPlayer(${index})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn btn-secondary view-stats-btn" onclick="dashboard.viewPlayerStats(${index})">
                        <i class="fas fa-chart-bar"></i> Stats
                    </button>
                </div>
            `;
            squadGrid.appendChild(playerCard);
        });
    }

    editPlayer(index) {
        const player = this.squadData.squad[index];
        console.log(`Editing player: ${player.full_name}`);
        
        const newName = prompt(`Edit player name:`, player.full_name);
        if (newName && newName.trim()) {
            player.full_name = newName.trim();
            this.renderSquadCards();
            this.showMessage(`Player ${newName} updated successfully!`, 'success');
        }
    }

    viewPlayerStats(index) {
        const player = this.squadData.squad[index];
        console.log(`Viewing stats for: ${player.full_name}`);
        
        const stats = player.stats;
        let statsText = `Player: ${player.full_name}\n\n`;
        statsText += `Runs: ${stats.runs || 0}\n`;
        statsText += `Wickets: ${stats.wickets || 0}\n`;
        statsText += `Matches: ${stats.matches || 0}\n`;
        if (stats.catches) statsText += `Catches: ${stats.catches}\n`;
        if (stats.stumpings) statsText += `Stumpings: ${stats.stumpings}\n`;
        
        alert(statsText);
    }

    addNewPlayer() {
        console.log('Adding new player...');
        const name = prompt('Enter player name:');
        if (name && name.trim()) {
            const newPlayer = {
                id: name.toLowerCase().replace(/\s+/g, ''),
                full_name: name.trim(),
                common_names: [name.trim()],
                role: "Batsman",
                batting_style: "Right-handed",
                bowling_style: "N/A",
                is_captain: false,
                is_wicketkeeper: false,
                stats: { runs: 0, wickets: 0, matches: 0 }
            };
            
            this.squadData.squad.push(newPlayer);
            this.squadData.notes.total_players = this.squadData.squad.length;
            this.renderSquadCards();
            this.updateSquadStats();
            this.showMessage(`Player ${name} added successfully!`, 'success');
        }
    }

    saveSquad() {
        console.log('Saving squad...');
        this.squadData.notes.last_updated = new Date().toISOString().split('T')[0];
        localStorage.setItem('flames_squad', JSON.stringify(this.squadData));
        this.showMessage('Squad saved to browser storage!', 'success');
    }

    exportSquad() {
        console.log('Exporting squad...');
        const dataStr = JSON.stringify(this.squadData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'flames_squad.json';
        link.click();
        
        URL.revokeObjectURL(url);
        this.showMessage('Squad exported successfully!', 'success');
    }

    loadAnalytics() {
        console.log('Loading analytics...');
        this.createTeamTrendsChart();
        this.createContributionChart();
    }

    loadInsights() {
        console.log('Loading insights...');
        const insightsGrid = document.getElementById('insightsGrid');
        if (!insightsGrid) return;

        const insights = [
            {
                title: "Top Performer",
                content: "Bilal Ahmed leads the team with 1,250 runs and 45 wickets. Consider him for captaincy in crucial matches.",
                type: "performance"
            },
            {
                title: "Bowling Strength",
                content: "Nehal Ahmed is your best bowler with 68 wickets. Use him in powerplay and death overs.",
                type: "strategy"
            },
            {
                title: "Batting Depth",
                content: "Your top 5 batsmen contribute 78% of total runs. Consider strengthening the middle order.",
                type: "analysis"
            }
        ];

        insightsGrid.innerHTML = '';
        insights.forEach(insight => {
            const insightCard = document.createElement('div');
            insightCard.className = 'insight-card';
            insightCard.innerHTML = `
                <h4>${insight.title}</h4>
                <p>${insight.content}</p>
            `;
            insightsGrid.appendChild(insightCard);
        });
    }

    generateInsights() {
        console.log('Generating new insights...');
        this.showMessage('Generating AI insights...', 'info');
        
        setTimeout(() => {
            this.loadInsights();
            this.showMessage('New insights generated!', 'success');
        }, 1500);
    }

    refreshDashboard() {
        console.log('Refreshing dashboard...');
        this.showMessage('Refreshing data...', 'info');
        
        setTimeout(() => {
            this.loadDashboardData();
            this.showMessage('Dashboard refreshed!', 'success');
        }, 1000);
    }

    createPerformanceChart() {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Win Rate %',
                    data: [60, 65, 70, 68, 72, 65],
                    borderColor: '#ff6b35',
                    backgroundColor: 'rgba(255, 107, 53, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#ffffff' }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: '#b8b8b8' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#b8b8b8' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
    }

    createResultsChart() {
        const ctx = document.getElementById('resultsChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Won', 'Lost', 'Draw'],
                datasets: [{
                    data: [31, 15, 2],
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#ffffff' }
                    }
                }
            }
        });
    }

    createTeamTrendsChart() {
        const ctx = document.getElementById('teamTrendsChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Runs Scored', 'Wickets Taken', 'Catches', 'Run Outs'],
                datasets: [{
                    label: 'Team Stats',
                    data: [2847, 275, 89, 23],
                    backgroundColor: '#ff6b35'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#ffffff' }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: '#b8b8b8' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#b8b8b8' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
    }

    createContributionChart() {
        const ctx = document.getElementById('contributionChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Bilal', 'Safi', 'Nehal', 'Others'],
                datasets: [{
                    data: [35, 25, 20, 20],
                    backgroundColor: ['#ff6b35', '#f7931e', '#1a1a2e', '#16213e']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#ffffff' }
                    }
                }
            }
        });
    }

    showMessage(message, type = 'info') {
        // Simple message display
        console.log(`${type.toUpperCase()}: ${message}`);
        
        // Create a temporary message element
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#ff6b35'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}

// Initialize dashboard when DOM is loaded
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new FlamesDashboard();
    window.dashboard = dashboard; // Make it globally accessible
});
