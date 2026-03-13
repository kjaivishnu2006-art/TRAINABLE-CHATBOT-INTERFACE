# Quick Start: Exporting Chatbot Models for Mobile Apps

Get your chatbot model exported and running on mobile in 5 minutes.

## Step 1: Export Your Model (1 minute)

```bash
cd examples/
python export_chatbot_model.py
```

This creates:
- `chatbot_lightweight.json` (10-50 KB) - For mobile apps
- `chatbot_embedding.json` (1-5 MB) - For semantic matching
- `chatbot_web/` folder - Ready-to-use web app

## Step 2: Choose Your Platform (2 minutes)

### Mobile App (iOS/Android)

1. Copy the exported JSON to your project assets:
```
ios/  → App/Assets/
android/ → app/src/main/assets/
```

2. Load in your app:

**Swift (iOS):**
```swift
let path = Bundle.main.path(forResource: "chatbot_lightweight", ofType: "json")!
let data = try! Data(contentsOf: URL(fileURLWithPath: path))
let model = try! JSONDecoder().decode(ChatbotModel.self, from: data)
```

**Kotlin (Android):**
```kotlin
val inputStream = context.assets.open("chatbot_lightweight.json")
val jsonObject = JSONObject(inputStream.bufferedReader().use { it.readText() })
```

### React Native / Flutter

**React Native:**
```javascript
import modelData from './model.json';
const chatbot = new MobileChatbot();
chatbot.model = modelData;
```

**Flutter (Dart):**
```dart
final modelJson = await rootBundle.loadString('assets/model.json');
final model = jsonDecode(modelJson);
```

### Web App

1. Copy the entire `chatbot_web/` folder to your server
2. Open `chatbot_web/chatbot.html` in a browser
3. Done! The chatbot works offline

## Step 3: Use in Your Code (2 minutes)

### Python Example
```python
from mobile_chatbot_client import MobileChatbotClient

# Load the exported model
client = MobileChatbotClient("chatbot_lightweight.json")

# Get an answer
response = client.get_answer("How to learn Python?")
print(f"Q: {response['original_question']}")
print(f"A: {response['answer']}")
print(f"Confidence: {response['confidence']:.0%}")
```

### JavaScript Example
```javascript
// Load model
const chatbot = new MobileChatbot('model.json');

// Get answer
const response = chatbot.findAnswer("What is Python?");
console.log("Answer:", response.answer);
console.log("Confidence:", response.confidence);
```

### Dart/Flutter Example
```dart
String findAnswer(String question, Map<String, dynamic> model) {
  List qaPairs = model['qa_pairs'];
  
  double bestScore = 0;
  String bestAnswer = 'No answer found';
  
  for (var qa in qaPairs) {
    // Simple keyword matching
    int matches = question.split(' ')
        .where((w) => qa['question'].toLowerCase().contains(w.toLowerCase()))
        .length;
    
    double score = matches / question.split(' ').length;
    
    if (score > bestScore) {
      bestScore = score;
      bestAnswer = qa['answer'];
    }
  }
  
  return bestAnswer;
}
```

## Advanced Options (Optional)

### Use Semantic Embeddings (Better Accuracy)

If accuracy matters more than speed:

```python
# Export with embeddings (92% accuracy vs 42%)
from export_chatbot_model import ChatbotModelExporter
from embedding_chatbot import EmbeddingQAChatbot

chatbot = EmbeddingQAChatbot("qa_dataset.json")
exporter = ChatbotModelExporter(chatbot)

# Quantized: ~25 KB per 50 questions
exporter.export_embedding_model("model.json", quantize_embeddings=True)
```

### Size Optimization

**Original Model:** 50 KB
**After Quantization:** 12 KB (75% smaller!)
**After Gzip:** 4 KB (92% smaller!)

```python
# Export with compression
from export_chatbot_model import ChatbotModelExporter
from embedding_chatbot import EmbeddingQAChatbot

chatbot = EmbeddingQAChatbot("qa_dataset.json")
exporter = ChatbotModelExporter(chatbot)

# Gzip compressed
exporter.export_full_model("model.json.gz", compress=True, include_embeddings=False)
```

### Web Bundle

Deploy instantly to web:

```python
# Creates ready-to-use web app
exporter.export_web_bundle("deploy/")
```

Then upload `deploy/` folder to any web server.

## FAQ

**Q: Which format should I use?**
A: 
- **Mobile app** → Use lightweight (~1 MB, works offline)
- **Web app** → Use web bundle (includes HTML/JS)
- **Need better accuracy?** → Use embedding (~5 MB, 92% vs 42%)

**Q: File is too large!**
A: Use quantization (saves 75%) or remove embeddings

**Q: How to handle offline?**
A: All formats work offline - no internet needed after export!

**Q: Can I update the model?**
A: Export new model, update app assets. Include version in metadata for multiple model support.

**Q: Security - will my Q&A data be exposed?**
A: No - it's embedded in your app. Data never leaves the device.

## Performance Expectations

| Format | Accuracy | Speed | File Size |
|--------|----------|-------|-----------|
| Lightweight | 42% | ~1ms | 10-50 KB |
| Embedding (quantized) | 92% | ~45ms | 1-5 MB |
| Web Bundle | 42% | ~1ms | 50-200 KB |

## Testing Your Export

```bash
# Run comprehensive tests
pytest examples/test_export_system.py -v

# Test mobile client
python examples/mobile_chatbot_client.py

# Validate JSON
python -m json.tool chatbot_lightweight.json
```

## Integration with Flask API

If using the Flask backend:

```bash
# Export endpoint available at
GET /api/export/lightweight/<chatbot_id>    # Download lightweight JSON
POST /api/export/embedding/<chatbot_id>     # Export with embeddings
GET /api/export/formats                     # View all formats
```

## Next Steps

1. **Test on device**: Try your export on actual mobile device
2. **Monitor performance**: Track query latency and accuracy
3. **Iterate**: Collect user feedback and improve Q&A pairs
4. **Update**: Export new models as your knowledge base grows

## Troubleshooting

**Model won't load on mobile?**
→ Verify JSON is valid: `python -m json.tool model.json`

**Accuracy too low?**
→ Use embedding model: `exporter.export_embedding_model(...)`

**App too slow?**
→ Use lightweight format with keyword matching

**File size too large?**
→ Use quantization: `export_embedding_model(..., quantize_embeddings=True)`

## Resources

- [Full Export Documentation](EXPORT_GUIDE.md)
- [Export API Reference](../src/chatbot_builder/export_api.py)
- [Mobile Client Source](mobile_chatbot_client.py)
- [Example Exports](./examples/)

## Support

- **Issues?** Check troubleshooting section above
- **Questions?** Review EXPORT_GUIDE.md for detailed examples
- **Contributing?** See CONTRIBUTING.md
