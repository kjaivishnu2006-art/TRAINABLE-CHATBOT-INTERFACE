# Flask REST API Backend - Complete Documentation

## 📌 Overview

A production-ready **Flask REST API** with SQLAlchemy ORM for the Trainable ChatBot Builder. Stores, manages, and retrieves chatbot training data from a persistent database.

### What's New?

✅ **Database persistence** - Data survives server restarts  
✅ **Multi-user support** - Multiple users can work with different chatbots  
✅ **RESTful API** - Standard HTTP methods and JSON responses  
✅ **CORS enabled** - Works seamlessly with web frontend  
✅ **Production ready** - Error handling, validation, logging  
✅ **Multiple databases** - SQLite, PostgreSQL, MySQL support  

---

## 🎯 Quick Start

### 1. Install Dependencies (2 minutes)

```bash
pip install -r requirements_flask.txt
```

### 2. Run Flask Server (30 seconds)

```bash
cd src/chatbot_builder
python run.py
```

**Output:**
```
Starting Flask API on port 5000...
Debug mode: True
Database: sqlite:///chatbot.db
 * Running on http://0.0.0.0:5000
```

### 3. Test API (10 seconds)

```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

### 4. Open Web Interface (Browser)

Use the new API-enabled interface:
```
file:///path/to/examples/index_api.html
```

**Or use Python server:**
```bash
cd examples
python -m http.server 3000
# Open: http://localhost:3000/index_api.html
```

---

## 📁 File Structure

```
Trainable ChatBot Interface/
│
├── src/chatbot_builder/
│   ├── app.py                    ← Flask application (main)
│   ├── config.py                 ← Configuration classes
│   ├── run.py                    ← Development server
│   ├── wsgi.py                   ← Production WSGI
│   ├── test_api.py               ← Test suite
│   ├── .env.example              ← Environment template
│   ├── .gitignore                ← Git ignore patterns
│   ├── FLASK_API_README.md       ← Complete API docs
│   ├── QUICK_START.md            ← Quick start guide
│   └── chatbot.db                ← SQLite database (auto-created)
│
├── examples/
│   ├── index_api.html            ← New API-enabled UI
│   ├── script_api.js             ← Frontend with API calls
│   ├── style.css                 ← Shared styling
│   │
│   ├── index.html                ← Old LocalStorage version
│   └── script.js                 ← Old LocalStorage version
│
├── FLASK_INTEGRATION_GUIDE.md    ← Integration guide
├── requirements_flask.txt         ← Python dependencies
└── README.md                      ← Main project README
```

---

## 🔑 Key Features

### 1. Complete CRUD Operations

```
Chatbots:  Create, Read, Update, Delete
Intents:   Create, Read, Update, Delete
Entities:  Create, Read, Update, Delete
```

### 2. Database Models

- **ChatBot** - Project container
- **Intent** - User intention/goal
- **Utterance** - Example user input
- **Response** - Bot reply
- **Entity** - Named entity (person, date, location, etc.)

### 3. RESTful Endpoints

```
GET  /api/health                     - Health check
GET  /api/stats                      - System statistics

GET  /api/chatbots                   - List all
POST /api/chatbots                   - Create new
GET  /api/chatbots/{id}              - Get details
PUT  /api/chatbots/{id}              - Update
DELETE /api/chatbots/{id}            - Delete

POST /api/chatbots/{id}/intents      - Create intent
PUT  /api/intents/{id}               - Update intent
DELETE /api/intents/{id}             - Delete intent

POST /api/chatbots/{id}/entities     - Create entity
PUT  /api/entities/{id}              - Update entity
DELETE /api/entities/{id}            - Delete entity

GET  /api/chatbots/{id}/export       - Export as JSON
POST /api/chatbots/{id}/import       - Import from JSON
```

### 4. Error Handling

```
400 Bad Request    - Invalid input
404 Not Found      - Resource doesn't exist
409 Conflict       - Duplicate entity
500 Server Error   - Unexpected error
```

All errors return JSON:
```json
{
  "error": "Descriptive error message"
}
```

---

## 🧪 Testing

### Automated Tests

Run comprehensive test suite:
```bash
cd src/chatbot_builder

# Test with default API (localhost:5000)
python test_api.py

# Test with custom URL
python test_api.py http://your-api.com
```

**Requires colorama:**
```bash
pip install colorama
```

### Manual Testing with cURL

```bash
# Create chatbot
curl -X POST http://localhost:5000/api/chatbots \
  -H "Content-Type: application/json" \
  -d '{"name":"My Bot","description":"Test"}'

# Get all chatbots
curl http://localhost:5000/api/chatbots

# Create intent
curl -X POST http://localhost:5000/api/chatbots/1/intents \
  -H "Content-Type: application/json" \
  -d '{
    "name":"greeting",
    "utterances":["hello","hi"],
    "responses":["Hello!"]
  }'
```

### Manual Testing with Python

```python
import requests

API = "http://localhost:5000/api"

# Create chatbot
resp = requests.post(f"{API}/chatbots", 
    json={"name": "My Bot", "description": "Test"})
chatbot = resp.json()
print(f"Created: {chatbot['id']}: {chatbot['name']}")

# Get full details
resp = requests.get(f"{API}/chatbots/{chatbot['id']}")
print(resp.json())
```

---

## 🗄️ Database

### SQLite (Development)

**Location:** `src/chatbot_builder/chatbot.db`

**Pros:**
- No installation needed
- Single file
- Good for prototyping

**Cons:**
- Limited concurrent users
- File-based (not ACID)

**Backup:**
```bash
cp chatbot.db chatbot.db.backup
```

### PostgreSQL (Production)

**Pros:**
- Multi-user support
- ACID compliance
- Advanced features

**Setup:**
```bash
createdb chatbot_db

# Update .env
DATABASE_URL=postgresql://user:password@localhost/chatbot_db
```

### MySQL (Production)

**Setup:**
```bash
mysql -u root -p
CREATE DATABASE chatbot_db;

# Update .env
DATABASE_URL=mysql+pymysql://user:password@localhost/chatbot_db
```

---

## 🚀 Deployment

### Local Development

```bash
python run.py
# http://localhost:5000
```

### Docker

```bash
docker build -t chatbot-api .
docker run -p 5000:5000 chatbot-api
```

### Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Heroku

```bash
heroku create my-chatbot-api
git push heroku main
heroku open
```

**Environment variables:**
```bash
heroku config:set FLASK_ENV=production
heroku config:set DATABASE_URL=...
```

---

## 📊 Example Workflow

### Step 1: Create Chatbot

```bash
curl -X POST http://localhost:5000/api/chatbots \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Service",
    "description": "Help customers with issues"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Customer Service",
  "description": "Help customers with issues",
  "created_at": "2026-03-12T10:00:00",
  "intent_count": 0,
  "entity_count": 0,
  "is_trained": false
}
```

### Step 2: Add Intents

```bash
curl -X POST http://localhost:5000/api/chatbots/1/intents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "complaint",
    "description": "Customer has a complaint",
    "priority": "high",
    "utterances": [
      "This product is broken",
      "I have a complaint",
      "This doesnt work"
    ],
    "responses": [
      "I apologize for the issue. Let me help you.",
      "We take complaints seriously. How can I assist?"
    ]
  }'
```

### Step 3: Add Entities

```bash
curl -X POST http://localhost:5000/api/chatbots/1/entities \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "entity.product",
    "entity_type": "PRODUCT",
    "description": "Product name",
    "examples": ["laptop", "phone", "tablet"]
  }'
```

### Step 4: Export Configuration

```bash
curl http://localhost:5000/api/chatbots/1/export > config.json
```

### Step 5: Import to Another Project

```bash
curl -X POST http://localhost:5000/api/chatbots/2/import \
  -H "Content-Type: application/json" \
  -d @config.json
```

---

## 🔧 Configuration

### .env File

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///chatbot.db

# API
PORT=5000
CORS_ORIGINS=*

# Optional
SECRET_KEY=change-me-in-production
```

### Environment Options

```bash
FLASK_ENV=development    # Development mode (debug on)
FLASK_ENV=production     # Production mode (debug off)

CORS_ORIGINS=*           # Allow all origins
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com # Specific origins

DATABASE_URL=sqlite:///chatbot.db           # SQLite (default)
DATABASE_URL=postgresql://user:pass@host    # PostgreSQL
DATABASE_URL=mysql+pymysql://user:pass@host # MySQL
```

---

## 🐛 Troubleshooting

### "Cannot connect to API"

```bash
# 1. Verify API is running
curl http://localhost:5000/api/health

# 2. Check if port 5000 is available
lsof -i :5000

# 3. Use different port
PORT=5001 python run.py
```

### "CORS error" in browser console

**Solution:**
```bash
# .env
CORS_ORIGINS=*
# Then restart API
```

### "Database is locked"

**Solution:**
```bash
# Restart API
# Ctrl+C to stop first

# Or reset database
rm chatbot.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Tests failing

```bash
# 1. Make sure API is running
python run.py

# 2. Run tests
python test_api.py

# 3. If still failing, check logs
FLASK_ENV=development python run.py
```

---

## 📚 Documentation

- **[FLASK_API_README.md](src/chatbot_builder/FLASK_API_README.md)** - Complete API reference
- **[FLASK_INTEGRATION_GUIDE.md](FLASK_INTEGRATION_GUIDE.md)** - Integration instructions
- **[QUICK_START.md](src/chatbot_builder/QUICK_START.md)** - 5-minute setup
- **[Flask Documentation](https://flask.palletsprojects.com/)** - Official Flask docs
- **[SQLAlchemy Documentation](https://docs.sqlalchemy.org/)** - ORM reference

---

## 📋 File Reference

| File | Purpose | LOC |
|------|---------|-----|
| `app.py` | Flask app + models + routes | 650+ |
| `config.py` | Configuration classes | 30 |
| `run.py` | Development server | 20 |
| `wsgi.py` | Production entry point | 10 |
| `test_api.py` | Test suite | 350+ |
| `script_api.js` | Frontend integration | 600+ |
| `index_api.html` | API-enabled UI | 350+ |

---

## ✨ Features Comparison

### LocalStorage Version (script.js)
- ✅ No backend needed
- ✅ Offline capable  
- ❌ Single device only
- ❌ Limited storage (5-10 MB)
- ❌ Manual backup

### API Backend Version (script_api.js)
- ✅ Multi-user support
- ✅ Persistent storage
- ✅ Team collaboration
- ✅ Unlimited data
- ✅ Automatic backup
- ❌ Requires running server

---

## 🔐 Security Notes

For production deployment:

1. **Change SECRET_KEY**
   ```bash
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key
   ```

2. **Use HTTPs**
   ```bash
   # Behind Nginx/Apache with SSL
   gunicorn -w 4 wsgi:app
   ```

3. **Add Authentication**
   ```python
   @require_api_key
   def create_chatbot():
       ...
   ```

4. **Enable CORS carefully**
   ```bash
   CORS_ORIGINS=https://yourdomain.com  # Not *
   ```

5. **Rate limiting**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   ```

---

## 🎓 Learning Resources

### API Basics
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [JSON Format](https://www.json.org/)

### Flask
- [Flask Quickstart](https://flask.palletsprojects.com/quickstart/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)

### Databases
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [PostgreSQL Getting Started](https://www.postgresql.org/docs/current/tutorial-start.html)
- [MySQL Tutorial](https://dev.mysql.com/doc/refman/8.0/en/tutorial.html)

---

## 💡 Next Steps

1. ✅ **Setup complete** - API and UI ready
2. 📊 **Add more intents** - Explore full functionality
3. 🚀 **Deploy to production** - Use Gunicorn or Docker
4. 📱 **Build mobile app** - Use same API endpoints
5. 🔌 **Integrate with ML** - Add TensorFlow training

---

## 📞 Support

- **API Issues?** → [FLASK_API_README.md](src/chatbot_builder/FLASK_API_README.md)
- **Integration Help?** → [FLASK_INTEGRATION_GUIDE.md](FLASK_INTEGRATION_GUIDE.md)
- **Quick Start?** → [QUICK_START.md](src/chatbot_builder/QUICK_START.md)
- **Flask Docs?** → https://flask.palletsprojects.com/

---

**Version:** 1.0.0  
**Last Updated:** March 2026  
**Status:** Production Ready ✓
