# JSON Dataset Format for Chatbot Training

## Overview

This document explains the JSON dataset format used for training chatbot models in the Trainable ChatBot Builder.

## File Structure

The complete dataset structure includes:

```json
{
  "metadata": { ... },
  "entities": [ ... ],
  "intents": [ ... ],
  "training_config": { ... },
  "statistics": { ... }
}
```

## Sections Explained

### 1. Metadata

```json
"metadata": {
  "version": "1.0.0",
  "name": "General Assistant Chatbot",
  "description": "A multi-intent chatbot dataset for training",
  "language": "en",
  "created_date": "2026-03-12",
  "author": "Chatbot Builder",
  "license": "MIT"
}
```

**Fields:**
- `version` - Dataset version (semantic versioning)
- `name` - Dataset name
- `description` - What this dataset is for
- `language` - Primary language (ISO 639-1 code)
- `created_date` - Creation date
- `author` - Who created it
- `license` - License type

### 2. Entity Definitions

```json
"entities": [
  {
    "entity_id": "entity.name",
    "entity_type": "NAME",
    "description": "Person's name or entity name",
    "examples": ["John", "Alice", "Company X"]
  }
]
```

**Fields:**
- `entity_id` - Unique identifier (usually `entity.TYPE`)
- `entity_type` - Type name in uppercase
- `description` - What this entity represents
- `examples` - Sample values for this entity

**Common Entity Types:**
- `NAME` - Person or entity names
- `DATE` - Dates and times
- `LOCATION` - Geographic locations
- `PRODUCT` - Products or services
- `EMAIL` - Email addresses
- `PHONE` - Phone numbers
- `NUMBER` - Numeric values
- `URL` - Web URLs
- `TIME` - Time references

### 3. Intent Definitions

```json
"intents": [
  {
    "intent_id": "greeting",
    "intent_name": "greeting",
    "description": "User greets the chatbot",
    "priority": "high",
    "utterances": [
      "hello",
      "hi there",
      "hey"
    ],
    "responses": [
      "Hello! How can I help you today?",
      "Hi there! What can I do for you?"
    ],
    "entities": [],
    "context": {
      "requires_context": false,
      "sets_context": "greeting_acknowledged"
    }
  }
]
```

**Intent Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `intent_id` | string | Unique identifier (no spaces, lowercase) |
| `intent_name` | string | Human-readable name |
| `description` | string | What this intent represents |
| `priority` | enum | `high`, `medium`, `low` |
| `utterances` | array | User input examples (8-10 recommended) |
| `responses` | array | Bot response options (5+ recommended) |
| `entities` | array | Entity IDs used in this intent |
| `context` | object | Context flow management |

**Context Field:**
```json
"context": {
  "requires_context": false,      // Does this need conversation history?
  "sets_context": "meeting_scheduled"  // What context does it create?
}
```

### 4. Training Configuration

```json
"training_config": {
  "epochs": 10,
  "batch_size": 32,
  "learning_rate": 0.001,
  "validation_split": 0.2,
  "random_seed": 42
}
```

**Parameters:**
- `epochs` - Number of training iterations
- `batch_size` - Examples per training batch
- `learning_rate` - Model learning rate
- `validation_split` - Percentage of data for validation (0-1)
- `random_seed` - Reproducibility seed

### 5. Statistics

```json
"statistics": {
  "total_intents": 10,
  "total_entities": 4,
  "total_utterances": 80,
  "average_utterances_per_intent": 8,
  "total_responses": 50,
  "min_utterances_per_intent": 8,
  "max_utterances_per_intent": 8
}
```

Auto-generated statistics about the dataset.

## Best Practices

### Utterances

1. **Diversity**: Use varied phrasings for the same intent
   ```json
   "utterances": [
     "hello",           // Simple
     "hi there",        // Casual
     "good morning",    // With time reference
     "hey bot",         // Addressing bot
     "greetings"        // Formal
   ]
   ```

2. **Realistic**: Use actual user language patterns
   - ✅ "What's the weather?" (natural)
   - ❌ "Query meteorological data" (unnatural)

3. **Quantity**: 8-15 examples per intent
   - Too few: Model underfits (can't generalize)
   - Too many: Diminishing returns, slower training

4. **Entities in Utterances**: Mark with curly braces
   ```json
   "utterances": [
     "Schedule meeting with {name}",
     "Meet with {name} on {date}",
     "Book {name} for {date}"
   ]
   ```

### Responses

1. **Variety**: Multiple response options prevent repetition
   ```json
   "responses": [
     "Sure! I can help.",
     "Of course, what do you need?",
     "Happy to help you."
   ]
   ```

2. **Consistency**: All responses fit the intent
   - ✅ For "greeting": "Hello! How can I help?"
   - ❌ For "greeting": "Your order is ready" (wrong intent)

3. **Natural**: Use conversational language
4. **Parameters**: Use {variable} for dynamic content
   ```json
   "responses": [
     "I'll schedule your {product} for {date}",
     "Your meeting with {name} is confirmed"
   ]
   ```

### Intents

1. **Naming**: Use lowercase with underscores
   - ✅ `schedule_meeting`, `ask_weather`
   - ❌ `ScheduleMeeting`, `ASK-WEATHER`

2. **One Purpose**: Each intent should have one clear goal
3. **No Overlap**: Intents should be clearly distinct
4. **Complete Coverage**: Cover expected user interactions

### Entities

1. **Reference**: Use `entity_id` format for referencing
2. **Types**: Use standard uppercase types
3. **Reusable**: Entities can be used across multiple intents
4. **Examples**: Provide clear examples

## Example Workflow

### Step 1: Define Entities

What information will the bot need to extract?

```json
"entities": [
  {
    "entity_id": "entity.name",
    "entity_type": "NAME",
    "description": "User or contact name"
  }
]
```

### Step 2: Define Intents

What does the user want to do?

```json
"intents": [
  {
    "intent_id": "make_appointment",
    "description": "User wants to make an appointment",
    "entities": ["entity.name", "entity.date"]
  }
]
```

### Step 3: Add Utterances

How will users express this intent?

```json
"utterances": [
  "Schedule appointment with {name}",
  "Book a meeting on {date}",
  "I need to see {name} {date}"
]
```

### Step 4: Add Responses

What should the bot say?

```json
"responses": [
  "I'll schedule your appointment with {name} on {date}",
  "Your appointment is confirmed"
]
```

## Dataset Statistics

A well-balanced dataset has:

- **Intents**: 5-50 intents (depends on domain)
- **Utterances per intent**: 8-20 (minimum 5)
- **Responses per intent**: 3-10
- **Entities**: 5-30 (reused across intents)
- **Total utterances**: 100+ (more is better)

**Example Good Dataset:**
- 30 intents
- 12 utterances per intent
- 6 responses per intent
- 15 entities
- 360 total utterances

## Common Patterns

### Dialogue Flow with Context

```json
{
  "intent_id": "order_coffee",
  "utterances": ["order coffee"],
  "context": {
    "requires_context": false,
    "sets_context": "order_in_progress"
  }
},
{
  "intent_id": "specify_size",
  "utterances": ["small", "large", "medium"],
  "context": {
    "requires_context": "order_in_progress",
    "sets_context": "size_specified"
  }
}
```

### Multiple Entity Types

```json
{
  "intent_id": "schedule_meeting",
  "utterances": [
    "Meet with {name} on {date}",
    "Schedule {name} for {date} at {location}"
  ],
  "entities": ["entity.name", "entity.date", "entity.location"]
}
```

### Fallback Intent

Always include a fallback for unknown inputs:

```json
{
  "intent_id": "fallback",
  "utterances": [
    "I don't know",
    "xyz abc",
    "random text",
    "???"
  ],
  "responses": [
    "Sorry, I don't understand. Can you rephrase?",
    "That's not something I can help with"
  ]
}
```

## Validation Checklist

Before using your dataset:

- [ ] All intent IDs are unique and lowercase
- [ ] Each intent has 8+ utterances
- [ ] Each intent has 3+ responses
- [ ] Entity references exist in `entities` section
- [ ] No typos in entity IDs
- [ ] Valid JSON syntax
- [ ] Metadata is complete
- [ ] Statistics are accurate

## Tools for Creation

### Using Python

```python
import json

dataset = {
    "metadata": { ... },
    "entities": [ ... ],
    "intents": [ ... ]
}

# Save
with open("my_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

# Load
with open("my_dataset.json") as f:
    data = json.load(f)
```

### Validate JSON

```bash
# Online validator
# https://jsonlint.com

# Python
python -m json.tool my_dataset.json
```

## Version Control

When modifying datasets:

1. Update `metadata.version`
2. Add changelog entry
3. Increment appropriately (1.0.0 → 1.0.1)

```json
"metadata": {
  "version": "1.0.1",
  "changes": "Added 5 new intents for payment processing"
}
```

---

**See Also:**
- [training_dataset.json](training_dataset.json) - Complete example
- [Getting Started Guide](../guides/getting_started.md) - How to use datasets
- [Training API](../../docs/api/training_api.md) - API documentation
