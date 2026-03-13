/* ===============================================
   Updated Script for API Backend
   Replaces localStorage with API calls
   =============================================== */

class ChatBotBuilder {
    constructor(apiUrl = 'http://localhost:5000/api') {
        this.apiUrl = apiUrl;
        this.currentChatbot = null;
        this.intents = [];
        this.trainedModel = null;
        this.messageHistory = [];
        this.threshold = 0.5;

        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadChatbots();
        this.updateStats();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.closest('.nav-btn')));
        });

        // Intent Management
        document.getElementById('add-intent-btn').addEventListener('click', () => this.openIntentModal());
        document.getElementById('intent-form').addEventListener('submit', (e) => this.addIntent(e));
        document.getElementById('cancel-btn').addEventListener('click', () => this.closeIntentModal());
        document.getElementById('close-modal').addEventListener('click', () => this.closeIntentModal());

        // Chat
        document.getElementById('send-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('user-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Export/Import
        document.getElementById('export-json-btn').addEventListener('click', () => this.exportJSON());
        document.getElementById('export-stats-btn').addEventListener('click', () => this.showStats());
        document.getElementById('import-btn').addEventListener('click', () => {
            document.getElementById('import-file').click();
        });
        document.getElementById('import-file').addEventListener('change', (e) => this.importJSON(e));

        // Settings
        document.getElementById('threshold').addEventListener('input', (e) => {
            document.getElementById('threshold-value').textContent = e.target.value;
            this.threshold = parseFloat(e.target.value);
        });
        document.getElementById('clear-btn').addEventListener('click', () => this.clearData());

        // Training
        document.getElementById('train-btn').addEventListener('click', () => this.trainModel());

        // Close modal on outside click
        document.getElementById('intent-modal').addEventListener('click', (e) => {
            if (e.target.id === 'intent-modal') this.closeIntentModal();
        });
    }

    // ===============================================
    // Chatbot Management
    // ===============================================

    async loadChatbots() {
        try {
            const response = await fetch(`${this.apiUrl}/chatbots`);
            const chatbots = await response.json();
            
            if (chatbots.length > 0) {
                this.currentChatbot = chatbots[0];
                await this.loadChatbot(this.currentChatbot.id);
            }
        } catch (error) {
            console.error('Error loading chatbots:', error);
            this.showAlert('Error loading chatbots', 'error');
        }
    }

    async loadChatbot(chatbotId) {
        try {
            const response = await fetch(`${this.apiUrl}/chatbots/${chatbotId}`);
            const chatbot = await response.json();
            
            this.currentChatbot = chatbot;
            this.intents = chatbot.intents || [];
            this.renderIntents();
            this.updateStats();
        } catch (error) {
            console.error('Error loading chatbot:', error);
            this.showAlert('Error loading chatbot', 'error');
        }
    }

    async createChatbot() {
        try {
            const name = document.getElementById('chatbot-name').value || 'My ChatBot';
            const description = document.getElementById('chatbot-desc').value || '';

            const response = await fetch(`${this.apiUrl}/chatbots`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, description })
            });

            if (response.ok) {
                const chatbot = await response.json();
                this.currentChatbot = chatbot;
                this.intents = [];
                this.renderIntents();
                this.updateStats();
                this.showAlert('Chatbot created successfully!');
            } else {
                const error = await response.json();
                this.showAlert(error.error || 'Error creating chatbot', 'error');
            }
        } catch (error) {
            console.error('Error creating chatbot:', error);
            this.showAlert('Error creating chatbot', 'error');
        }
    }

    // ===============================================
    // UI Navigation
    // ===============================================

    switchTab(btn) {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

        btn.classList.add('active');
        const tabName = btn.dataset.tab;
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    openIntentModal(index = null) {
        const modal = document.getElementById('intent-modal');
        const form = document.getElementById('intent-form');
        const title = document.getElementById('modal-title');

        if (index !== null) {
            title.textContent = 'Edit Intent';
            const intent = this.intents[index];
            document.getElementById('intent-name').value = intent.name;
            document.getElementById('intent-desc').value = intent.description || '';
            document.getElementById('utterances').value = intent.utterances
                .map(u => typeof u === 'string' ? u : u.text)
                .join('\n');
            document.getElementById('responses').value = intent.responses
                .map(r => typeof r === 'string' ? r : r.text)
                .join('\n');
            form.dataset.editIndex = index;
        } else {
            title.textContent = 'Add Intent';
            form.reset();
            delete form.dataset.editIndex;
        }

        modal.style.display = 'flex';
    }

    closeIntentModal() {
        document.getElementById('intent-modal').style.display = 'none';
        document.getElementById('intent-form').reset();
    }

    // ===============================================
    // Intent Management
    // ===============================================

    async addIntent(e) {
        e.preventDefault();

        if (!this.currentChatbot) {
            this.showAlert('Please create a chatbot first', 'error');
            return;
        }

        const name = document.getElementById('intent-name').value.trim();
        const description = document.getElementById('intent-desc').value.trim();
        const utterances = document.getElementById('utterances').value
            .split('\n')
            .map(u => u.trim())
            .filter(u => u);
        const responses = document.getElementById('responses').value
            .split('\n')
            .map(r => r.trim())
            .filter(r => r);

        if (!name || utterances.length === 0 || responses.length === 0) {
            this.showAlert('Please fill in all fields', 'error');
            return;
        }

        try {
            const form = document.getElementById('intent-form');
            const editIndex = form.dataset.editIndex;

            if (editIndex !== undefined) {
                // Update existing intent
                const intent = this.intents[parseInt(editIndex)];
                const response = await fetch(`${this.apiUrl}/intents/${intent.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name,
                        description,
                        utterances,
                        responses
                    })
                });

                if (response.ok) {
                    await this.loadChatbot(this.currentChatbot.id);
                    this.showAlert('Intent updated successfully!');
                } else {
                    this.showAlert('Error updating intent', 'error');
                }
            } else {
                // Create new intent
                const response = await fetch(`${this.apiUrl}/chatbots/${this.currentChatbot.id}/intents`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name,
                        description,
                        utterances,
                        responses
                    })
                });

                if (response.ok) {
                    await this.loadChatbot(this.currentChatbot.id);
                    this.showAlert('Intent added successfully!');
                } else {
                    const error = await response.json();
                    this.showAlert(error.error || 'Error adding intent', 'error');
                }
            }

            this.closeIntentModal();
        } catch (error) {
            console.error('Error managing intent:', error);
            this.showAlert('Error managing intent', 'error');
        }
    }

    async deleteIntent(index) {
        if (confirm('Are you sure you want to delete this intent?')) {
            try {
                const intent = this.intents[index];
                const response = await fetch(`${this.apiUrl}/intents/${intent.id}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await this.loadChatbot(this.currentChatbot.id);
                    this.showAlert('Intent deleted!');
                } else {
                    this.showAlert('Error deleting intent', 'error');
                }
            } catch (error) {
                console.error('Error deleting intent:', error);
                this.showAlert('Error deleting intent', 'error');
            }
        }
    }

    renderIntents() {
        const container = document.getElementById('intents-list');

        if (this.intents.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No intents yet. Create your first one!</p></div>';
            return;
        }

        container.innerHTML = this.intents.map((intent, index) => `
            <div class="intent-card">
                <div class="intent-card-header">
                    <div class="intent-card-title">${this.escapeHtml(intent.name)}</div>
                    <div class="intent-card-actions">
                        <button class="btn btn-primary btn-sm" onclick="builder.openIntentModal(${index})">
                            Edit
                        </button>
                        <button class="btn btn-danger btn-sm" onclick="builder.deleteIntent(${index})">
                            Delete
                        </button>
                    </div>
                </div>
                <div class="intent-card-content">
                    <div class="intent-field">
                        <div class="intent-field-label">Utterances (${this.getUtteranceCount(intent)})</div>
                        <div class="intent-field-content">
                            ${this.getUtterances(intent).slice(0, 3).map(u => 
                                `<span class="tag">${this.escapeHtml(u)}</span>`
                            ).join('')}
                            ${this.getUtteranceCount(intent) > 3 ? `<span class="tag">+${this.getUtteranceCount(intent) - 3}</span>` : ''}
                        </div>
                    </div>
                    <div class="intent-field">
                        <div class="intent-field-label">Responses (${this.getResponseCount(intent)})</div>
                        <div class="intent-field-content">
                            ${this.getResponses(intent).slice(0, 3).map(r => 
                                `<span class="tag">${this.escapeHtml(r.substring(0, 15))}...</span>`
                            ).join('')}
                            ${this.getResponseCount(intent) > 3 ? `<span class="tag">+${this.getResponseCount(intent) - 3}</span>` : ''}
                        </div>
                    </div>
                </div>
                ${intent.description ? `<p style="color: #6b7280; font-size: 0.9rem; margin-top: 1rem;">${this.escapeHtml(intent.description)}</p>` : ''}
            </div>
        `).join('');
    }

    getUtterances(intent) {
        return (intent.utterances || []).map(u => typeof u === 'string' ? u : u.text);
    }

    getUtteranceCount(intent) {
        return (intent.utterances || []).length;
    }

    getResponses(intent) {
        return (intent.responses || []).map(r => typeof r === 'string' ? r : r.text);
    }

    getResponseCount(intent) {
        return (intent.responses || []).length;
    }

    updateStats() {
        const totalIntents = this.intents.length;
        const totalUtterances = this.intents.reduce((sum, i) => sum + this.getUtteranceCount(i), 0);

        document.getElementById('intent-count').textContent = totalIntents;
        document.getElementById('utterance-count').textContent = totalUtterances;
    }

    // ===============================================
    // Training & Chat
    // ===============================================

    trainModel() {
        if (this.intents.length === 0) {
            this.showAlert('Please add at least one intent first', 'error');
            return;
        }

        const modal = document.getElementById('training-modal');
        modal.style.display = 'flex';

        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 100) progress = 100;

            const fill = document.getElementById('progress-fill');
            fill.style.width = progress + '%';

            document.getElementById('training-status').textContent = 
                `Training model... ${Math.floor(progress)}%`;

            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    this.trainedModel = this.intents;
                    document.getElementById('send-btn').disabled = false;
                    document.getElementById('user-input').disabled = false;
                    modal.style.display = 'none';
                    this.showAlert('Model trained successfully!');
                }, 500);
            }
        }, 300);
    }

    sendMessage() {
        const input = document.getElementById('user-input');
        const message = input.value.trim();

        if (!message) return;

        if (!this.trainedModel) {
            this.showAlert('Please train a model first', 'error');
            return;
        }

        this.addMessageToChat(message, 'user');
        input.value = '';

        const best = this.findBestIntent(message);

        setTimeout(() => {
            if (best && best.score >= this.threshold) {
                const responses = this.getResponses(best.intent);
                const response = responses[Math.floor(Math.random() * responses.length)];
                this.addMessageToChat(response, 'bot');
            } else {
                this.addMessageToChat('Sorry, I didn\'t understand that. Can you rephrase?', 'bot');
            }
        }, 500);
    }

    findBestIntent(userInput) {
        if (!this.trainedModel) return null;

        const input = userInput.toLowerCase().split(/\s+/);
        let bestIntent = null;
        let bestScore = 0;

        this.trainedModel.forEach(intent => {
            const utterances = this.getUtterances(intent);
            const scores = utterances.map(utterance => {
                const uWords = utterance.toLowerCase().split(/\s+/);
                const matches = input.filter(word => uWords.includes(word)).length;
                return matches / Math.max(input.length, uWords.length);
            });

            const maxScore = Math.max(...scores);
            if (maxScore > bestScore) {
                bestScore = maxScore;
                bestIntent = intent;
            }
        });

        return bestIntent ? { intent: bestIntent, score: bestScore } : null;
    }

    addMessageToChat(message, sender) {
        const container = document.getElementById('chat-messages');
        const msgEl = document.createElement('div');
        msgEl.className = `message ${sender}-message`;
        msgEl.innerHTML = `<p>${this.escapeHtml(message)}</p>`;
        container.appendChild(msgEl);
        container.scrollTop = container.scrollHeight;
    }

    // ===============================================
    // Export/Import
    // ===============================================

    async showStats() {
        if (!this.currentChatbot) {
            this.showAlert('No chatbot loaded', 'error');
            return;
        }

        try {
            const response = await fetch(`${this.apiUrl}/chatbots/${this.currentChatbot.id}/export`);
            const data = await response.json();

            const stats = data.statistics;
            const statsGrid = document.getElementById('stats-grid');
            statsGrid.innerHTML = Object.entries(stats).map(([label, value]) => `
                <div class="stat-card">
                    <div class="stat-card-value">${value}</div>
                    <div class="stat-card-label">${label.replace(/_/g, ' ')}</div>
                </div>
            `).join('');

            document.getElementById('stats-container').style.display = 'block';
            this.showAlert('Statistics loaded!');
        } catch (error) {
            console.error('Error loading stats:', error);
            this.showAlert('Error loading statistics', 'error');
        }
    }

    async exportJSON() {
        if (!this.currentChatbot) {
            this.showAlert('No chatbot loaded', 'error');
            return;
        }

        try {
            const response = await fetch(`${this.apiUrl}/chatbots/${this.currentChatbot.id}/export`);
            const data = await response.json();

            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `chatbot_${this.currentChatbot.id}_${Date.now()}.json`;
            link.click();

            this.showAlert('Dataset exported successfully!');
        } catch (error) {
            console.error('Error exporting:', error);
            this.showAlert('Error exporting dataset', 'error');
        }
    }

    async importJSON(e) {
        const file = e.target.files[0];
        if (!file || !this.currentChatbot) return;

        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                const data = JSON.parse(event.target.result);

                const response = await fetch(`${this.apiUrl}/chatbots/${this.currentChatbot.id}/import`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    await this.loadChatbot(this.currentChatbot.id);
                    this.showAlert('Dataset imported successfully!');
                } else {
                    this.showAlert('Error importing dataset', 'error');
                }
            } catch (error) {
                this.showAlert('Invalid JSON file', 'error');
            }
        };
        reader.readAsText(file);
    }

    async clearData() {
        if (confirm('Are you sure? This will delete all intents and cannot be undone.')) {
            try {
                // Delete all intents
                for (const intent of this.intents) {
                    await fetch(`${this.apiUrl}/intents/${intent.id}`, {
                        method: 'DELETE'
                    });
                }

                this.intents = [];
                this.trainedModel = null;
                this.renderIntents();
                this.updateStats();
                this.showAlert('All data cleared!');
            } catch (error) {
                console.error('Error clearing data:', error);
                this.showAlert('Error clearing data', 'error');
            }
        }
    }

    // ===============================================
    // Utilities
    // ===============================================

    showAlert(message, type = 'success') {
        const alert = document.getElementById('alert');
        alert.textContent = message;
        alert.className = `alert ${type}`;
        alert.style.display = 'block';

        setTimeout(() => {
            alert.style.display = 'none';
        }, 3000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = window.location.hostname === 'localhost' 
        ? 'http://localhost:5000/api'
        : '/api';
    
    window.builder = new ChatBotBuilder(apiUrl);
});
