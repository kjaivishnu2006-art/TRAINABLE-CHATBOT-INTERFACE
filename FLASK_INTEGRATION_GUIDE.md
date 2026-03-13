# Flask API Integration Guide

Complete guide for integrating the Flask API backend with the ChatBot Builder web interface.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Setup Instructions](#setup-instructions)
3. [Running the Stack](#running-the-stack)
4. [API vs LocalStorage](#api-vs-localstorage)
5. [Frontend Integration](#frontend-integration)
6. [Database Management](#database-management)
7. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### Three-Tier Architecture

```
┌─────────────────────────────────────────┐
│     Web Interface (HTML/CSS/JS)        │
│  ├─ index_api.html - API version      │
│  ├─ style.css - Responsive styling    │
│  └─ script_api.js - API integration   │
└────────────┬────────────────────────────┘
             │ HTTP Requests (Fetch API)
             │ JSON Request/Response
┌────────────▼────────────────────────────┐
│      Flask REST API                     │
│  ├─ app.py - Main application          │
│  ├─ Models (ChatBot, Intent, etc.)     │
│  └─ Routes (CRUD endpoints)            │
└────────────┬────────────────────────────┘
             │ SQLAlchemy ORM
┌────────────▼────────────────────────────┐
│    SQLAlchemy Database Layer            │
│  ├─ SQLite (development)               │
│  └─ PostgreSQL/MySQL (production)      │
└─────────────────────────────────────────┘
```

### Data Flow Example

```
User Creates Intent in UI
        ↓
Form Validation (Client)
        ↓
POST /api/chatbots/{id}/intents (JSON)
        ↓
Flask Route Handler
        ↓
SQLAlchemy Model Creation
        ↓
Database INSERT
        ↓
JSON Response with Intent ID
        ↓
Update UI with New Intent
```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser with JavaScript enabled
- Optional: PostgreSQL or MySQL for production

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd "Trainable ChatBot interface"

# Install Flask dependencies
pip install -r requirements_flask.txt
```

**Expected output:**
```
Successfully installed flask-2.3.0 flask-cors-4.0.0 flask-sqlalchemy-3.0.5 sqlalchemy-2.0.23
```

### Step 2: Configure Environment

```bash
# Navigate to Flask directory
cd src/chatbot_builder

# Copy example environment file
cp .env.example .env

# Edit .env if needed (defaults work for development)
cat .env
```

**Default .env contents:**
```bash
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///chatbot.db
CORS_ORIGINS=*
```

### Step 3: Initialize Database

```bash
# Option 1: Using Python directly
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()

# Option 2: Using CLI
flask shell
>>> db.create_all()
>>> exit()
```

**Verify database was created:**
```bash
ls -la chatbot.db  # Should show file
```

### Step 4: Start Flask Server

```bash
# From src/chatbot_builder directory
python run.py
```

**Expected console output:**
```
Starting Flask API on port 5000...
Debug mode: True
Database: sqlite:///chatbot.db
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### Step 5: Test API Health

In another terminal:
```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

### Step 6: Open Web Interface

Open in browser:
```
file:///path/to/examples/index_api.html
```

Or serve with Python:
```bash
cd examples
python -m http.server 3000
# Open: http://localhost:3000/index_api.html
```

---

## Running the Stack

### Development Stack (Local)

**Terminal 1: Flask API**
```bash
cd src/chatbot_builder
python run.py
```

**Terminal 2: Web Server**
```bash
cd examples
python -m http.server 3000
```

**Browser:**
```
http://localhost:3000/index_api.html
```

### Docker Stack (Production-like)

**docker-compose.yml:**
```yaml
version: '3'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/chatbot
    depends_on:
      - db
  
  db:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=chatbot
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Run with Docker:**
```bash
docker-compose up
```

---

## API vs LocalStorage

### LocalStorage Version (`script.js`)
- **Data persistence**: Browser LocalStorage
- **Offline capable**: ✅ Yes
- **Multi-device sync**: ❌ No
- **Data backup**: Manual export/import
- **Best for**: Single-device prototyping

### API Backend Version (`script_api.js`)
- **Data persistence**: Database (SQLite/PostgreSQL/MySQL)
- **Offline capable**: ❌ No (requires server)
- **Multi-device sync**: ✅ Yes
- **Data backup**: Automatic + export/import
- **Best for**: Production, team collaboration, mobile apps

### Comparison Table

| Feature | LocalStorage | API Backend |
|---------|-------------|------------|
| Data Persistence | Browser storage | Server database |
| Payload Size Limit | 5-10 MB | Unlimited |
| Concurrent Users | 1 | Many |
| Mobile Support | App-only | Web + App |
| Real-time Sync | No | Yes (with WebSockets) |
| Version Control | Manual | Built-in |
| Backup | Manual | Automatic |
| Setup Complexity | Simple | Moderate |
| Production Ready | No | Yes |

---

## Frontend Integration

### Which File to Use?

**Development/Single User:**
```html
<script src="script.js"></script>
```

**Production/Multi-User:**
```html
<script src="script_api.js"></script>
```

### File Comparison

**script.js (LocalStorage)**
```javascript
class ChatBotBuilder {
    init() {
        this.loadFromStorage();  // Load from browser
    }
    
    saveToStorage() {
        localStorage.setItem('chatbots', JSON.stringify(this.intents));
    }
}
```

**script_api.js (API Backend)**
```javascript
class ChatBotBuilder {
    async init() {
        await this.loadChatbots();  // Load from API
    }
    
    async loadChatbots() {
        const response = await fetch(`${this.apiUrl}/chatbots`);
        return await response.json();
    }
}
```

### Configuration

Default API URL detection:
```javascript
const apiUrl = window.location.hostname === 'localhost'
    ? 'http://localhost:5000/api'
    : '/api';

window.builder = new ChatBotBuilder(apiUrl);
```

Override by adding to HTML:
```html
<script>
    window.API_URL = 'https://your-api.com/api';
</script>
<script src="script_api.js"></script>
```

---

## Database Management

### Using SQLite (Development)

**Database file location:**
```
src/chatbot_builder/chatbot.db
```

**Backup database:**
```bash
cp chatbot.db chatbot.db.backup
```

**Reset database:**
```bash
rm chatbot.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**Query database:**
```bash
python
>>> from app import app, db, ChatBot, Intent
>>> with app.app_context():
...     chatbots = ChatBot.query.all()
...     for cb in chatbots:
...         print(f"{cb.id}: {cb.name} ({len(cb.intents)} intents)")
```

### Using PostgreSQL (Production)

**Install PostgreSQL:**
```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download from https://www.postgresql.org/download/windows/
```

**Create database:**
```bash
createdb chatbot_db
```

**Update .env:**
```bash
DATABASE_URL=postgresql://user:password@localhost/chatbot_db
```

**Migrate database:**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Using MySQL (Production)

**Install MySQL:**
```bash
# macOS
brew install mysql
brew services start mysql

# Ubuntu
sudo apt-get install mysql-server

# Windows
# Download from https://dev.mysql.com/downloads/mysql/
```

**Create database:**
```bash
mysql -u root -p
CREATE DATABASE chatbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Update .env:**
```bash
DATABASE_URL=mysql+pymysql://user:password@localhost/chatbot_db
```

**Install driver:**
```bash
pip install pymysql
```

**Migrate database:**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## Troubleshooting

### API Connection Issues

**Symptom:** "Cannot connect to API"

**Solution:**
```bash
# 1. Verify Flask is running
curl http://localhost:5000/api/health

# 2. Check port 5000 is available
lsof -i :5000

# 3. Use different port
PORT=5001 python run.py

# 4. Check CORS settings in .env
CORS_ORIGINS=*
```

### Database Locked

**Symptom:** "sqlite3.OperationalError: database is locked"

**Solution:**
```bash
# 1. Restart Flask server
# Ctrl+C to stop

# 2. Kill existing process
pkill -f "python run.py"

# 3. Reset database
rm chatbot.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### CORS Error in Browser

**Symptom:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution:**
```bash
# 1. Ensure CORS is enabled in .env
CORS_ORIGINS=*

# 2. Or configure specific domain
CORS_ORIGINS=http://localhost:3000

# 3. Restart Flask server after changes
```

### ModuleNotFoundError

**Symptom:** "No module named 'flask'"

**Solution:**
```bash
# Install dependencies
pip install -r requirements_flask.txt

# Or specific packages
pip install flask flask-cors flask-sqlalchemy
```

### Browser Cache Issues

**Solution:**
```bash
# Hard refresh browser
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (macOS)

# Or clear cache
Settings → Clear browsing data → Cache

# Or use private/incognito window
```

### Port Already in Use

**Symptom:** "Address already in use"

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000
# or
netstat -lntp | grep 5000

# Kill process
kill -9 <PID>

# Use different port
PORT=5001 python run.py
```

---

## Advanced Configuration

### HTTPS/SSL (Production)

**Using self-signed certificate:**
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

python run.py --ssl-context=adhoc
```

**Using production SSL:**
```bash
# Use Gunicorn with Nginx reverse proxy
gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app

# Configure Nginx for HTTPS
```

### Rate Limiting

Add to `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/chatbots', methods=['POST'])
@limiter.limit("5 per minute")
def create_chatbot():
    ...
```

### Authentication

Add to `app.py`:
```python
from functools import wraps
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.environ.get('API_KEY'):
            return {'error': 'Invalid API key'}, 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/chatbots', methods=['POST'])
@require_api_key
def create_chatbot():
    ...
```

### Logging

Add to `app.py`:
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.before_request
def log_request():
    app.logger.info(f"{request.method} {request.path}")

@app.after_request
def log_response(response):
    app.logger.info(f"Response: {response.status_code}")
    return response
```

---

## Performance Optimization

### Database Indexing

Add to `models.py`:
```python
class Intent(db.Model):
    __table_args__ = (
        db.Index('ix_intent_chatbot_name', 'chatbot_id', 'name'),
        db.UniqueConstraint('chatbot_id', 'name'),
    )
```

### Query Optimization

```python
# Use eager loading
chatbot = ChatBot.query.options(
    db.joinedload(ChatBot.intents).joinedload(Intent.utterances)
).get(id)

# Use pagination
page = ChatBot.query.paginate(page=1, per_page=10)
```

### Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/stats')
@cache.cached(timeout=300)
def get_stats():
    ...
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `app.py` | Flask application and routes |
| `run.py` | Development server runner |
| `wsgi.py` | Production WSGI entry point |
| `config.py` | Configuration classes |
| `.env` | Environment variables |
| `.env.example` | Example environment file |
| `script_api.js` | Frontend API integration |
| `index_api.html` | HTML with API support |
| `requirements_flask.txt` | Python dependencies |
| `FLASK_API_README.md` | Complete API documentation |
| `QUICK_START.md` | Quick start guide |

---

## Support & Resources

- **API Docs**: [FLASK_API_README.md](FLASK_API_README.md)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Flask Docs**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

Last updated: March 2026
