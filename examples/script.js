/* ===============================================
   Trainable ChatBot Builder - JavaScript Logic
   =============================================== */

class ChatBotBuilder {
    constructor() {
        this.intents = [];
        this.trainedModel = null;
        this.chatbotName = 'My ChatBot';
        this.messageHistory = [];
        this.threshold = 0.5;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadFromStorage();
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

    switchTab(btn) {
        // Deactivate all tabs
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

        // Activate selected tab
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
            document.getElementById('utterances').value = intent.utterances.join('\n');
            document.getElementById('responses').value = intent.responses.join('\n');
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

    addIntent(e) {
        e.preventDefault();

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

        const form = document.getElementById('intent-form');
        const editIndex = form.dataset.editIndex;

        if (editIndex !== undefined) {
            this.intents[parseInt(editIndex)] = { name, description, utterances, responses };
            this.showAlert('Intent updated successfully!');
        } else {
            this.intents.push({ name, description, utterances, responses });
            this.showAlert('Intent added successfully!');
        }

        this.renderIntents();
        this.updateStats();
        this.saveToStorage();
        this.closeIntentModal();
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
                        <div class="intent-field-label">Utterances (${intent.utterances.length})</div>
                        <div class="intent-field-content">
                            ${intent.utterances.slice(0, 3).map(u => 
                                `<span class="tag">${this.escapeHtml(u)}</span>`
                            ).join('')}
                            ${intent.utterances.length > 3 ? `<span class="tag">+${intent.utterances.length - 3}</span>` : ''}
                        </div>
                    </div>
                    <div class="intent-field">
                        <div class="intent-field-label">Responses (${intent.responses.length})</div>
                        <div class="intent-field-content">
                            ${intent.responses.slice(0, 3).map(r => 
                                `<span class="tag">${this.escapeHtml(r.substring(0, 15))}...</span>`
                            ).join('')}
                            ${intent.responses.length > 3 ? `<span class="tag">+${intent.responses.length - 3}</span>` : ''}
                        </div>
                    </div>
                </div>
                ${intent.description ? `<p style="color: #6b7280; font-size: 0.9rem; margin-top: 1rem;">${this.escapeHtml(intent.description)}</p>` : ''}
            </div>
        `).join('');
    }

    deleteIntent(index) {
        if (confirm('Are you sure you want to delete this intent?')) {
            this.intents.splice(index, 1);
            this.renderIntents();
            this.updateStats();
            this.saveToStorage();
            this.showAlert('Intent deleted!');
        }
    }

    updateStats() {
        const totalIntents = this.intents.length;
        const totalUtterances = this.intents.reduce((sum, i) => sum + i.utterances.length, 0);

        document.getElementById('intent-count').textContent = totalIntents;
        document.getElementById('utterance-count').textContent = totalUtterances;
    }

    trainModel() {
        if (this.intents.length === 0) {
            this.showAlert('Please add at least one intent first', 'error');
            return;
        }

        const modal = document.getElementById('training-modal');
        modal.style.display = 'flex';

        // Simulate training
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

        // Add user message
        this.addMessageToChat(message, 'user');
        input.value = '';

        // Find best matching intent
        const best = this.findBestIntent(message);

        // Add bot response
        setTimeout(() => {
            if (best && best.score >= this.threshold) {
                const response = best.intent.responses[
                    Math.floor(Math.random() * best.intent.responses.length)
                ];
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
            const scores = intent.utterances.map(utterance => {
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

    showStats() {
        const stats = {
            'Total Intents': this.intents.length,
            'Total Utterances': this.intents.reduce((sum, i) => sum + i.utterances.length, 0),
            'Total Responses': this.intents.reduce((sum, i) => sum + i.responses.length, 0),
            'Avg Utterances/Intent': Math.round(
                this.intents.reduce((sum, i) => sum + i.utterances.length, 0) / Math.max(this.intents.length, 1)
            ),
            'Model Trained': this.trainedModel ? 'Yes' : 'No'
        };

        const statsGrid = document.getElementById('stats-grid');
        statsGrid.innerHTML = Object.entries(stats).map(([label, value]) => `
            <div class="stat-card">
                <div class="stat-card-value">${value}</div>
                <div class="stat-card-label">${label}</div>
            </div>
        `).join('');

        document.getElementById('stats-container').style.display = 'block';
        this.showAlert('Statistics updated!');
    }

    exportJSON() {
        const data = {
            metadata: {
                name: document.getElementById('chatbot-name').value || this.chatbotName,
                description: document.getElementById('chatbot-desc').value,
                version: '1.0.0',
                created_date: new Date().toISOString()
            },
            intents: this.intents.map(i => ({
                intent_id: i.name.toLowerCase().replace(/\s+/g, '_'),
                intent_name: i.name,
                description: i.description,
                utterances: i.utterances,
                responses: i.responses
            })),
            statistics: {
                total_intents: this.intents.length,
                total_utterances: this.intents.reduce((sum, i) => sum + i.utterances.length, 0)
            }
        };

        const dataStr = JSON.stringify(data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `chatbot_${Date.now()}.json`;
        link.click();

        this.showAlert('Dataset exported successfully!');
    }

    importJSON(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);

                if (data.intents) {
                    this.intents = data.intents.map(i => ({
                        name: i.intent_name || i.name,
                        description: i.description || '',
                        utterances: Array.isArray(i.utterances) ? i.utterances : [],
                        responses: Array.isArray(i.responses) ? i.responses : []
                    }));

                    this.renderIntents();
                    this.updateStats();
                    this.saveToStorage();
                    this.showAlert('Dataset imported successfully!');
                }
            } catch (error) {
                this.showAlert('Invalid JSON file', 'error');
            }
        };
        reader.readAsText(file);
    }

    clearData() {
        if (confirm('Are you sure? This will delete all intents and cannot be undone.')) {
            this.intents = [];
            this.trainedModel = null;
            this.renderIntents();
            this.updateStats();
            localStorage.removeItem('chatbot_intents');
            this.showAlert('All data cleared!');
        }
    }

    saveToStorage() {
        localStorage.setItem('chatbot_intents', JSON.stringify(this.intents));
    }

    loadFromStorage() {
        const saved = localStorage.getItem('chatbot_intents');
        if (saved) {
            this.intents = JSON.parse(saved);
            this.renderIntents();
            this.updateStats();
        }
    }

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
    window.builder = new ChatBotBuilder();
});
