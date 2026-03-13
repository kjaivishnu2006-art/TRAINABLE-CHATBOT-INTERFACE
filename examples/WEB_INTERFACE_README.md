# HTML/CSS/JavaScript Chatbot Training Interface

A fully-functional, modern web-based interface for building and training chatbots without any backend required.

## 🚀 Quick Start

### Open in Browser

```bash
# Simply open the HTML file in any modern browser
# Windows: Double-click index.html
# macOS/Linux: Open with your browser

# Or use a local server
python -m http.server 8000
# Then visit: http://localhost:8000
```

## ✨ Features

### 📝 Intent Builder
- **Add/Edit/Delete Intents** - Create training intents easily
- **Utterances** - Add training examples (what users say)
- **Responses** - Define bot responses
- **Real-time Stats** - See intent and utterance counts
- **Tag Preview** - Quick view of your data

### 💬 Test Chat
- **Interactive Testing** - Chat with your trained model
- **Real-time Responses** - Instant feedback
- **Confidence Display** - See matching accuracy
- **Message History** - Track conversation

### 📦 Export/Import
- **JSON Export** - Download your dataset
- **JSON Import** - Load saved datasets
- **Statistics** - View dataset metrics
- **Data Preservation** - Auto-save to browser storage

### ⚙️ Settings
- **Chatbot Name** - Customize your bot
- **Chatbot Description** - Add details
- **Training Config** - Adjust epochs, batch size
- **Confidence Threshold** - Control strictness
- **Clear Data** - Reset everything

## 📂 Files

| File | Purpose |
|------|---------|
| `index.html` | Main interface structure |
| `style.css` | All styling and layout |
| `script.js` | Logic and interactivity |

## 🎯 How to Use

### Step 1: Create Intent

1. Click **+ Add Intent** button
2. Enter intent name (e.g., "greeting")
3. Add utterances (one per line):
   ```
   hello
   hi
   hey there
   ```
4. Add responses:
   ```
   Hello! How can I help?
   Hi there! What can I do?
   ```
5. Click **Save Intent**

### Step 2: Add More Intents

Repeat Step 1 for other intents:
- `farewell` - When user says goodbye
- `help_request` - When user asks for help
- `joke` - Funny request
- etc.

### Step 3: Train Model

1. Click **🚀 Train Model** button
2. Wait for training to complete
3. See success message

### Step 4: Test Chat

1. Switch to **Test Chat** tab
2. Type a message (e.g., "hello")
3. See bot response
4. Try different questions

### Step 5: Export Data

1. Go to **Export** tab
2. Choose export option:
   - **Download JSON** - Save dataset file
   - **View Stats** - See metrics
   - **Import Dataset** - Load previous data

## 💾 Data Storage

### Browser Storage
- Data saved automatically to `localStorage`
- Persists between sessions
- No server required
- Survives browser refresh

### Export/Import
```javascript
// Export to JSON
builder.exportJSON();  // Downloads file

// Import from JSON
// Click "Import Dataset" and select a file
```

## 🎨 UI Components

### Modal Dialog
```html
<div class="modal" id="intent-modal">
  <div class="modal-content">
    <!-- Content here -->
  </div>
</div>
```

### Chat Interface
```html
<div class="chat-container">
  <div class="chat-messages"></div>
  <div class="chat-input-group">
    <input class="chat-input">
    <button class="btn">Send</button>
  </div>
</div>
```

### Cards & Sections
```html
<div class="intent-card">
  <div class="intent-card-header">
    <div class="intent-card-title">Intent Name</div>
  </div>
  <div class="intent-card-content">
    <!-- Content -->
  </div>
</div>
```

## 🎨 Customization

### Change Colors

Edit CSS variables in `style.css`:

```css
:root {
    --primary-color: #2563eb;      /* Blue */
    --success-color: #10b981;      /* Green */
    --danger-color: #ef4444;       /* Red */
}
```

### Add Custom Intent

```javascript
// In JavaScript console
builder.intents.push({
    name: "my_intent",
    description: "My custom intent",
    utterances: ["hello", "hi"],
    responses: ["Hi there!"]
});
builder.renderIntents();
```

### Adjust Matching Algorithm

Edit the `findBestIntent()` method in `script.js` to:
- Change similarity calculation
- Add fuzzy matching
- Implement different scoring

## 📱 Responsive Design

Works on all screen sizes:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px-1200px)
- ✅ Mobile (< 768px)

**Mobile Features:**
- Stacked navigation
- Full-width inputs
- Touch-friendly buttons
- Optimized modals

## 🔧 JavaScript API

### ChatBotBuilder Class

```javascript
// Access the builder instance
window.builder

// Methods
builder.addIntent(e)              // Add new intent
builder.deleteIntent(index)       // Delete by index
builder.trainModel()              // Train the model
builder.sendMessage()             // Send chat message
builder.exportJSON()              // Export dataset
builder.importJSON(e)             // Import dataset
builder.showStats()               // Display statistics
builder.clearData()               // Clear all data

// Properties
builder.intents                   // Array of intents
builder.trainedModel             // Trained model reference
builder.threshold                // Confidence threshold
```

### Add Event Listener

```javascript
document.getElementById('add-intent-btn').addEventListener('click', () => {
    builder.openIntentModal();
});
```

## 🧪 Example Quickly Populated

Pre-load sample data:

```js
// In browser console
builder.intents = [
    {
        name: "greeting",
        description: "User greets",
        utterances: ["hello", "hi", "hey"],
        responses: ["Hello!", "Hi there!"]
    }
];
builder.renderIntents();
```

## 🚀 Advanced Features

### Local Storage Management

```javascript
// Save data
localStorage.setItem('chatbot_intents', JSON.stringify(builder.intents));

// Load data
const data = JSON.parse(localStorage.getItem('chatbot_intents'));
```

### Message History

```javascript
// Access chat history
builder.messageHistory

// Clear history
builder.messageHistory = [];
```

### Custom Alerts

```javascript
// Show success
builder.showAlert('Success!', 'success');

// Show error
builder.showAlert('Error!', 'error');

// Show warning
builder.showAlert('Warning!', 'warning');
```

## 📋 Example Intents

Pre-configured examples you can try:

### Customer Service
```json
{
  "name": "order_status",
  "utterances": ["where is my order", "track package"],
  "responses": ["Your order is on the way!"]
}
```

### FAQ
```json
{
  "name": "ask_price",
  "utterances": ["how much", "what's the cost"],
  "responses": ["Our pricing varies by plan"]
}
```

## 🐛 Troubleshooting

### Data not saving?
- Clear browser storage: `localStorage.clear()`
- Check browser storage limit (usually 5-10MB)
- Try exporting and re-importing

### Chat not responding?
- Make sure model is trained (green progress bar)
- Check confidence threshold setting
- Review utterances for good coverage

### Import fails?
- Validate JSON format (use https://jsonlint.com)
- Ensure `intents` array exists
- Check file encoding (should be UTF-8)

## 🎓 Learning Resources

- [MDN Web Docs](https://developer.mozilla.org/) - HTML/CSS/JS documentation
- [JavaScript Console](https://developer.chrome.com/docs/devtools/console/) - Debug code
- [LocalStorage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) - Data persistence
- [HTML Forms](https://developer.mozilla.org/en-US/docs/Learn/Forms) - Form handling

## 📤 Deploying

### Host on GitHub Pages
1. Push files to GitHub repository
2. Enable GitHub Pages in settings
3. Access at: `https://username.github.io/repo-name`

### Host on Netlify
1. Drag and drop folder to Netlify
2. Get instant URL
3. Share with others

### Host on Local Server

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (http-server package)
npx http-server

# Then open: http://localhost:8000
```

## 💡 Tips & Tricks

1. **Organize Intents** - Group related ones together
2. **Diverse Utterances** - Use varied phrasings
3. **Test Thoroughly** - Try different inputs
4. **Export Often** - Backup your data
5. **Iterate** - Improve dataset over time

## 🎉 Ready to Build?

Open `index.html` in your browser and start creating amazing chatbots! 

---

**No installation, no server, no backend needed. Just pure HTML, CSS, and JavaScript!** 🚀
