# Flask API Backend Documentation

Complete REST API for the Trainable ChatBot Builder web interface.

## 📋 Overview

A production-ready Flask REST API with SQLAlchemy ORM for managing chatbot training data.

**Features:**
- ✅ Full CRUD operations
- ✅ Database persistence (SQLite, PostgreSQL, MySQL)
- ✅ CORS enabled for web frontend
- ✅ JSON request/response
- ✅ Error handling
- ✅ Data validation
- ✅ Import/Export functionality

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements_flask.txt
```

### Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

Or use CLI:
```bash
flask db init
```

### Run Server

```bash
python run.py
# or
flask run
```

Server starts at: `http://localhost:5000`

## 🔌 API Endpoints

### Health Check

```
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

### ChatBot Endpoints

#### List All ChatBots
```
GET /api/chatbots
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "My ChatBot",
    "description": "A helpful assistant",
    "language": "en",
    "created_at": "2026-03-12T10:00:00",
    "updated_at": "2026-03-12T10:00:00",
    "is_trained": false,
    "intent_count": 3,
    "entity_count": 2
  }
]
```

#### Create ChatBot
```
POST /api/chatbots
Content-Type: application/json

{
  "name": "My ChatBot",
  "description": "A helpful assistant",
  "language": "en"
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "My ChatBot",
  "description": "A helpful assistant",
  "language": "en",
  "created_at": "2026-03-12T10:00:00",
  "updated_at": "2026-03-12T10:00:00",
  "is_trained": false,
  "intent_count": 0,
  "entity_count": 0
}
```

#### Get ChatBot Details
```
GET /api/chatbots/{id}
```

**Response:**
```json
{
  "id": 1,
  "name": "My ChatBot",
  "description": "A helpful assistant",
  "language": "en",
  "created_at": "2026-03-12T10:00:00",
  "updated_at": "2026-03-12T10:00:00",
  "is_trained": false,
  "intent_count": 3,
  "entity_count": 2,
  "intents": [
    {
      "id": 1,
      "name": "greeting",
      "description": "Greet the user",
      "priority": "high",
      "utterances": [
        { "id": 1, "text": "hello" },
        { "id": 2, "text": "hi" }
      ],
      "responses": [
        { "id": 1, "text": "Hello! How can I help?" }
      ],
      "created_at": "2026-03-12T10:00:00",
      "updated_at": "2026-03-12T10:00:00"
    }
  ],
  "entities": [
    {
      "id": 1,
      "entity_id": "entity.name",
      "entity_type": "NAME",
      "description": "Person's name",
      "examples": ["John", "Alice"]
    }
  ]
}
```

#### Update ChatBot
```
PUT /api/chatbots/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description",
  "language": "en",
  "is_trained": true
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Updated Name",
  ...
}
```

#### Delete ChatBot
```
DELETE /api/chatbots/{id}
```

**Response (200):**
```json
{
  "message": "Chatbot deleted successfully"
}
```

### Intent Endpoints

#### Create Intent
```
POST /api/chatbots/{chatbot_id}/intents
Content-Type: application/json

{
  "name": "greeting",
  "description": "User greets the bot",
  "priority": "high",
  "utterances": [
    "hello",
    "hi",
    "hey there"
  ],
  "responses": [
    "Hello! How can I help?",
    "Hi there!"
  ]
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "greeting",
  "description": "User greets the bot",
  "priority": "high",
  "utterances": [
    { "id": 1, "text": "hello" },
    { "id": 2, "text": "hi" },
    { "id": 3, "text": "hey there" }
  ],
  "responses": [
    { "id": 1, "text": "Hello! How can I help?" },
    { "id": 2, "text": "Hi there!" }
  ],
  "created_at": "2026-03-12T10:00:00",
  "updated_at": "2026-03-12T10:00:00"
}
```

#### Get Intent
```
GET /api/intents/{id}
```

#### Update Intent
```
PUT /api/intents/{id}
Content-Type: application/json

{
  "name": "greeting",
  "description": "Updated description",
  "priority": "medium",
  "utterances": ["hello", "hi"],
  "responses": ["Hello!"]
}
```

#### Delete Intent
```
DELETE /api/intents/{id}
```

### Entity Endpoints

#### Create Entity
```
POST /api/chatbots/{chatbot_id}/entities
Content-Type: application/json

{
  "entity_id": "entity.name",
  "entity_type": "NAME",
  "description": "Person's name",
  "examples": ["John", "Alice", "Bob"]
}
```

#### Get Entity
```
GET /api/entities/{id}
```

#### Update Entity
```
PUT /api/entities/{id}
Content-Type: application/json

{
  "entity_id": "entity.name",
  "entity_type": "NAME",
  "description": "Updated description",
  "examples": ["Updated", "Examples"]
}
```

#### Delete Entity
```
DELETE /api/entities/{id}
```

### Export/Import Endpoints

#### Export ChatBot
```
GET /api/chatbots/{id}/export
```

**Response:**
```json
{
  "metadata": {
    "name": "My ChatBot",
    "description": "Description",
    "language": "en",
    "created_date": "2026-03-12T10:00:00",
    "version": "1.0.0"
  },
  "intents": [...],
  "entities": [...],
  "statistics": {
    "total_intents": 3,
    "total_utterances": 12,
    "total_responses": 9,
    "total_entities": 2
  }
}
```

#### Import ChatBot
```
POST /api/chatbots/{id}/import
Content-Type: application/json

{
  "intents": [...],
  "entities": [...]
}
```

### Statistics Endpoint

#### Get System Statistics
```
GET /api/stats
```

**Response:**
```json
{
  "total_chatbots": 5,
  "total_intents": 25,
  "total_utterances": 150,
  "total_responses": 100,
  "total_entities": 10,
  "trained_chatbots": 2
}
```

## 🗄️ Database Schema

### ChatBots Table
```
id (Primary Key)
name (Unique, String)
description (Text)
language (String, default: 'en')
created_at (DateTime)
updated_at (DateTime)
is_trained (Boolean, default: False)
```

### Intents Table
```
id (Primary Key)
chatbot_id (Foreign Key)
name (String)
description (Text)
priority (String: high/medium/low)
created_at (DateTime)
updated_at (DateTime)
Unique Constraint: (chatbot_id, name)
```

### Utterances Table
```
id (Primary Key)
intent_id (Foreign Key)
text (String)
created_at (DateTime)
```

### Responses Table
```
id (Primary Key)
intent_id (Foreign Key)
text (String)
created_at (DateTime)
```

### Entities Table
```
id (Primary Key)
chatbot_id (Foreign Key)
entity_id (String, e.g., "entity.name")
entity_type (String, e.g., "NAME")
description (Text)
examples (JSON Array)
created_at (DateTime)
Unique Constraint: (chatbot_id, entity_id)
```

## 🔑 Error Responses

### 400 Bad Request
```json
{
  "error": "Name is required"
}
```

### 404 Not Found
```json
{
  "error": "Chatbot not found"
}
```

### 409 Conflict
```json
{
  "error": "Chatbot with this name already exists"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## 🔧 Configuration

### Environment Variables

```bash
# .env file
FLASK_ENV=development
DATABASE_URL=sqlite:///chatbot.db
FLASK_APP=app.py
CORS_ORIGINS=*
```

### Supported Databases

**SQLite (default):**
```
DATABASE_URL=sqlite:///chatbot.db
```

**PostgreSQL:**
```
DATABASE_URL=postgresql://user:password@localhost/chatbot_db
```

**MySQL:**
```
DATABASE_URL=mysql+pymysql://user:password@localhost/chatbot_db
```

## 🧪 Testing API

### Using cURL

```bash
# Create chatbot
curl -X POST http://localhost:5000/api/chatbots \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Bot", "description": "A test chatbot"}'

# Get all chatbots
curl http://localhost:5000/api/chatbots

# Create intent
curl -X POST http://localhost:5000/api/chatbots/1/intents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "greeting",
    "utterances": ["hello", "hi"],
    "responses": ["Hello!"]
  }'
```

### Using Python

```python
import requests

API_URL = "http://localhost:5000/api"

# Create chatbot
response = requests.post(
    f"{API_URL}/chatbots",
    json={
        "name": "My Bot",
        "description": "My chatbot"
    }
)
chatbot = response.json()

# Create intent
response = requests.post(
    f"{API_URL}/chatbots/{chatbot['id']}/intents",
    json={
        "name": "greeting",
        "utterances": ["hello", "hi"],
        "responses": ["Hello!"]
    }
)
intent = response.json()

# Get chatbot with intents
response = requests.get(f"{API_URL}/chatbots/{chatbot['id']}")
full_chatbot = response.json()
```

### Using JavaScript

See `script_api.js` for full implementation using the Fetch API.

```javascript
const API_URL = 'http://localhost:5000/api';

// Create chatbot
async function createChatbot() {
    const response = await fetch(`${API_URL}/chatbots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: 'My Bot',
            description: 'My chatbot'
        })
    });
    return await response.json();
}

// Create intent
async function createIntent(chatbotId) {
    const response = await fetch(`${API_URL}/chatbots/${chatbotId}/intents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: 'greeting',
            utterances: ['hello', 'hi'],
            responses: ['Hello!']
        })
    });
    return await response.json();
}
```

## 📊 Example Workflow

```
1. POST /api/chatbots
   └─> Create "Customer Service Bot"

2. POST /api/chatbots/{id}/intents
   ├─> Create "greet" intent
   ├─> Create "help" intent
   └─> Create "feedback" intent

3. POST /api/chatbots/{id}/entities
   ├─> Create "entity.name" for names
   └─> Create "entity.date" for dates

4. GET /api/chatbots/{id}
   └─> Get full chatbot with all intents/entities

5. PUT /api/chatbots/{id}
   └─> Mark as trained (is_trained: true)

6. GET /api/chatbots/{id}/export
   └─> Export dataset as JSON

7. POST /api/chatbots/{id2}/import
   └─> Import dataset to another chatbot
```

## 🚀 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements_flask.txt .
RUN pip install -r requirements_flask.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
```

### Environment Variables

```bash
FLASK_ENV=production
DATABASE_URL=postgresql://...
FLASK_DEBUG=False
```

## 📄 License

MIT License

---

**Files:**
- `app.py` - Main Flask application
- `run.py` - Server runner
- `config.py` - Configuration
- `script_api.js` - Frontend integration
- `requirements_flask.txt` - Dependencies
