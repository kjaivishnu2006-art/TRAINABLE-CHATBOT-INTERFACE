# Simple Q&A Chatbot Example

A straightforward chatbot implementation that reads Q&A pairs from a JSON dataset and answers user questions using keyword matching.

## Features

✅ **JSON-based Q&A storage** - Easy to add and modify questions/answers  
✅ **Keyword matching** - Smart matching using question keywords  
✅ **Confidence scoring** - Shows how confident the bot is about its answer  
✅ **Text preprocessing** - Handles punctuation and normalizes input  
✅ **Interactive chat** - Run natural conversations with the bot  
✅ **Fully tested** - Comprehensive unit tests included  

## How It Works

1. **Load Dataset**: Reads Q&A pairs from JSON file
2. **Preprocess Input**: Cleans user input (punctuation, case)
3. **Calculate Similarity**: Compares input against questions and keywords
4. **Return Answer**: Returns best match if above confidence threshold

## Quick Start

### Run Interactive Chat

```bash
# Make sure you're in the examples directory
cd examples

# Run the chatbot
python simple_chatbot.py
```

**Chat with the bot:**
```
You: What is Python?
Chatbot: Python is a high-level, interpreted programming language...
(Confidence: 92%)

You: How do I install packages?
Chatbot: Use pip to install packages: pip install package_name...
(Confidence: 87%)
```

### Programmatic Usage

```python
from simple_chatbot import SimpleQAChatbot

# Initialize
chatbot = SimpleQAChatbot("qa_dataset.json")

# Get answer
answer, confidence = chatbot.find_answer("How do I learn Python?")
print(f"Answer: {answer}")
print(f"Confidence: {int(confidence * 100)}%")

# List all questions
chatbot.list_questions()
```

## Dataset Format

**File: `qa_dataset.json`**

```json
{
  "chatbot_name": "My Chatbot",
  "description": "A helpful assistant",
  "qa_pairs": [
    {
      "id": 1,
      "question": "What is Python?",
      "keywords": ["python", "programming"],
      "answer": "Python is a programming language..."
    }
  ]
}
```

### Required Fields
- `qa_pairs` - Array of Q&A objects
- `question` - The question text
- `answer` - The response text

### Optional Fields
- `chatbot_name` - Display name (default: "Chatbot")
- `keywords` - List of relevant keywords for better matching
- `id` - Question identifier

## Similarity Matching Algorithm

The chatbot calculates similarity using:

```
Score = (Question Match × 0.75) + (Keyword Match × 0.25)
```

Where:
- **Question Match**: Overlapping words between input and question
- **Keyword Match**: Overlapping words between input and keywords
- **Threshold**: Default 0.3 (30%) - can be adjusted

Higher scores mean better matches.

## Running Tests

```bash
# Run all tests
pytest test_simple_chatbot.py -v

# Run specific test
pytest test_simple_chatbot.py::test_find_answer_exact_match -v

# Run with coverage
pytest test_simple_chatbot.py --cov
```

**Test Coverage:**
```
test_chatbot_initialization.py       PASSED
test_chatbot_file_not_found.py       PASSED
test_preprocess_text.py              PASSED
test_find_answer_exact_match.py      PASSED
test_find_answer_partial_match.py    PASSED
test_find_answer_no_match.py         PASSED
test_find_answer_empty_input.py      PASSED
test_similarity_calculation.py       PASSED
```

## Chat Commands

**During Interactive Chat:**

| Command | Description |
|---------|-------------|
| `quit` | Exit the chatbot |
| `help` | Show available commands |
| `list` | Show all Q&A topics |

## Customization

### Add More Q&A Pairs

Edit `qa_dataset.json`:

```json
{
  "qa_pairs": [
    // ... existing pairs ...
    {
      "id": 11,
      "question": "What is Docker?",
      "keywords": ["docker", "containers", "deployment"],
      "answer": "Docker is a containerization platform that packages applications..."
    }
  ]
}
```

### Adjust Confidence Threshold

```python
# More strict (requires higher confidence)
answer, confidence = chatbot.find_answer("What is Python?", threshold=0.5)

# More lenient
answer, confidence = chatbot.find_answer("What is Python?", threshold=0.2)
```

### Create Custom Q&A Dataset

```python
import json

dataset = {
    "chatbot_name": "My Custom Bot",
    "qa_pairs": [
        {
            "id": 1,
            "question": "Your question?",
            "keywords": ["keyword1", "keyword2"],
            "answer": "Your answer here."
        }
    ]
}

with open("my_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)
```

## Architecture

```
SimpleQAChatbot
├── _load_dataset()         # Load JSON Q&A pairs
├── _preprocess_text()      # Clean and normalize text
├── _calculate_similarity() # Score matching
├── find_answer()           # Get best answer
├── chat()                  # Interactive mode
└── list_questions()        # Show all Q&As
```

## Limitations

- **Keyword-based** - No NLP/ML, simple word matching
- **One-turn** - No conversation history or context
- **Exact phrases** - Doesn't understand paraphrasing
- **No learning** - Doesn't improve from interactions

## Next Steps

To make this more sophisticated:

1. **Add NLP**: Use `spaCy` or `NLTK` for better understanding
2. **Add Context**: Track conversation history
3. **Use ML**: Train intent classifier (like in main project)
4. **Add Entities**: Extract names, dates, etc.
5. **Sentiment Analysis**: Detect user emotion
6. **Multi-language**: Support multiple languages

## Examples

### Customer Service Bot

See `customer_service_bot.json` for a ready-to-use example:

```bash
python -c "
from simple_chatbot import SimpleQAChatbot
bot = SimpleQAChatbot('customer_service_bot.json')
answer, conf = bot.find_answer('Where is my order?')
print(f'{answer} (Confidence: {int(conf*100)}%)')
"
```

### Trivia Bot

See `trivia_bot.json` for a fun interactive example:

```bash
python simple_chatbot.py  # Then run trivia bot
```

## File Structure

```
examples/
├── simple_chatbot.py           # Main chatbot class
├── simple_chatbot_test.py      # Unit tests
├── qa_dataset.json             # Sample Q&A dataset
├── customer_service_bot.json   # Customer service template
├── trivia_bot.json             # Trivia game template
└── README.md                   # This file
```

---

**Ready to get started?** Run `python simple_chatbot.py` now! 🚀
