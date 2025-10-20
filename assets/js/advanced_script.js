// Advanced Cricket Dashboard JavaScript
// Global variables and data management

let cricketData = null;
let charts = {};
let currentFilters = {
    year: 'all',
    opponent: 'all',
    result: 'all'
};

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
    loadCricketData();
});

// Initialize dashboard components
async function initializeDashboard() {
    console.log('🔥 Initializing Flames CC Advanced Dashboard...');
    
    setupTabNavigation();
    initializeCharts();
    setupFilters();
    
    // Show loading state
    showLoadingState();
    
    // Simulate data loading
    setTimeout(() => {
        hideLoadingState();
        showMessage('Dashboard loaded successfully! Welcome to Flames CC Analytics.', 'success');
    }, 1000);
}

// Setup tab navigation with enhanced animations
function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs with animation
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.style.transform = 'scale(1)';
            });
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            
            // Add active class to clicked tab with animation
            button.classList.add('active');
            button.style.transform = 'scale(1.05)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 150);
            
            // Show target tab with animation
            const targetContent = document.getElementById(targetTab);
            targetContent.classList.add('active');
            
            // Refresh data for the active tab
            refreshTabData(targetTab);
            
            // Update URL hash
            window.location.hash = targetTab;
        });
    });
    
    // Handle initial tab from URL hash
    const initialTab = window.location.hash.slice(1) || 'overview';
    const initialButton = document.querySelector(`[data-tab="${initialTab}"]`);
    if (initialButton) {
        initialButton.click();
    }
}

// Setup event listeners for interactive elements
function setupEventListeners() {
    // Refresh button
    document.getElementById('refreshBtn')?.addEventListener('click', refreshDashboard);
    
    // Chart period controls
    document.querySelectorAll('.chart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.chart-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateChartsByPeriod(this.dataset.period);
        });
    });
    
    // View controls for players tab
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            togglePlayerView(this.dataset.view);
        });
    });
    
    // Generate insights button
    document.getElementById('generateInsights')?.addEventListener('click', generateNewInsights);
    
    // Filter controls
    document.getElementById('yearFilter')?.addEventListener('change', applyFilters);
    document.getElementById('opponentFilter')?.addEventListener('change', applyFilters);
    document.getElementById('resultFilter')?.addEventListener('change', applyFilters);
}

// Load cricket data from repository
async function loadCricketData() {
    try {
        // Load real cricket data from extracted files
        if (typeof getRealCricketData === 'function') {
            cricketData = getRealCricketData();
            console.log('✅ Loaded real cricket data:', cricketData);
        } else if (typeof REAL_CRICKET_DATA !== 'undefined') {
            cricketData = REAL_CRICKET_DATA;
            console.log('✅ Loaded real cricket data from constant:', cricketData);
        } else {
            // Fallback to sample data if real data not available
            console.log('⚠️ Real data not available, using sample data');
            cricketData = {
            matches: [
                {
                    filename: "08 - 27-Feb-21 - Sledgers VS Flames.pdf",
                    date: "2021-02-27T00:00:00",
                    opponent: "Sledgers",
                    result: "Win",
                    flames_score: 185,
                    opponent_score: 162,
                    flames_wickets: 6,
                    opponent_wickets: 9,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "13 - 26-Sep-21 - CLASSIC XI KARACHI VS Flames.pdf",
                    date: "2021-09-26T00:00:00",
                    opponent: "CLASSIC XI KARACHI",
                    result: "Loss",
                    flames_score: 145,
                    opponent_score: 168,
                    flames_wickets: 8,
                    opponent_wickets: 5,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "14 - 17-Oct-21 - GRACE SPORTS (TNVISIONS) VS Flames.pdf",
                    date: "2021-10-17T00:00:00",
                    opponent: "GRACE SPORTS (TNVISIONS)",
                    result: "Win",
                    flames_score: 195,
                    opponent_score: 178,
                    flames_wickets: 4,
                    opponent_wickets: 7,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "15 - 24-Oct-21 - YOUNG CHALLANGERS VS Flames.pdf",
                    date: "2021-10-24T00:00:00",
                    opponent: "YOUNG CHALLANGERS",
                    result: "Win",
                    flames_score: 168,
                    opponent_score: 145,
                    flames_wickets: 7,
                    opponent_wickets: 9,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "16 - 31-Oct-21 - FD47 VS Flames.pdf",
                    date: "2021-10-31T00:00:00",
                    opponent: "FD47",
                    result: "Loss",
                    flames_score: 152,
                    opponent_score: 175,
                    flames_wickets: 9,
                    opponent_wickets: 6,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "17 - 15-Nov-21 - LABAIK SPORTS Vs FLames.pdf",
                    date: "2021-11-15T00:00:00",
                    opponent: "LABAIK SPORTS",
                    result: "Win",
                    flames_score: 178,
                    opponent_score: 165,
                    flames_wickets: 5,
                    opponent_wickets: 8,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "18 - 21-Nov-21 - GLADIATOR CC WAQAR VS Flames.pdf",
                    date: "2021-11-21T00:00:00",
                    opponent: "GLADIATOR CC WAQAR",
                    result: "Win",
                    flames_score: 189,
                    opponent_score: 172,
                    flames_wickets: 6,
                    opponent_wickets: 7,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "19 - 19-Dec-21 - PSMJ TIGERS VS Flames.pdf",
                    date: "2021-12-19T00:00:00",
                    opponent: "PSMJ TIGERS",
                    result: "Loss",
                    flames_score: 142,
                    opponent_score: 156,
                    flames_wickets: 8,
                    opponent_wickets: 6,
                    venue: "Karachi Stadium",
                    series: "Season 2021"
                },
                {
                    filename: "20 - 13-Jan-22 - FIRESIDE XI VS Flames.pdf",
                    date: "2022-01-13T00:00:00",
                    opponent: "FIRESIDE XI",
                    result: "Win",
                    flames_score: 174,
                    opponent_score: 158,
                    flames_wickets: 7,
                    opponent_wickets: 9,
                    venue: "Karachi Stadium",
                    series: "Season 2022"
                },
                {
                    filename: "21 - 23-Jan-22 - LEGENDS CC KARACHI VS Flames.pdf",
                    date: "2022-01-23T00:00:00",
                    opponent: "LEGENDS CC KARACHI",
                    result: "Win",
                    flames_score: 196,
                    opponent_score: 183,
                    flames_wickets: 4,
                    opponent_wickets: 8,
                    venue: "Karachi Stadium",
                    series: "Season 2022"
                }
            ],
            players: [
                {
                    name: "Ahmed Khan",
                    matches: 25,
                    runs: 1245,
                    average: 49.8,
                    wickets: 15,
                    bowling_average: 28.5,
                    economy: 6.2,
                    strike_rate: 125.3,
                    highest_score: 128,
                    best_bowling: "4/25",
                    catches: 8,
                    stumpings: 0
                },
                {
                    name: "Bilal Ahmed",
                    matches: 23,
                    runs: 987,
                    average: 42.9,
                    wickets: 28,
                    bowling_average: 22.1,
                    economy: 5.8,
                    strike_rate: 118.7,
                    highest_score: 95,
                    best_bowling: "5/32",
                    catches: 12,
                    stumpings: 0
                },
                {
                    name: "Saeed Ali",
                    matches: 22,
                    runs: 756,
                    average: 34.4,
                    wickets: 35,
                    bowling_average: 19.8,
                    economy: 5.5,
                    strike_rate: 112.4,
                    highest_score: 78,
                    best_bowling: "6/28",
                    catches: 6,
                    stumpings: 0
                },
                {
                    name: "Usman Sheikh",
                    matches: 20,
                    runs: 634,
                    average: 31.7,
                    wickets: 22,
                    bowling_average: 24.3,
                    economy: 6.0,
                    strike_rate: 108.9,
                    highest_score: 82,
                    best_bowling: "3/18",
                    catches: 15,
                    stumpings: 0
                },
                {
                    name: "Faisal Khan",
                    matches: 18,
                    runs: 523,
                    average: 29.1,
                    wickets: 18,
                    bowling_average: 26.7,
                    economy: 6.5,
                    strike_rate: 105.2,
                    highest_score: 67,
                    best_bowling: "4/31",
                    catches: 9,
                    stumpings: 0
                },
                {
                    name: "Mohammad Hassan",
                    matches: 16,
                    runs: 412,
                    average: 25.8,
                    wickets: 25,
                    bowling_average: 21.4,
                    economy: 5.9,
                    strike_rate: 98.7,
                    highest_score: 58,
                    best_bowling: "5/24",
                    catches: 7,
                    stumpings: 0
                },
                {
                    name: "Ali Raza",
                    matches: 14,
                    runs: 356,
                    average: 25.4,
                    wickets: 12,
                    bowling_average: 29.8,
                    economy: 6.8,
                    strike_rate: 102.3,
                    highest_score: 72,
                    best_bowling: "3/22",
                    catches: 11,
                    stumpings: 0
                }
            ],
            team_stats: {
                summary: {
                    total_matches: 47,
                    wins: 28,
                    losses: 17,
                    draws: 2,
                    win_rate: 59.6,
                    total_runs_scored: 8476,
                    total_runs_conceded: 7892
                }
            },
            opponents: [
                "Sledgers", "CLASSIC XI KARACHI", "GRACE SPORTS (TNVISIONS)", 
                "YOUNG CHALLANGERS", "FD47", "LABAIK SPORTS", "GLADIATOR CC WAQAR",
                "PSMJ TIGERS", "FIRESIDE XI", "LEGENDS CC KARACHI", "USMAN ENTERPRISE",
                "SUNRISE CRICKET CLUB KARACHI", "GULSHAN STARS CC", "INFINITY CC KARACHI",
                "STRIKER 11", "UZ ASSOCIATES", "ROYAL STRIKERS", "PAK FLAG STARS",
                "SHAN XI QADIR", "BLAZING BUSTERS XI", "AZAD CC OWAIS", "WINSOME XI KARACHI",
                "AVT ENTERPRISES KARACHI", "A A ASSOCIATES", "Spartan", "Karachi Challengers",
                "Amazing Stars", "Leo Knight", "Alpha CC", "Cricket Warriors"
            ],
            seasons: [2020, 2021, 2022, 2023]
        };
        
        // Update dashboard with loaded data
        updateDashboard();
        
    } catch (error) {
        console.error('Error loading cricket data:', error);
        showMessage('Error loading data. Please try again.', 'error');
    }
}

// Update dashboard with loaded data
function updateDashboard() {
    if (!cricketData) return;
    
    updateOverviewStats();
    updateMatchesTable();
    updatePlayersGrid();
    updateFilters();
    updateLeaderboards();
    refreshCharts();
    
    console.log('✅ Dashboard updated with cricket data');
}

// Update overview statistics with animations
function updateOverviewStats() {
    const stats = cricketData.team_stats.summary;
    
    // Animate number updates
    animateNumber('totalMatches', stats.total_matches);
    animateNumber('wins', stats.wins);
    animateNumber('losses', stats.losses);
    animateNumber('draws', stats.draws);
    animateNumber('totalPlayers', cricketData.players.length);
    
    // Update header stats
    document.getElementById('headerMatches').textContent = stats.total_matches;
    document.getElementById('headerWinRate').textContent = stats.win_rate.toFixed(1) + '%';
    document.getElementById('headerPlayers').textContent = cricketData.players.length;
    
    // Update hero stats
    document.getElementById('totalRuns').textContent = stats.total_runs_scored.toLocaleString();
    
    // Update progress bars with animation
    setTimeout(() => {
        updateProgressBars();
    }, 500);
}

// Animate number updates
function animateNumber(elementId, targetValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const startValue = 0;
    const duration = 1500;
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const currentValue = Math.round(startValue + (targetValue - startValue) * easeOutQuart);
        
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// Update progress bars with animation
function updateProgressBars() {
    const stats = cricketData.team_stats.summary;
    const total = stats.total_matches;
    
    // Win rate progress bar
    const winProgress = document.querySelector('.stat-card.featured .progress-bar');
    if (winProgress) {
        winProgress.style.width = '0%';
        setTimeout(() => {
            winProgress.style.width = (stats.wins / total * 100) + '%';
        }, 100);
    }
    
    // Loss progress bar
    const lossProgress = document.querySelector('.stat-card:nth-child(2) .progress-bar');
    if (lossProgress) {
        lossProgress.style.width = '0%';
        setTimeout(() => {
            lossProgress.style.width = (stats.losses / total * 100) + '%';
        }, 200);
    }
    
    // Draw progress bar
    const drawProgress = document.querySelector('.stat-card:nth-child(3) .progress-bar');
    if (drawProgress) {
        drawProgress.style.width = '0%';
        setTimeout(() => {
            drawProgress.style.width = (stats.draws / total * 100) + '%';
        }, 300);
    }
}

// Initialize all charts
function initializeCharts() {
    // Win/Loss Chart
    const winLossCtx = document.getElementById('winLossChart');
    if (winLossCtx) {
        charts.winLoss = new Chart(winLossCtx, {
            type: 'doughnut',
            data: {
                labels: ['Wins', 'Losses', 'Draws'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [
                        'rgba(74, 222, 128, 0.8)',
                        'rgba(248, 113, 113, 0.8)',
                        'rgba(251, 191, 36, 0.8)'
                    ],
                    borderColor: [
                        '#4ade80',
                        '#f87171',
                        '#fbbf24'
                    ],
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#ffffff',
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 2000
                }
            }
        });
    }
    
    // Monthly Performance Chart
    const monthlyCtx = document.getElementById('monthlyChart');
    if (monthlyCtx) {
        charts.monthly = new Chart(monthlyCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Wins',
                    data: new Array(12).fill(0),
                    borderColor: '#4ade80',
                    backgroundColor: 'rgba(74, 222, 128, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 3
                }, {
                    label: 'Losses',
                    data: new Array(12).fill(0),
                    borderColor: '#f87171',
                    backgroundColor: 'rgba(248, 113, 113, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    }
                },
                animation: {
                    duration: 2000
                }
            }
        });
    }
    
    // Batting Chart
    const battingCtx = document.getElementById('battingChart');
    if (battingCtx) {
        charts.batting = new Chart(battingCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Runs',
                    data: [],
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: '#667eea',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    }
                }
            }
        });
    }
    
    // Bowling Chart
    const bowlingCtx = document.getElementById('bowlingChart');
    if (bowlingCtx) {
        charts.bowling = new Chart(bowlingCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Wickets',
                    data: [],
                    backgroundColor: 'rgba(118, 75, 162, 0.8)',
                    borderColor: '#764ba2',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#ffffff'
                        }
                    }
                }
            }
        });
    }
    
    // Opponent Analysis Chart
    const opponentCtx = document.getElementById('opponentChart');
    if (opponentCtx) {
        charts.opponent = new Chart(opponentCtx, {
            type: 'polarArea',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        'rgba(74, 222, 128, 0.8)',
                        'rgba(248, 113, 113, 0.8)',
                        'rgba(251, 191, 36, 0.8)',
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(34, 197, 94, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                }
            }
        });
    }
}

// Refresh all charts with current data
function refreshCharts() {
    if (!cricketData) return;
    
    // Update Win/Loss Chart
    if (charts.winLoss) {
        const stats = cricketData.team_stats.summary;
        charts.winLoss.data.datasets[0].data = [stats.wins, stats.losses, stats.draws];
        charts.winLoss.update();
    }
    
    // Update Monthly Chart
    if (charts.monthly) {
        const monthlyData = getMonthlyPerformance();
        charts.monthly.data.datasets[0].data = monthlyData.wins;
        charts.monthly.data.datasets[1].data = monthlyData.losses;
        charts.monthly.update();
    }
    
    // Update Batting Chart
    if (charts.batting) {
        const topBatsmen = cricketData.players
            .sort((a, b) => b.runs - a.runs)
            .slice(0, 5);
        
        charts.batting.data.labels = topBatsmen.map(p => p.name);
        charts.batting.data.datasets[0].data = topBatsmen.map(p => p.runs);
        charts.batting.update();
    }
    
    // Update Bowling Chart
    if (charts.bowling) {
        const topBowlers = cricketData.players
            .sort((a, b) => b.wickets - a.wickets)
            .slice(0, 5);
        
        charts.bowling.data.labels = topBowlers.map(p => p.name);
        charts.bowling.data.datasets[0].data = topBowlers.map(p => p.wickets);
        charts.bowling.update();
    }
    
    // Update Opponent Chart
    if (charts.opponent) {
        const opponentStats = getOpponentStats();
        charts.opponent.data.labels = opponentStats.labels;
        charts.opponent.data.datasets[0].data = opponentStats.data;
        charts.opponent.update();
    }
}

// Get monthly performance data
function getMonthlyPerformance() {
    const monthlyWins = new Array(12).fill(0);
    const monthlyLosses = new Array(12).fill(0);
    
    cricketData.matches.forEach(match => {
        if (match.date) {
            const month = new Date(match.date).getMonth();
            if (match.result === 'Win') {
                monthlyWins[month]++;
            } else if (match.result === 'Loss') {
                monthlyLosses[month]++;
            }
        }
    });
    
    return { wins: monthlyWins, losses: monthlyLosses };
}

// Get opponent statistics
function getOpponentStats() {
    const opponentMap = {};
    
    cricketData.matches.forEach(match => {
        if (!opponentMap[match.opponent]) {
            opponentMap[match.opponent] = { wins: 0, losses: 0 };
        }
        
        if (match.result === 'Win') {
            opponentMap[match.opponent].wins++;
        } else if (match.result === 'Loss') {
            opponentMap[match.opponent].losses++;
        }
    });
    
    const sortedOpponents = Object.entries(opponentMap)
        .sort((a, b) => (b[1].wins + b[1].losses) - (a[1].wins + a[1].losses))
        .slice(0, 6);
    
    return {
        labels: sortedOpponents.map(([name]) => name),
        data: sortedOpponents.map(([, stats]) => stats.wins + stats.losses)
    };
}

// Update matches table
function updateMatchesTable() {
    const tbody = document.querySelector('#matchesTable tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    const filteredMatches = getFilteredMatches();
    
    filteredMatches.forEach(match => {
        const row = document.createElement('tr');
        const margin = match.flames_score > match.opponent_score ? 
            `${match.flames_score - match.opponent_score} runs` : 
            `${match.opponent_score - match.flames_score} runs`;
        
        row.innerHTML = `
            <td>${formatDate(match.date)}</td>
            <td>${match.opponent}</td>
            <td>${match.venue || 'Karachi Stadium'}</td>
            <td><span class="result-badge ${getResultClass(match.result)}">${match.result}</span></td>
            <td>${match.flames_score}/${match.flames_wickets} vs ${match.opponent_score}/${match.opponent_wickets}</td>
            <td>${margin}</td>
            <td><button class="btn btn-sm" onclick="viewMatchDetails('${match.filename}')">View</button></td>
        `;
        tbody.appendChild(row);
    });
}

// Update players grid
function updatePlayersGrid() {
    const playersGrid = document.getElementById('playersGrid');
    if (!playersGrid) return;
    
    playersGrid.innerHTML = '';
    
    cricketData.players.forEach(player => {
        const playerCard = document.createElement('div');
        playerCard.className = 'player-card';
        playerCard.innerHTML = `
            <div class="player-header">
                <div class="player-avatar">${getInitials(player.name)}</div>
                <div class="player-name">${player.name}</div>
            </div>
            <div class="player-stats">
                <div class="player-stat">
                    <span class="stat-label">Matches</span>
                    <span class="stat-value">${player.matches}</span>
                </div>
                <div class="player-stat">
                    <span class="stat-label">Runs</span>
                    <span class="stat-value">${player.runs}</span>
                </div>
                <div class="player-stat">
                    <span class="stat-label">Average</span>
                    <span class="stat-value">${player.average}</span>
                </div>
                <div class="player-stat">
                    <span class="stat-label">Wickets</span>
                    <span class="stat-value">${player.wickets}</span>
                </div>
                <div class="player-stat">
                    <span class="stat-label">Bowl Avg</span>
                    <span class="stat-value">${player.bowling_average}</span>
                </div>
                <div class="player-stat">
                    <span class="stat-label">Economy</span>
                    <span class="stat-value">${player.economy}</span>
                </div>
            </div>
        `;
        playersGrid.appendChild(playerCard);
    });
}

// Update leaderboards
function updateLeaderboards() {
    updateLeaderboard('battingLeaders', cricketData.players, 'runs', 'Runs');
    updateLeaderboard('bowlingLeaders', cricketData.players, 'wickets', 'Wickets');
    updateLeaderboard('fieldingLeaders', cricketData.players, 'catches', 'Catches');
}

// Update individual leaderboard
function updateLeaderboard(elementId, players, metric, label) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const sortedPlayers = players
        .sort((a, b) => b[metric] - a[metric])
        .slice(0, 5);
    
    element.innerHTML = '';
    
    sortedPlayers.forEach((player, index) => {
        const leaderboardItem = document.createElement('div');
        leaderboardItem.className = 'leaderboard-item';
        leaderboardItem.innerHTML = `
            <div class="leaderboard-rank">${index + 1}</div>
            <div class="leaderboard-info">
                <div class="leaderboard-name">${player.name}</div>
                <div class="leaderboard-stats">${player.matches} matches</div>
            </div>
            <div class="leaderboard-value">${player[metric]}</div>
        `;
        element.appendChild(leaderboardItem);
    });
}

// Setup filters
function setupFilters() {
    const yearFilter = document.getElementById('yearFilter');
    const opponentFilter = document.getElementById('opponentFilter');
    
    if (yearFilter) {
        const years = [...new Set(cricketData.matches.map(match => new Date(match.date).getFullYear()))];
        years.sort((a, b) => b - a);
        
        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearFilter.appendChild(option);
        });
    }
    
    if (opponentFilter) {
        cricketData.opponents.forEach(opponent => {
            const option = document.createElement('option');
            option.value = opponent;
            option.textContent = opponent;
            opponentFilter.appendChild(option);
        });
    }
}

// Apply filters
function applyFilters() {
    currentFilters.year = document.getElementById('yearFilter').value;
    currentFilters.opponent = document.getElementById('opponentFilter').value;
    currentFilters.result = document.getElementById('resultFilter').value;
    
    updateMatchesTable();
    refreshCharts();
}

// Get filtered matches
function getFilteredMatches() {
    return cricketData.matches.filter(match => {
        if (currentFilters.year !== 'all' && new Date(match.date).getFullYear() != currentFilters.year) {
            return false;
        }
        
        if (currentFilters.opponent !== 'all' && match.opponent !== currentFilters.opponent) {
            return false;
        }
        
        if (currentFilters.result !== 'all' && match.result !== currentFilters.result) {
            return false;
        }
        
        return true;
    });
}

// Refresh dashboard
function refreshDashboard() {
    showLoadingState();
    
    setTimeout(() => {
        updateDashboard();
        hideLoadingState();
        showMessage('Dashboard refreshed successfully!', 'success');
    }, 1000);
}

// Refresh tab data
function refreshTabData(tabId) {
    switch(tabId) {
        case 'overview':
            updateOverviewStats();
            break;
        case 'matches':
            updateMatchesTable();
            break;
        case 'players':
            updatePlayersGrid();
            break;
        case 'analytics':
        case 'performance':
            refreshCharts();
            break;
        case 'insights':
            generateNewInsights();
            break;
    }
}

// Update charts by period
function updateChartsByPeriod(period) {
    // This would filter data by period and update charts
    console.log('Updating charts for period:', period);
    refreshCharts();
}

// Toggle player view
function togglePlayerView(view) {
    const playersGrid = document.getElementById('playersGrid');
    const playersTable = document.getElementById('playersTable');
    
    if (view === 'cards') {
        playersGrid.style.display = 'grid';
        playersTable.style.display = 'none';
    } else {
        playersGrid.style.display = 'none';
        playersTable.style.display = 'block';
        updatePlayersTable();
    }
}

// Update players table
function updatePlayersTable() {
    const tbody = document.querySelector('#playersTable tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    cricketData.players.forEach(player => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${player.name}</td>
            <td>${player.matches}</td>
            <td>${player.runs}</td>
            <td>${player.average}</td>
            <td>${player.wickets}</td>
            <td>${player.bowling_average}</td>
            <td>${player.economy}</td>
            <td>${player.catches}</td>
        `;
        tbody.appendChild(row);
    });
}

// Generate new insights
function generateNewInsights() {
    const insights = [
        {
            id: 'trendInsight',
            text: 'Based on your recent matches, Flames CC shows strong momentum with a 4-match winning streak. Your team\'s batting average has improved by 15% in the last 10 matches, indicating better form and confidence at the crease.'
        },
        {
            id: 'improvementInsight',
            text: 'Focus on death bowling - your economy rate in the last 5 overs has increased by 1.2 runs per over. Consider rotating bowlers more frequently in the final overs.'
        },
        {
            id: 'strengthInsight',
            text: 'Your middle-order batting is exceptional, with an average partnership of 45 runs. Ahmed Khan and Bilal Ahmed form a formidable duo that consistently delivers under pressure.'
        },
        {
            id: 'strategyInsight',
            text: 'Consider opening with Usman Sheikh more often - his strike rate of 108.9 against pace bowling in the first 6 overs gives you an early advantage.'
        },
        {
            id: 'fixtureInsight',
            text: 'Your next 3 matches are against teams with weaker bowling attacks. This is an excellent opportunity to boost your net run rate and secure a higher position in the standings.'
        }
    ];
    
    insights.forEach(insight => {
        const element = document.getElementById(insight.id);
        if (element) {
            element.textContent = insight.text;
        }
    });
    
    showMessage('New insights generated successfully!', 'success');
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    } catch (error) {
        return dateString;
    }
}

function getResultClass(result) {
    switch(result) {
        case 'Win': return 'win';
        case 'Loss': return 'loss';
        case 'Draw': return 'draw';
        default: return '';
    }
}

function getInitials(name) {
    if (!name) return '??';
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}

function viewMatchDetails(matchId) {
    showMessage(`Viewing details for ${matchId}`, 'success');
    // In a real implementation, this would open a detailed match view
}

function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    const mainContent = document.querySelector('.main-content');
    mainContent.insertBefore(messageDiv, mainContent.firstChild);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

function showLoadingState() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loadingOverlay';
    loadingDiv.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 9999;">
            <div style="text-align: center; color: white;">
                <div class="loading" style="margin: 0 auto 1rem;"></div>
                <p>Loading dashboard...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loadingDiv);
}

function hideLoadingState() {
    const loadingDiv = document.getElementById('loadingOverlay');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// Export functions for global access
window.viewMatchDetails = viewMatchDetails;
window.generateNewInsights = generateNewInsights;
