# Examples

Pre-built chatbot templates to get you started quickly.

## Available Examples

### 1. Customer Service Bot

A helpful assistant for customer support and FAQs.

**Features:**
- Order tracking
- Return policy information
- Payment issue support
- Friendly greetings

**File:** `customer_service_bot.json`

**How to use:**
```bash
python scripts/import_example.py customer_service_bot.json
```

### 2. Trivia Bot

An interactive trivia game chatbot.

**Features:**
- Question generation
- Answer validation
- Score tracking
- Multiple categories

**File:** `trivia_bot.json`

**How to use:**
```bash
python scripts/import_example.py trivia_bot.json
```

### 3. Weather Assistant

Get weather information and forecasts.

**Features:**
- Location-based weather queries
- Forecast information
- Alert handling

**File:** `weather_assistant.json`

## Using Examples

### Quick Start

1. **In the UI:**
   - Click "Load Example"
   - Select an example
   - Train and export

2. **Via CLI:**
   ```bash
   python scripts/import_example.py <example_name>.json
   ```

### Customizing Examples

1. Download the JSON file
2. Edit intents, utterances, and responses
3. Upload back to trainer
4. Train and export

## 📝 JSON Format

```json
{
  "name": "Bot Name",
  "description": "What this bot does",
  "intents": [
    {
      "id": "unique_id",
      "name": "intent_name",
      "utterances": ["example1", "example2"],
      "responses": ["response1", "response2"],
      "entities": ["entity_type"]
    }
  ],
  "entities": [
    {
      "name": "entity_name",
      "type": "entity.type"
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "created_date": "2026-03-12",
    "language": "en"
  }
}
```

## Creating Your Own Template

1. Create a chatbot
2. Train and test it
3. Export as JSON (select "Save as Template")
4. Share with others!

---

Have a great example? [Contribute it!](../CONTRIBUTING.md)
