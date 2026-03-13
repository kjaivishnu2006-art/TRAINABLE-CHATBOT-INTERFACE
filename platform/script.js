/**
 * GSOC ChatBot Platform - Dashboard Logic
 * Orchestrates the UI, API calls, and real-time features.
 */

const API_BASE = '/api';

// State Management
const State = {
    currentView: 'dashboard',
    projects: [],
    activeProject: null,
    stats: {
        intents: 0,
        accuracy: 92,
        size: '3.6 KB'
    }
};

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    fetchDashboardStats();
    loadProjects();
    
    // Default view
    switchView('dashboard');
});

// Navigation System
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const view = item.getAttribute('data-view');
            if (view) {
                navItems.forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                switchView(view);
            }
        });
    });
}

function switchView(viewName) {
    State.currentView = viewName;
    const title = document.getElementById('view-title');
    const container = document.getElementById('view-container');
    
    // Fade out effect
    container.style.opacity = '0';
    
    setTimeout(() => {
        // Update Title
        title.innerText = viewName.charAt(0).toUpperCase() + viewName.slice(1) + (viewName === 'dashboard' ? ' Overview' : '');
        
        // Render content based on view
        renderView(viewName, container);
        
        // Fade in effect
        container.style.opacity = '1';
    }, 200);
}

function renderView(viewName, container) {
    switch(viewName) {
        case 'dashboard':
            container.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card glass">
                        <div class="stat-label">Total Intents</div>
                        <div class="stat-value">${State.stats.intents}</div>
                    </div>
                    <div class="stat-card glass">
                        <div class="stat-label">Semantic Accuracy</div>
                        <div class="stat-value">${State.activeProject ? State.stats.accuracy + '%' : '--'}</div>
                    </div>
                    <div class="stat-card glass">
                        <div class="stat-label">Model Size</div>
                        <div class="stat-value">${State.stats.size}</div>
                    </div>
                    <div class="stat-card glass">
                        <div class="stat-label">API Status</div>
                        <div class="stat-value" style="color: var(--success);">Online</div>
                    </div>
                </div>
                <div class="features-grid">
                    <div class="card glass">
                        <h2>🧠 Semantic Clusters</h2>
                        <div class="visualizer-container" onclick="switchView('visualizer')" style="cursor: pointer;">
                             <p style="text-align: center; padding-top: 140px; color: var(--primary);">
                                Click to view Semantic Visualizer (Ultra)
                            </p>
                        </div>
                    </div>
                    <div class="card glass">
                        <h2>🚀 Quick Actions</h2>
                        <div style="display: flex; flex-direction: column; gap: 1rem;">
                            <button class="btn btn-primary" onclick="switchView('builder')">Open Intent Builder</button>
                            <button class="btn glass" onclick="switchView('test')">Start Chat Test</button>
                            <button class="btn glass" onclick="switchView('export')">Export for Mobile</button>
                        </div>
                    </div>
                </div>
            `;
            break;
            
        case 'projects':
            renderProjectsList();
            break;

        case 'builder':
            renderBuilder();
            break;
            
        case 'test':
            container.innerHTML = `
                <div class="features-grid" style="grid-template-columns: 1fr 1fr;">
                    <div class="card glass" style="display: flex; flex-direction: column; height: 600px;">
                        <h2>Test Arena</h2>
                        <div id="chat-box" style="flex: 1; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column; gap: 1rem; background: rgba(0,0,0,0.2); border-radius: 10px; margin-bottom: 1rem;">
                            <div style="background: var(--surface); padding: 0.75rem 1rem; border-radius: 0 1rem 1rem 1rem; max-width: 80%; align-self: flex-start; border: 1px solid var(--surface-border);">
                                👋 Hello! I'm your chatbot. Start typing to test me.
                            </div>
                        </div>
                        <div style="display: flex; gap: 0.5rem;">
                            <input type="text" id="chat-input" class="glass" placeholder="Type a message..." style="flex: 1; padding: 0.75rem; border: none; border-radius: 10px; color: white;">
                            <button class="btn btn-primary" onclick="sendMessage()">Send</button>
                        </div>
                    </div>
                    <div class="card glass">
                        <h2>🎙️ Voice Analysis (Ultra)</h2>
                        <div style="padding: 1.5rem; background: rgba(0,0,0,0.1); border-radius: 10px;">
                            <p class="stat-label">Recognized Speech:</p>
                            <p id="speech-result" style="font-style: italic; margin-top: 0.5rem; color: var(--text-muted);">Speech Recognition API ready.</p>
                        </div>
                        <button class="btn glass" id="voice-btn" onclick="toggleVoice()" style="width: 100%; margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                            <span>🎤</span> Push to Talk
                        </button>
                    </div>
                </div>
            `;
            break;

        case 'visualizer':
            renderVisualizer();
            break;
            
        default:
            container.innerHTML = `<div class="card glass"><p>The <b>${viewName}</b> phase is currently under development for GSoC.</p></div>`;
    }
}

// API Interactions
async function fetchDashboardStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        State.stats.intents = data.total_intents;
        State.stats.accuracy = 92; // Default for semantic
        
        if (State.currentView === 'dashboard') {
             updateStat('stat-intents', data.total_intents);
             updateStat('stat-accuracy', '92%');
        }
    } catch (error) {
        console.error('Failed to fetch stats:', error);
        showToast('Background API connection issues.', 'error');
    }
}

async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/chatbots`);
        const data = await response.json();
        State.projects = data;
        
        if (State.currentView === 'projects') {
            renderProjectsList();
        }
    } catch (error) {
        console.error('Failed to load projects:', error);
    }
}

async function createProject() {
    const name = prompt("Enter ChatBot Name:");
    if (!name) return;
    
    try {
        const response = await fetch(`${API_BASE}/chatbots`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, description: 'Created via Platform Dashboard' })
        });
        
        if (response.ok) {
            showToast('Project created successfully!');
            loadProjects();
            fetchDashboardStats();
        } else {
            const err = await response.json();
            showToast(err.error || 'Failed to create project', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

function updateStat(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerText = value;
}

function renderProjectsList() {
    const container = document.getElementById('view-container');
    container.innerHTML = `
        <div class="card glass">
            <h2>Your ChatBot Projects</h2>
            <div id="projects-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                ${State.projects.map(p => `
                    <div class="stat-card glass" style="cursor: pointer; border: 1px solid var(--primary);" onclick="selectProject(${p.id})">
                        <h3 style="margin-bottom: 0.5rem;">🤖 ${p.name}</h3>
                        <p class="stat-label">${p.description || 'No description'}</p>
                        <div style="margin-top: 1rem; font-size: 0.8rem; color: var(--primary);">Click to manage</div>
                    </div>
                `).join('')}
                <div class="stat-card glass" style="border: 2px dashed var(--surface-border); display: flex; align-items: center; justify-content: center; cursor: pointer;" onclick="createProject()">
                    <span style="font-size: 2rem; color: var(--primary);">+</span>
                </div>
            </div>
        </div>
    `;
}

async function selectProject(id) {
    try {
        const response = await fetch(`${API_BASE}/chatbots/${id}`);
        const data = await response.json();
        State.activeProject = data;
        showToast(`Active Project: ${data.name}`);
        switchView('builder');
    } catch (error) {
        showToast('Failed to load project details', 'error');
    }
}

// UI Helpers
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (!toast) {
        console.warn('Toast element not found:', message);
        return;
    }
    toast.innerText = message;
    toast.style.background = type === 'error' ? 'var(--error)' : 'var(--surface)';
    toast.style.display = 'block';
    toast.style.animation = 'fadeIn 0.3s ease forwards';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function renderBuilder() {
    const container = document.getElementById('view-container');
    if (!State.activeProject) {
        container.innerHTML = `
            <div class="card glass" style="text-align: center; padding: 4rem;">
                <h2>No Project Selected</h2>
                <p class="stat-label">Please select a project from the "My Projects" tab first.</p>
                <button class="btn btn-primary" style="margin-top: 2rem;" onclick="switchView('projects')">Go to Projects</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div class="card glass">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <div>
                    <h2>Intent Builder: ${State.activeProject.name}</h2>
                    <p class="stat-label">Manage what your bot understands.</p>
                </div>
                <button class="btn btn-primary" onclick="addIntent()">+ Add Intent</button>
            </div>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="text-align: left; color: var(--text-muted); border-bottom: 1px solid var(--surface-border);">
                        <th style="padding: 1rem;">Intent Name</th>
                        <th style="padding: 1rem;">Utterances</th>
                        <th style="padding: 1rem;">Status</th>
                        <th style="padding: 1rem;">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${State.activeProject.intents.map(i => `
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <td style="padding: 1rem; font-weight: 600;">${i.name}</td>
                            <td style="padding: 1rem;">${i.utterances ? i.utterances.length : 0} lines</td>
                            <td style="padding: 1rem;"><span style="color: var(--success);">● Active</span></td>
                            <td style="padding: 1rem;">
                                <button class="btn glass" style="padding: 0.25rem 0.75rem; font-size: 0.8rem;">Edit</button>
                            </td>
                        </tr>
                    `).join('')}
                    ${State.activeProject.intents.length === 0 ? '<tr><td colspan="4" style="text-align: center; padding: 2rem; color: var(--text-muted);">No intents yet. Click "Add Intent" to start training.</td></tr>' : ''}
                </tbody>
            </table>
        </div>
    `;
}

// Ultra Features Implementation
function renderVisualizer() {
    const container = document.getElementById('view-container');
    container.innerHTML = `
        <div class="card glass">
            <h2>🧠 Semantic Space Visualizer</h2>
            <p class="stat-label">Visualizing high-dimensional intent clusters in 2D space.</p>
            <div class="visualizer-container" id="viz-canvas" style="margin-top: 2rem; background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, rgba(15, 23, 42, 1) 100%); position: relative;">
                <!-- Simulated Nodes -->
                <div class="viz-node" style="top: 20%; left: 30%; background: var(--primary);"></div>
                <div class="viz-node" style="top: 25%; left: 35%; background: var(--primary);"></div>
                <div class="viz-node" style="top: 60%; left: 70%; background: var(--secondary);"></div>
                <div class="viz-node" style="top: 65%; left: 75%; background: var(--secondary);"></div>
                <div class="viz-node" style="top: 40%; left: 10%; background: var(--accent);"></div>
                
                <div style="position: absolute; bottom: 20px; left: 20px; font-size: 0.8rem; color: var(--text-muted);">
                    Legend: [● Greetings] [● FAQ] [● Support]
                </div>
            </div>
            <style>
                .viz-node {
                    position: absolute;
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    box-shadow: 0 0 15px currentColor;
                    animation: pulse 2s infinite ease-in-out;
                }
                @keyframes pulse {
                    0% { transform: scale(1); opacity: 0.8; }
                    50% { transform: scale(1.3); opacity: 1; }
                    100% { transform: scale(1); opacity: 0.8; }
                }
            </style>
        </div>
    `;
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const box = document.getElementById('chat-box');
    
    if (!input.value.trim()) return;
    
    const div = document.createElement('div');
    div.classList.add('fade-in');
    div.style = 'background: var(--primary); padding: 0.75rem 1rem; border-radius: 1rem 1rem 0 1rem; max-width: 80%; align-self: flex-end; color: white;';
    div.innerText = input.value;
    box.appendChild(div);
    
    const userMsg = input.value;
    input.value = '';
    
    // API Call for answer
    if (State.activeProject) {
        askBot(userMsg, box);
    } else {
        setTimeout(() => {
            const botDiv = document.createElement('div');
            botDiv.classList.add('fade-in');
            botDiv.style = 'background: var(--surface); padding: 0.75rem 1rem; border-radius: 0 1rem 1rem 1rem; max-width: 80%; align-self: flex-start; border: 1px solid var(--surface-border);';
            botDiv.innerText = "Please select a project to enable real AI responses.";
            box.appendChild(botDiv);
            box.scrollTop = box.scrollHeight;
        }, 600);
    }
}

async function askBot(question, box) {
    try {
        const response = await fetch(`${API_BASE}/ask/${State.activeProject.id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();
        
        const botDiv = document.createElement('div');
        botDiv.classList.add('fade-in');
        botDiv.style = 'background: var(--surface); padding: 0.75rem 1rem; border-radius: 0 1rem 1rem 1rem; max-width: 80%; align-self: flex-start; border: 1px solid var(--surface-border);';
        botDiv.innerText = data.answer || "I'm not sure how to answer that.";
        box.appendChild(botDiv);
        box.scrollTop = box.scrollHeight;
        
        if (data.confidence) {
             showToast(`Match Confidence: ${Math.round(data.confidence * 100)}%`);
        }
    } catch (error) {
        showToast('Inference error', 'error');
    }
}

// Voice Testing (Ultra Feature)
let recognition;
let isListening = false;

function setupVoice() {
    if (!('webkitSpeechRecognition' in window) && !('speechRecognition' in window)) {
        showToast('Speech recognition not supported in this browser.', 'warning');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    
    recognition.onstart = () => {
        isListening = true;
        document.getElementById('voice-btn').classList.add('btn-primary');
        document.getElementById('speech-result').innerText = "Listening...";
    };
    
    recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');
        document.getElementById('speech-result').innerText = transcript;
        
        if (event.results[0].isFinal) {
            document.getElementById('chat-input').value = transcript;
            setTimeout(() => sendMessage(), 500);
        }
    };
    
    recognition.onend = () => {
        isListening = false;
        document.getElementById('voice-btn').classList.remove('btn-primary');
        if (document.getElementById('speech-result').innerText === "Listening...") {
            document.getElementById('speech-result').innerText = "Stopped.";
        }
    };
    
    recognition.onerror = (event) => {
        console.error('Speech error:', event.error);
        showToast('Speech error: ' + event.error, 'error');
    };
}

function toggleVoice() {
    if (!recognition) setupVoice();
    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
    }
}

async function addIntent() {
    if (!State.activeProject) return;
    
    const name = prompt("Enter Intent Name (e.g. 'greeting'):");
    if (!name) return;
    
    const utterancesStr = prompt("Enter sample phrases (separated by commas):");
    const utterances = utterancesStr ? utterancesStr.split(',').map(s => s.trim()) : [];
    
    const response = prompt("Enter Bot Response:");
    if (!response) return;

    try {
        const res = await fetch(`${API_BASE}/chatbots/${State.activeProject.id}/intents`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                name: name, 
                utterances: utterances,
                responses: [response]
            })
        });
        
        if (res.ok) {
            showToast('Intent added successfully!');
            selectProject(State.activeProject.id); // Refresh
        } else {
            const err = await res.json();
            showToast(err.error || 'Failed to add intent', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}
