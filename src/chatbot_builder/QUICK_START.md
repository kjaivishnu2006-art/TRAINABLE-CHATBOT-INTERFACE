# Quick Start Guide - Flask API Backend

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
cd src/chatbot_builder
pip install -r ../../requirements_flask.txt
```

### 2. Configure Database (.env)
```bash
# Copy template
cp .env.example .env

# Edit .env if needed (default SQLite works for development)
```

### 3. Create Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 4. Start Server
```bash
python run.py
```

**Output:**
```
Starting Flask API on port 5000...
Debug mode: True
Database: sqlite:///chatbot.db
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 5. Test API
```bash
curl http://localhost:5000/api/health
# Response: {"status": "ok", "message": "API is running"}
```

### 6. Use Web Interface
Replace `script.js` with `script_api.js` in `index.html`:

```html
<!-- In index.html -->
<script src="script_api.js"></script>  <!-- Use API backend -->
<!-- <script src="script.js"></script> -->  <!-- Comment out local storage -->
```

## 📝 Usage Example

### Create Chatbot via API
```bash
curl -X POST http://localhost:5000/api/chatbots \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My ChatBot",
    "description": "A helpful assistant"
  }'
```

### Add Intent
```bash
curl -X POST http://localhost:5000/api/chatbots/1/intents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "greeting",
    "description": "User greets the bot",
    "utterances": ["hello", "hi", "hey"],
    "responses": ["Hello! How can I help?", "Hi there!"]
  }'
```

### Export Dataset
```bash
curl http://localhost:5000/api/chatbots/1/export > dataset.json
```

## 🗄️ Database Locations

- **SQLite**: `chatbot.db` (in same directory as app.py)
- **PostgreSQL**: Configure in `.env` DATABASE_URL
- **MySQL**: Configure in `.env` DATABASE_URL

## 🔧 Development Commands

### Initialize database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

### Drop all tables (WARNING)
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.drop_all()
```

### Query data
```bash
python
>>> from app import app, db, ChatBot
>>> with app.app_context():
...     chatbots = ChatBot.query.all()
...     for cb in chatbots:
...         print(f"{cb.id}: {cb.name}")
```

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Using Docker
```bash
docker build -t chatbot-api .
docker run -p 5000:5000 chatbot-api
```

### Environment Variables (Production)
```bash
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://...
CORS_ORIGINS=https://yourdomain.com
```

## 🐛 Troubleshooting

### "Address already in use"
Port 5000 is already running. Use different port:
```bash
PORT=5001 python run.py
```

### "ModuleNotFoundError: No module named 'flask'"
Install dependencies:
```bash
pip install -r requirements_flask.txt
```

### "sqlite3.OperationalError: database is locked"
Another process is using the database. Restart the server.

### "CORS error" in browser
Ensure `CORS_ORIGINS=*` in `.env` or configure specific domain.

## 📚 Documentation Files

- [FLASK_API_README.md](FLASK_API_README.md) - Complete API reference
- [requirements_flask.txt](../../requirements_flask.txt) - Dependencies
- [app.py](app.py) - Flask application
- [script_api.js](../../examples/script_api.js) - Frontend integration

## ✅ Validation Checklist

- [ ] Dependencies installed (`pip list | grep -i flask`)
- [ ] Database created (check `chatbot.db` exists)
- [ ] API running (`curl http://localhost:5000/api/health`)
- [ ] CORS enabled (no errors in browser console)
- [ ] Web interface loads (http://localhost:3000 or file://)
- [ ] Can create chatbot from UI
- [ ] Can add intents
- [ ] Can export/import JSON
- [ ] Data persists after refresh

## 💡 Pro Tips

1. **Use PostgreSQL for production** - SQLite has limitations with concurrent requests
2. **Enable query logging** - Add to .env: `SQLALCHEMY_ECHO=True`
3. **Use Postman** - Test API endpoints with Postman collection
4. **Monitor database** - Check `chatbot.db` file size for disk usage
5. **Version your exports** - Exports include timestamp for tracking

---

For complete API documentation, see [FLASK_API_README.md](FLASK_API_README.md)
