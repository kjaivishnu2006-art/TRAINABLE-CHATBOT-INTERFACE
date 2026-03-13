# System Architecture

Complete overview of the Trainable ChatBot Builder system design.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│      Trainable ChatBot Builder Platform                  │
└─────────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │   Training   │   │   Export     │   │   Testing    │
    │   Interface  │   │   System     │   │   Console    │
    └──────────────┘   └──────────────┘   └──────────────┘
           ↓                    ↓                    ↓
    ┌────────────────────────────────────────────────────┐
    │        Model AI Layer (TensorFlow/Keras)           │
    └────────────────────────────────────────────────────┘
           ↓                             ↓
    ┌──────────────────────┐   ┌─────────────────────────┐
    │  Intent Classifier   │   │  Response Generator     │
    └──────────────────────┘   └─────────────────────────┘
           ↓
    ┌────────────────────────────────────────────────────┐
    │  Exported Package (.tflite + JSON files)           │
    └────────────────────────────────────────────────────┘
           ↓
    ┌────────────────────────────────────────────────────┐
    │    MIT App Inventor (Client Integration)           │
    └────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Training Interface (`src/chatbot_builder/`)

**Purpose**: Intuitive UI for creating chatbot training data

**Key Components**:
- `main.py` - Application entry point and server setup
- `gui.py` - Web-based user interface (Flask + Frontend)
- `intent_manager.py` - Intent CRUD operations
- `config.py` - Configuration management

**Data Model**:
```python
Intent:
  - id: string
  - name: string
  - utterances: List[string]  # User examples: ["Hi", "Hello"]
  - responses: List[string]   # Bot responses
  - entities: Dict[str, str]  # Named entity types

ChatBot:
  - intents: List[Intent]
  - entities: Dict[str, Type]  # Global entity definitions
  - metadata: Metadata         # Training info
```

### 2. Training Pipeline (`src/training/`)

**Purpose**: Models training and optimization

**Key Components**:
- `preprocessor.py` - Text tokenization, normalization, feature extraction
- `trainer.py` - TensorFlow model training orchestration
- `models.py` - Neural network architecture definitions
- `evaluator.py` - Model performance metrics

**Training Flow**:
```
Raw Data (Utterances) 
    ↓
[Preprocessing]
  - Tokenization
  - Normalization
  - Feature extraction
    ↓
[Model Training]
  - Build neural network
  - Train on labeled data
  - Validate performance
    ↓
[Evaluation]
  - Calculate accuracy
  - Precision/Recall/F1
  - Confusion matrix
    ↓
[Optimized Model]
```

**Model Architecture**:
```
Input: Text sequence
  ↓
[Embedding Layer] - Convert words to vectors
  ↓
[LSTM/GRU] - Capture sequential patterns
  ↓
[Dense Layer] - Feature transformation
  ↓
[Output Layer] - Intent probability distribution
  ↓
Output: Intent class + confidence score
```

### 3. Export System (`src/export/`)

**Purpose**: Converts trained model to deployable format

**Key Components**:
- `exporter.py` - TensorFlow to TFLite conversion
- `optimizer.py` - Model quantization and compression
- `packager.py` - ZIP package generation
- `validators.py` - Output validation

**Export Pipeline**:
```
Trained Model (TF SavedModel)
    ↓
[Conversion to TFLite]
  - Convert frozen graph
  - Optimize for mobile
    ↓
[Quantization] (Optional)
  - 8-bit integer quantization
  - Reduce model size ~3-4x
    ↓
[Packaging]
  - chatbot_model.tflite
  - responses.json
  - config.json
  - vocabulary.txt
    ↓
[Output Package]
  chatbot_package.zip (ready for MIT App Inventor)
```

## Data Flow

### Training Data Input

**User provides**:
```json
{
  "intents": [
    {
      "name": "greeting",
      "utterances": ["Hello", "Hi", "Hey there"],
      "responses": ["Hi! How can I help?", "Hello!"]
    },
    {
      "name": "joke",
      "utterances": ["Tell me a joke", "Make me laugh"],
      "responses": ["Why did the chicken..."]
    }
  ],
  "entities": {
    "name": "entity.name",
    "date": "entity.date"
  }
}
```

### Processing Pipeline

```
Input: "Hello there!"
  ↓
[Tokenizer]
  → ["hello", "there"]
  ↓
[Embedding]
  → [[0.2, -0.5, ...], [0.1, 0.3, ...]]
  ↓
[LSTM]
  → [Context vector]
  ↓
[Classifier]
  → {"greeting": 0.94, "joke": 0.03, "weather": 0.02}
  ↓
[Response Selection]
  → Select from greeting responses
  ↓
Output: "Hi! How can I help?"
```

## File Structure

### Input Files
- `training_data.json` - Intents and responses
- `utterances.csv` - Examples (optional)
- `config.yaml` - Training parameters

### Model Files
- `model_weights.h5` - Trained model weights
- `vocabulary.txt` - Word-to-index mapping
- `tokenizer.json` - Tokenizer configuration

### Output Files
- `chatbot_model.tflite` - Optimized inference model
- `responses.json` - Response templates
- `config.json` - Model metadata
- `chatbot_package.zip` - Complete export

## Integration with MIT App Inventor

### Import Process
1. User downloads `chatbot_package.zip`
2. Extracts files to MIT App Inventor project assets
3. Adds `ChatBot` component to app
4. Configures component with model path
5. Calls inference blocks in app logic

### Runtime Execution
```
User Input (Text)
  ↓
[App Block: ChatBot.GetResponse(text)]
  ↓
[TFLite Interpreter]
  - Loads model on-device
  - Runs inference
  - Returns intent + response
  ↓
[App updates UI with response]
```

## Performance Characteristics

### Training
- **Time**: 1-10 minutes (depends on dataset size)
- **Memory**: 500MB - 2GB
- **CPU Usage**: High during training

### Inference (Per request)
- **Latency**: 50-200ms (on mobile device)
- **Memory**: 20-50MB (model loaded once)
- **Disk**: 2-5MB (model file size)

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| ML Framework | TensorFlow | 2.13.0 |
| Mobile Inference | TensorFlow Lite | 2.13.0 |
| Backend | Flask | 2.2.0 |
| Frontend | HTML/CSS/JavaScript | ES6+ |
| NLP | NLTK, spaCy | Latest |
| Scripting | Python | 3.8+ |

## Security Considerations

1. **Data Privacy**
   - Models trained locally (option for cloud)
   - Personal data not uploaded to servers
   - GDPR compliant

2. **Model Security**
   - Exported models are self-contained
   - No external API calls after export
   - On-device execution only

3. **Access Control**
   - User authentication (if online)
   - API rate limiting
   - Input validation

## Future Enhancements

- [ ] Multi-language support
- [ ] Dialogue state management
- [ ] Sentiment analysis
- [ ] Entity linking
- [ ] Active learning from user feedback
- [ ] Model federated learning

---

[Back to Documentation](index.md)
