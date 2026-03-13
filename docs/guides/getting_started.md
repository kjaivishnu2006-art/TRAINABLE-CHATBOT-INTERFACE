# Getting Started Guide

Learn how to create your first chatbot in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- All dependencies installed (see [Setup Instructions](../../SETUP.md))

## Step 1: Launch the Application

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Start the training interface
python -m src.chatbot_builder.main
```

The application opens at **http://localhost:5000**

## Step 2: Create Your First Intent

### What is an Intent?

An **intent** represents what the user wants (e.g., "greeting", "get_weather", "tell_joke").

### Add Intent

1. Click **"+ New Intent"**
2. Enter name: `greeting`
3. Click **Create**

## Step 3: Add Training Utterances

**Utterances** are example sentences the user might say.

1. Click in the **Utterances** field
2. Add examples (one per line):
   ```
   Hello
   Hi
   Hey
   Good morning
   What's up
   ```
3. Click **Add Utterances**

## Step 4: Define Bot Responses

**Responses** are what the bot will say back.

1. Click in the **Responses** field
2. Add responses:
   ```
   Hi there! How can I help?
   Hello! What can I do for you?
   Hey! What do you need today?
   ```
3. Click **Add Responses**

## Step 5: Create More Intents

Repeat steps 2-4 to create another intent:

### Intent: "tell_joke"

**Utterances**:
- Tell me a joke
- Make me laugh
- Got any jokes?
- Tell me something funny

**Responses**:
- Why did the programmer quit his job? Because he didn't get arrays.
- How many programmers does it take to change a light bulb? None, that's a hardware problem!

## Step 6: Train the Model

1. Click **"Train Model"**
2. Review training settings:
   - **Epochs**: 10 (default)
   - **Batch size**: 32 (default)
   - **Learning rate**: 0.001 (default)
3. Click **"Start Training"**
4. Wait for training to complete (1-2 minutes)

**Training Progress**:
```
Epoch 1/10: loss=0.523, accuracy=0.89
Epoch 2/10: loss=0.312, accuracy=0.94
...
Training Complete!
Final Accuracy: 96%
```

## Step 7: Test Your Chatbot

The **Testing Console** lets you chat with your bot before exporting.

1. Click **"Testing Console"** tab
2. Type a message:
   ```
   Hey there!
   ```
3. See the response:
   ```
   Bot: Hi there! How can I help?
   Detected Intent: greeting (confidence: 0.96)
   ```

Try a few more:
- "Tell me a joke"
- "Hello"
- "Make me laugh"

## Step 8: Export Your Model

Ready to use your bot in an app? Export it!

1. Click **"Export Model"**
2. Review export settings:
   - **Model format**: TensorFlow Lite
   - **Quantization**: Enabled (reduces size)
   - **Include responses**: Yes
3. Click **"Export"**
4. Download `chatbot_package.zip`

**What's in the package?**
- `chatbot_model.tflite` - The AI model (~2MB)
- `responses.json` - Response templates
- `config.json` - Model configuration
- `README.md` - Integration instructions

## Step 9: Use in MIT App Inventor

### Import Model

1. Open your MIT App Inventor project
2. Go to **Media** section
3. Upload files from `chatbot_package.zip`:
   - `chatbot_model.tflite`
   - `responses.json`
   - `config.json`

### Add ChatBot Component

1. In **Designer**:
   - Go to **Extensions** → **Import Extension**
   - Upload `ChatBotComponent.aix`

2. In **Blocks**:
   - Add `ChatBot.LoadModel` block
   - Set model file to `chatbot_model.tflite`

3. Add chat logic:
   ```blocks
   When UserInput.TextChanged:
     set Response to ChatBot.GetResponse(UserInput.Text)
     set ResponseLabel.Text to Response
   ```

## 🎉 Congratulations!

You've created and deployed your first chatbot!

## Next Steps

- **[Advanced Training](advanced_training.md)** - Learn more techniques
- **[MIT App Inventor Integration](mit_app_inventor_integration.md)** - Deep dive integration
- **[API Reference](../api/training_api.md)** - Programmatic interface
- **[Examples](../../examples/)** - Pre-built templates

## 📖 Common Tasks

### Add More Intents

Repeat Steps 2-4. The model learns from all intents together.

### Improve Accuracy

Add more training examples per intent. More data = better performance.

### Update Bot Responses

Edit responses and retrain. The model will learn the new patterns.

### Use Different Languages

UTF-8 supported for most languages (Chinese, Spanish, Arabic, etc.)

### Add Entity Recognition

Mark important words with entity labels:
- User: "Book flight to **London** on **March 15**"
- Entities: destination="London", date="March 15"

### Handle Unknown Inputs

Add a "fallback" intent with generic utterances:
- "I don't know"
- "Not sure"
- "What?"

Responses:
- "Sorry, I didn't understand. Can you rephrase?"
- "Hmm, I'm not sure I got that. Try again?"

## 🆘 Troubleshooting

### Model won't train
- **Check**: Do you have at least 2 intents?
- **Check**: Each intent has at least 3 utterances?
- See [FAQ](faq.md)

### Low accuracy
- Add more training examples
- Use clearer utterances
- Review and fix data quality

### Export fails
- Check available disk space
- Ensure file permissions
- Restart application

## 📚 Learn More

- **[Architecture](../ARCHITECTURE.md)** - How it works
- **[FAQ](faq.md)** - Common questions
- **[Contributing](../../CONTRIBUTING.md)** - Help improve the project

---

**Ready to build more advanced chatbots?** → [Advanced Training Guide](advanced_training.md)
