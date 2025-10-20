// Squad Management System

class SquadManager {
    constructor() {
        this.squadData = null;
        this.init();
    }

    async init() {
        await this.loadSquad();
        this.setupEventListeners();
        this.renderSquad();
    }

    async loadSquad() {
        try {
            const response = await fetch('flames_squad.json');
            this.squadData = await response.json();
        } catch (error) {
            console.error('Error loading squad:', error);
            // Initialize with empty squad if file doesn't exist
            this.squadData = {
                team_name: "Flames CC",
                squad: [],
                name_mapping: {},
                notes: {
                    last_updated: new Date().toISOString().split('T')[0],
                    total_players: 0,
                    active_squad: true
                }
            };
        }
    }

    setupEventListeners() {
        // Save Squad button
        document.getElementById('saveSquadBtn')?.addEventListener('click', () => {
            this.saveSquadToLocalStorage();
        });

        // Export Squad button
        document.getElementById('exportSquadBtn')?.addEventListener('click', () => {
            this.exportSquad();
        });

        // Add Player button
        document.getElementById('addPlayerBtn')?.addEventListener('click', () => {
            this.showAddPlayerForm();
        });
    }

    renderSquad() {
        if (!this.squadData || !this.squadData.squad) return;

        const squadGrid = document.getElementById('squadGrid');
        if (!squadGrid) return;

        // Update summary stats
        this.updateSquadStats();

        // Clear existing cards
        squadGrid.innerHTML = '';

        // Render each player card
        this.squadData.squad.forEach(player => {
            const card = this.createPlayerCard(player);
            squadGrid.appendChild(card);
        });
    }

    updateSquadStats() {
        const squad = this.squadData.squad || [];
        
        // Count by role
        const batsmen = squad.filter(p => p.role === 'Batsman').length;
        const bowlers = squad.filter(p => p.role === 'Bowler').length;
        const allrounders = squad.filter(p => p.role === 'All-rounder').length;
        const wicketkeepers = squad.filter(p => p.role === 'Wicketkeeper').length;

        document.getElementById('totalPlayers').textContent = squad.length;
        document.getElementById('totalBatsmen').textContent = batsmen + wicketkeepers;
        document.getElementById('totalBowlers').textContent = bowlers;
        document.getElementById('totalAllrounders').textContent = allrounders;
    }

    createPlayerCard(player) {
        const card = document.createElement('div');
        card.className = 'squad-player-card';
        
        if (player.is_captain) {
            card.classList.add('captain');
        }
        if (player.is_wicketkeeper) {
            card.classList.add('wicketkeeper');
        }

        card.innerHTML = `
            ${player.is_captain ? '<div class="captain-badge"><i class="fas fa-star"></i> Captain</div>' : ''}
            ${player.is_wicketkeeper && !player.is_captain ? '<div class="wk-badge"><i class="fas fa-glove"></i> WK</div>' : ''}
            
            <div class="player-id-badge">${player.player_id}</div>
            <h3>${player.full_name}</h3>
            <div class="player-role">${player.role}</div>
            
            <div class="player-details">
                <div class="detail-row">
                    <span class="detail-label">Batting Style</span>
                    <span class="detail-value">${player.batting_style || 'Not specified'}</span>
                </div>
                ${player.bowling_style ? `
                <div class="detail-row">
                    <span class="detail-label">Bowling Style</span>
                    <span class="detail-value">${player.bowling_style}</span>
                </div>
                ` : ''}
            </div>

            <div class="name-variations">
                <h4>Known As:</h4>
                <div>
                    ${player.common_names.map(name => `<span class="name-tag">${name}</span>`).join('')}
                </div>
            </div>

            <div class="player-actions">
                <button class="btn-edit" onclick="squadManager.editPlayer('${player.player_id}')">
                    <i class="fas fa-edit"></i> Edit
                </button>
            </div>
        `;

        return card;
    }

    editPlayer(playerId) {
        const player = this.squadData.squad.find(p => p.player_id === playerId);
        if (!player) return;

        const card = document.querySelector(`[data-player-id="${playerId}"]`)?.closest('.squad-player-card');
        if (!card) {
            // Find card by player ID in the grid
            const cards = document.querySelectorAll('.squad-player-card');
            cards.forEach(c => {
                if (c.innerHTML.includes(playerId)) {
                    this.showEditForm(c, player);
                }
            });
        }
    }

    showEditForm(card, player) {
        card.innerHTML = `
            <div class="player-id-badge">${player.player_id}</div>
            <h3>Edit Player</h3>
            
            <form class="player-edit-form" onsubmit="event.preventDefault(); squadManager.savePlayer('${player.player_id}', this);">
                <div class="form-group">
                    <label>Full Name *</label>
                    <input type="text" name="full_name" value="${player.full_name}" required>
                </div>

                <div class="form-group">
                    <label>Common Names (comma-separated) *</label>
                    <textarea name="common_names" required>${player.common_names.join(', ')}</textarea>
                </div>

                <div class="form-group">
                    <label>Role *</label>
                    <select name="role" required>
                        <option value="Batsman" ${player.role === 'Batsman' ? 'selected' : ''}>Batsman</option>
                        <option value="Bowler" ${player.role === 'Bowler' ? 'selected' : ''}>Bowler</option>
                        <option value="All-rounder" ${player.role === 'All-rounder' ? 'selected' : ''}>All-rounder</option>
                        <option value="Wicketkeeper" ${player.role === 'Wicketkeeper' ? 'selected' : ''}>Wicketkeeper</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Batting Style</label>
                    <select name="batting_style">
                        <option value="">Select...</option>
                        <option value="Right-hand bat" ${player.batting_style === 'Right-hand bat' ? 'selected' : ''}>Right-hand bat</option>
                        <option value="Left-hand bat" ${player.batting_style === 'Left-hand bat' ? 'selected' : ''}>Left-hand bat</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Bowling Style</label>
                    <input type="text" name="bowling_style" value="${player.bowling_style || ''}" 
                           placeholder="e.g., Right-arm medium, Left-arm spin">
                </div>

                <div class="checkbox-group">
                    <div class="checkbox-wrapper">
                        <input type="checkbox" name="is_captain" id="cap_${player.player_id}" 
                               ${player.is_captain ? 'checked' : ''}>
                        <label for="cap_${player.player_id}">Captain</label>
                    </div>
                    <div class="checkbox-wrapper">
                        <input type="checkbox" name="is_wicketkeeper" id="wk_${player.player_id}" 
                               ${player.is_wicketkeeper ? 'checked' : ''}>
                        <label for="wk_${player.player_id}">Wicketkeeper</label>
                    </div>
                </div>

                <div class="player-actions">
                    <button type="submit" class="btn-save">
                        <i class="fas fa-save"></i> Save
                    </button>
                    <button type="button" class="btn-cancel" onclick="squadManager.renderSquad()">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                </div>
            </form>
        `;
    }

    savePlayer(playerId, form) {
        const formData = new FormData(form);
        
        const playerIndex = this.squadData.squad.findIndex(p => p.player_id === playerId);
        if (playerIndex === -1) return;

        // Update player data
        const commonNames = formData.get('common_names').split(',').map(n => n.trim());
        
        this.squadData.squad[playerIndex] = {
            ...this.squadData.squad[playerIndex],
            full_name: formData.get('full_name'),
            common_names: commonNames,
            role: formData.get('role'),
            batting_style: formData.get('batting_style') || null,
            bowling_style: formData.get('bowling_style') || null,
            is_captain: formData.get('is_captain') === 'on',
            is_wicketkeeper: formData.get('is_wicketkeeper') === 'on'
        };

        // Update name mapping
        this.updateNameMapping();

        // Re-render
        this.renderSquad();
        
        // Show success message
        this.showMessage('Player updated successfully!', 'success');
    }

    updateNameMapping() {
        this.squadData.name_mapping = {};
        this.squadData.squad.forEach(player => {
            player.common_names.forEach(name => {
                this.squadData.name_mapping[name] = player.player_id;
            });
        });
    }

    showAddPlayerForm() {
        // Create modal with add player form
        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.id = 'addPlayerModal';
        
        // Generate new player ID
        const existingIds = this.squadData.squad.map(p => parseInt(p.player_id.replace('P', '')));
        const newId = `P${String(Math.max(...existingIds, 0) + 1).padStart(3, '0')}`;

        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i class="fas fa-user-plus"></i> Add New Player</h2>
                    <button class="close-modal" onclick="document.getElementById('addPlayerModal').remove()">×</button>
                </div>

                <form class="player-edit-form" onsubmit="event.preventDefault(); squadManager.addNewPlayer(this);">
                    <input type="hidden" name="player_id" value="${newId}">
                    
                    <div class="form-group">
                        <label>Player ID</label>
                        <input type="text" value="${newId}" disabled>
                    </div>

                    <div class="form-group">
                        <label>Full Name *</label>
                        <input type="text" name="full_name" required placeholder="e.g., Muhammad Azhar">
                    </div>

                    <div class="form-group">
                        <label>Common Names (comma-separated) *</label>
                        <textarea name="common_names" required placeholder="e.g., Azhar, M.Azhar, Muhammad Azhar"></textarea>
                    </div>

                    <div class="form-group">
                        <label>Role *</label>
                        <select name="role" required>
                            <option value="">Select Role...</option>
                            <option value="Batsman">Batsman</option>
                            <option value="Bowler">Bowler</option>
                            <option value="All-rounder">All-rounder</option>
                            <option value="Wicketkeeper">Wicketkeeper</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Batting Style</label>
                        <select name="batting_style">
                            <option value="">Select...</option>
                            <option value="Right-hand bat">Right-hand bat</option>
                            <option value="Left-hand bat">Left-hand bat</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Bowling Style</label>
                        <input type="text" name="bowling_style" placeholder="e.g., Right-arm medium, Left-arm spin">
                    </div>

                    <div class="checkbox-group">
                        <div class="checkbox-wrapper">
                            <input type="checkbox" name="is_captain" id="new_cap">
                            <label for="new_cap">Captain</label>
                        </div>
                        <div class="checkbox-wrapper">
                            <input type="checkbox" name="is_wicketkeeper" id="new_wk">
                            <label for="new_wk">Wicketkeeper</label>
                        </div>
                    </div>

                    <div class="player-actions">
                        <button type="submit" class="btn-save">
                            <i class="fas fa-plus"></i> Add Player
                        </button>
                        <button type="button" class="btn-cancel" onclick="document.getElementById('addPlayerModal').remove()">
                            <i class="fas fa-times"></i> Cancel
                        </button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);
    }

    addNewPlayer(form) {
        const formData = new FormData(form);
        
        const newPlayer = {
            player_id: formData.get('player_id'),
            full_name: formData.get('full_name'),
            common_names: formData.get('common_names').split(',').map(n => n.trim()),
            role: formData.get('role'),
            batting_style: formData.get('batting_style') || null,
            bowling_style: formData.get('bowling_style') || null,
            is_captain: formData.get('is_captain') === 'on',
            is_wicketkeeper: formData.get('is_wicketkeeper') === 'on'
        };

        this.squadData.squad.push(newPlayer);
        this.updateNameMapping();
        this.squadData.notes.total_players = this.squadData.squad.length;
        
        document.getElementById('addPlayerModal').remove();
        this.renderSquad();
        this.showMessage('New player added successfully!', 'success');
    }

    saveSquadToLocalStorage() {
        this.squadData.notes.last_updated = new Date().toISOString().split('T')[0];
        localStorage.setItem('flames_squad', JSON.stringify(this.squadData));
        this.showMessage('Squad saved to browser storage!', 'success');
    }

    exportSquad() {
        this.squadData.notes.last_updated = new Date().toISOString().split('T')[0];
        
        const dataStr = JSON.stringify(this.squadData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'flames_squad.json';
        link.click();
        
        this.showMessage('Squad exported successfully!', 'success');
    }

    showMessage(text, type) {
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        
        const squadGrid = document.getElementById('squadGrid');
        squadGrid.parentNode.insertBefore(message, squadGrid);
        
        setTimeout(() => message.remove(), 3000);
    }
}

// Initialize squad manager when DOM is loaded
let squadManager;
document.addEventListener('DOMContentLoaded', () => {
    squadManager = new SquadManager();
});

