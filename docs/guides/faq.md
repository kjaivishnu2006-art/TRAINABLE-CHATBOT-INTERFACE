# FAQ - Frequently Asked Questions

## General

### What is Trainable ChatBot Builder?

A no-code platform that lets educators and students train custom chatbots using TensorFlow, then deploy them in MIT App Inventor apps without needing machine learning expertise.

### Who should use this?

- Computer science teachers introducing AI/ML
- Students building AI-powered mobile apps
- Anyone prototyping conversational AI quickly
- Educators in K-12, college, or bootcamps

### Does it cost anything?

No! The project is open-source MIT licensed. Free to use, modify, and share.

### What platforms are supported?

- **Training**: Windows, macOS, Linux
- **Deployment**: Android (via MIT App Inventor)
- **Models**: Run on any device that supports TensorFlow Lite

## Getting Started

### I'm new to machine learning. Can I still use this?

**Absolutely!** That's the entire point. Zero ML experience needed:
- Intuitive UI for creating intents/responses
- Automatic model training
- One-click export
- Just provide examples

### How do I install it?

See [SETUP.md](../../SETUP.md) - takes 5 minutes.

### I'm having trouble installing dependencies. Help?

Check [SETUP.md - Troubleshooting](../../SETUP.md#troubleshooting) section. If still stuck:
- Open [GitHub Issue](https://github.com/your-org/trainable-chatbot/issues)
- Ask in [GitHub Discussions](https://github.com/your-org/trainable-chatbot/discussions)

### How do I create my first chatbot?

See [Getting Started Guide](getting_started.md) - 5 minute tutorial!

## Training

### How many training examples do I need?

**Minimum**: 3-5 examples per intent  
**Recommended**: 10-20 per intent for good accuracy  
**Best**: 50+ per intent for production

More examples = better accuracy.

### What if I have unbalanced data?

(e.g., "greeting" has 50 examples, "joke" has 5)

The trainer handles this, but model will be biased toward overrepresented intents. Add more examples to underrepresented ones.

### How long does training take?

Usually **1-5 minutes** depending on:
- Number of intents
- Examples per intent
- Hardware capabilities
- Number of epochs

### Why is my accuracy low?

Possible causes:
1. **Not enough training data** - Add more examples
2. **Poor quality data** - Review/clean examples
3. **Similar intents** - Make intent definitions clearer
4. **Too few epochs** - Train longer
5. **Bad utterances** - Use real user language

### Can I train in other languages?

Yes! UTF-8 supports:
- Spanish, French, German
- Chinese, Japanese, Korean
- Arabic, Hindi, Russian
- And many more!

### How do I improve model accuracy?

1. Add more training examples
2. Ensure examples are representative
3. Train for more epochs
4. Reduce number of intents (more focused)
5. Use active learning (test → collect failures → retrain)

### Can I see training progress?

Yes! The UI shows:
- Epoch number and loss
- Accuracy metrics
- Training time
- Progress bar

### What if training fails?

Check:
- Minimum 2 intents required?
- Each intent has at least 3 utterances?
- Valid UTF-8 encoding?
- Sufficient disk space?

See [SETUP.md - Troubleshooting](../../SETUP.md#troubleshooting)

## Model Export

### What does the export include?

```
chatbot_package.zip
├── chatbot_model.tflite      (AI model)
├── responses.json            (Response templates)
├── config.json               (Configuration)
├── vocabulary.txt            (Word mapping)
└── README.md                 (Integration guide)
```

### How large is the exported model?

Typically **2-5 MB** after export. TensorFlow Lite is optimized for mobile!

### Can I use the model offline?

**Yes!** That's the whole point. Models run completely on-device. No internet needed.

### Can I update the model later?

Yes. Train again and export new version. Replace files in your app.

## MIT App Inventor Integration

### How do I import the model into MIT App Inventor?

See [MIT App Inventor Integration Guide](mit_app_inventor_integration.md)

Quick summary:
1. Upload `.tflite` file to app assets
2. Add ChatBot component
3. Load model in blocks
4. Call inference on text input

### Do I need the MIT App Inventor extension?

Yes, if it's not built-in. You'll import a `.aix` file (custom extension).

### What's the response latency?

Typically **50-200ms** per inference on mobile devices.

### How much memory does it use?

**~20-50 MB** when loaded (very reasonable for mobile).

### Can I use this with other platforms besides MIT App Inventor?

Yes! Export as TensorFlow Lite, use in any TFLite-compatible platform:
- Flutter
- React Native
- Native Android/iOS
- Web (TensorFlow.js)

## Troubleshooting

### "Model not found" error

**Check:**
1. Did you upload the `.tflite` file?
2. Is the filename correct?
3. Is it in the project assets?

### Model gives nonsensical responses

**Likely causes:**
1. Poorly trained model (low accuracy) → add more data
2. Wrong responses being returned → check responses.json
3. Intent mismatch → review test results

### Export button is disabled

**Reasons:**
1. Model hasn't been trained
2. Training failed
3. No intents defined
4. No utterances added

Train first, then export.

### "Out of memory" during training

**Solutions:**
1. Reduce batch size (CLI: `--batch-size 8`)
2. Use fewer intents
3. Reduce training examples
4. Close other applications
5. Upgrade RAM (if possible)

### Can't connect to app builder on localhost

**Try:**
```bash
# Access from different machine
http://<your-computer-ip>:5000

# Or check port usage
netstat -an | grep 5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows
```

## Advanced Topics

### Can I use pre-trained models?

Not yet, but it's on the roadmap. Currently trains from scratch.

### What about entity recognition?

Basic entity support is available. More advanced NER coming soon.

### How do I implement dialogue state?

Currently stateless per-turn. Complex dialogue flows can be managed in the MIT App Inventor app logic.

### Can I track model performance?

Export includes accuracy metrics. App should log predictions for analysis.

### What about privacy and data?

- **Training data** stays on your machine (unless using cloud option)
- **Exported models** run completely offline
- **No personal data** is transmitted
- **GDPR compliant**

## Reporting Issues

### Found a bug?

1. Check existing [issues](https://github.com/your-org/trainable-chatbot/issues)
2. [Report new issue](https://github.com/your-org/trainable-chatbot/issues/new?template=bug_report.md)
3. Include:
   - Steps to reproduce
   - Python version
   - Error messages
   - Operating system

### Feature request?

[Suggest feature](https://github.com/your-org/trainable-chatbot/issues/new?template=feature_request.md) in GitHub Issues.

### Need help?

- Ask in [GitHub Discussions](https://github.com/your-org/trainable-chatbot/discussions)
- Email: [support@example.com](mailto:support@example.com)

## Contributing

### Can I contribute?

**Yes please!** See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### What areas need help?

- Bug fixes
- Feature implementations  
- Documentation improvements
- Example chatbots
- Language support
- Testing

---

**Still have questions?** [Open a discussion!](https://github.com/your-org/trainable-chatbot/discussions)
