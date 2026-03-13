# CLI Reference

Command-line interface documentation for the Trainable ChatBot Builder.

## Installation

### Via pip

```bash
pip install trainable-chatbot-builder
```

### From source

```bash
git clone https://github.com/your-org/trainable-chatbot.git
cd trainable-chatbot
pip install -e .
```

## Commands

### Start Training Interface

Launch the web-based training interface:

```bash
chatbot-builder
```

**Options:**
```bash
chatbot-builder --port 5000           # Custom port
chatbot-builder --host 0.0.0.0        # Listen on all interfaces
chatbot-builder --debug               # Enable debug mode
```

### Train Model

Train a model from command line:

```bash
chatbot-builder train \
  --input training_data.json \
  --output models/my_bot \
  --epochs 10 \
  --batch-size 32
```

**Options:**
- `--input` - Path to training data JSON file (required)
- `--output` - Output directory for trained model (required)
- `--epochs` - Number of training epochs (default: 10)
- `--batch-size` - Batch size for training (default: 32)
- `--learning-rate` - Learning rate (default: 0.001)
- `--validation-split` - Validation split ratio (default: 0.2)
- `--verbose` - Show detailed training output (flag)

### Evaluate Model

Evaluate model performance:

```bash
chatbot-builder evaluate \
  --model models/my_bot/model.h5 \
  --test-data test_utterances.json
```

**Options:**
- `--model` - Path to trained model (required)
- `--test-data` - Test data JSON file (required)
- `--metric` - Metric to evaluate: accuracy, precision, recall, f1 (default: accuracy)

### Export Model

Export trained model to TensorFlow Lite:

```bash
chatbot-builder export \
  --model models/my_bot \
  --output exports/my_bot_v1 \
  --quantize
```

**Options:**
- `--model` - Path to trained model (required)
- `--output` - Output directory (required)
- `--quantize` - Enable quantization (flag)
- `--optimize` - Enable optimization (flag)
- `--format` - Export format: tflite, savedmodel (default: tflite)

### Test Model

Test model interactively:

```bash
chatbot-builder test \
  --model models/my_bot/model.h5 \
  --vocab models/my_bot/vocabulary.txt
```

**Options:**
- `--model` - Path to trained model (required)
- `--vocab` - Path to vocabulary file (required)
- `--responses` - Path to responses JSON file

### Import Example

Load a pre-built example:

```bash
chatbot-builder import-example \
  --example customer_service_bot
```

**Available examples:**
- `customer_service_bot`
- `trivia_bot`
- `weather_assistant`

### Validate Data

Check training data format:

```bash
chatbot-builder validate \
  --input training_data.json
```

**Checks:**
- Valid JSON format
- All required fields present
- Minimum utterances per intent
- No duplicate intents
- Valid entity types

## Examples

### Training Workflow

```bash
# 1. Create training data
# (See examples/ directory or create your own)

# 2. Validate data
chatbot-builder validate --input my_chatbot.json

# 3. Train model
chatbot-builder train \
  --input my_chatbot.json \
  --output ./models/my_bot

# 4. Evaluate
chatbot-builder evaluate \
  --model ./models/my_bot/model.h5 \
  --test-data test_data.json

# 5. Test interactively
chatbot-builder test \
  --model ./models/my_bot/model.h5 \
  --vocab ./models/my_bot/vocabulary.txt

# 6. Export
chatbot-builder export \
  --model ./models/my_bot \
  --output ./exports/chatbot_v1 \
  --quantize
```

### Docker Usage

```bash
# Build image
docker build -t trainable-chatbot .

# Run container
docker run -p 5000:5000 trainable-chatbot

# Train with volume mount
docker run \
  -v $(pwd)/data:/app/data \
  trainable-chatbot \
  chatbot-builder train \
  --input /app/data/training.json \
  --output /app/data/models
```

## Configuration

### Config File

Create `chatbot-config.yml`:

```yaml
training:
  epochs: 10
  batch_size: 32
  learning_rate: 0.001
  validation_split: 0.2

model:
  embedding_dim: 128
  max_sequence_length: 20
  lstm_units: 64

export:
  quantize: true
  format: tflite
  optimize: true
```

Use config:
```bash
chatbot-builder train \
  --input training_data.json \
  --config chatbot-config.yml
```

## Troubleshooting

### "Command not found: chatbot-builder"

```bash
# Verify installation
pip list | grep trainable-chatbot

# Reinstall if needed
pip install --upgrade trainable-chatbot-builder

# Use full path
python -m src.chatbot_builder.main
```

### Memory errors during training

```bash
# Reduce batch size
chatbot-builder train \
  --input data.json \
  --batch-size 8 \
  --output models/bot
```

### Poor model accuracy

```bash
# Add more training data
# Add more epochs
chatbot-builder train \
  --input data.json \
  --epochs 20 \
  --output models/bot

# Check data quality
chatbot-builder validate --input data.json
```

## Environment Variables

```bash
# Set during startup
export FLASK_ENV=production
export MODEL_OUTPUT_DIR=./models/
export LOG_LEVEL=INFO

chatbot-builder
```

## Getting Help

```bash
chatbot-builder --help
chatbot-builder train --help
chatbot-builder export --help
```

---

[Back to API Reference](.)
