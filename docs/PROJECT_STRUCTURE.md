# Project Structure Overview

```
trainable-chatbot/
│
├── 📄 Root Configuration Files
│   ├── README.md                    # Project overview & quick start
│   ├── LICENSE                      # MIT License
│   ├── CONTRIBUTING.md              # Contribution guidelines
│   ├── CODE_OF_CONDUCT.md           # Community standards
│   ├── SETUP.md                     # Detailed setup instructions
│   ├── .gitignore                   # Git ignore patterns
│   ├── requirements.txt             # Python dependencies
│   ├── requirements-dev.txt         # Development dependencies
│   └── setup.py                     # Package installation
│
├── 📁 .github/
│   ├── workflows/
│   │   ├── tests.yml               # Automated testing on push/PR
│   │   ├── lint.yml                # Code quality checks
│   │   └── publish.yml             # Release automation
│   │
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md           # Bug report template
│       ├── feature_request.md      # Feature request template
│       └── documentation.md        # Documentation template
│
├── 📁 src/                          # Source code
│   │
│   ├── chatbot_builder/            # Training interface module
│   │   ├── __init__.py
│   │   ├── main.py                # CLI entry point
│   │   ├── gui.py                 # Web UI (Flask/React)
│   │   ├── intent_manager.py      # Intent CRUD operations
│   │   ├── config.py              # Configuration
│   │   └── utils.py               # Helper functions
│   │
│   ├── training/                   # Model training module
│   │   ├── __init__.py
│   │   ├── trainer.py             # Training orchestration
│   │   ├── preprocessor.py        # Text preprocessing
│   │   ├── models.py              # TensorFlow models
│   │   ├── evaluator.py           # Performance metrics
│   │   └── callbacks.py           # Training callbacks
│   │
│   └── export/                     # Export module
│       ├── __init__.py
│       ├── exporter.py            # TFLite conversion
│       ├── optimizer.py           # Quantization
│       ├── packager.py            # ZIP generation
│       └── validators.py          # Validation
│
├── 📁 tests/                        # Test suite
│   │
│   ├── unit/
│   │   ├── test_intent_manager.py
│   │   ├── test_trainer.py
│   │   ├── test_preprocessor.py
│   │   ├── test_exporter.py
│   │   └── conftest.py            # Pytest fixtures
│   │
│   ├── integration/
│   │   ├── test_full_pipeline.py
│   │   ├── test_mit_app_inventor_compat.py
│   │   └── test_export_import.py
│   │
│   └── fixtures/
│       ├── sample_training_data.json
│       ├── sample_model.h5
│       └── sample_utterances.txt
│
├── 📁 docs/                         # Documentation
│   │
│   ├── index.md                    # Docs home
│   ├── ARCHITECTURE.md             # System design
│   ├── CHANGELOG.md                # Version history
│   │
│   ├── api/
│   │   ├── training_api.md         # Training module API
│   │   ├── export_api.md           # Export module API
│   │   └── cli_reference.md        # CLI documentation
│   │
│   └── guides/
│       ├── getting_started.md      # Beginner tutorial
│       ├── how_it_works.md         # Technical overview
│       ├── advanced_training.md    # Advanced topics
│       ├── mit_app_inventor_integration.md
│       └── faq.md                  # FAQ
│
├── 📁 examples/                     # Example chatbots
│   ├── customer_service_bot.json   # Customer support template
│   ├── trivia_bot.json             # Trivia game template
│   ├── weather_assistant.json      # Weather bot template
│   └── README.md                   # Examples documentation
│
├── 📁 assets/                       # Project assets
│   │
│   ├── architecture/
│   │   ├── system_diagram.png      # Architecture diagram
│   │   ├── data_flow.png           # Data flow diagram
│   │   └── component_diagram.png
│   │
│   ├── screenshots/
│   │   ├── ui_main.png             # Training interface
│   │   ├── ui_testing.png          # Testing console
│   │   └── ui_export.png           # Export dialog
│   │
│   └── logos/
│       ├── logo.png
│       └── gsoc_badge.png
│
├── 📁 scripts/                      # Utility scripts
│   ├── launch_builder.py           # Start training UI
│   ├── train_sample_model.py       # Demo training
│   ├── validate_export.py          # Export validation
│   ├── verify_setup.py             # Setup verification
│   ├── setup_dev_env.sh            # Dev environment setup
│   └── create_release.sh           # Release automation
│
└── 📁 models/                       # (Generated) Trained models
    ├── my_bot_v1/
    │   ├── model.h5               # Trained weights
    │   ├── vocabulary.txt         # Tokenizer vocab
    │   └── config.json            # Model config
    │
    └── my_bot_v2/
```

## Key Directories Explained

### `/src` - Application Code
Main source code organized by functionality:
- `chatbot_builder/` - User interface and intent management
- `training/` - ML model training pipeline
- `export/` - Model optimization and packaging

### `/tests` - Automated Testing
Comprehensive test suite:
- `unit/` - Unit tests for individual modules
- `integration/` - End-to-end workflow tests
- `fixtures/` - Test data and mock objects

### `/docs` - Documentation
User-facing and technical documentation:
- Guides for getting started and advanced usage
- API reference
- Architecture documentation

### `/examples` - Templates
Pre-built example chatbots:
- JSON format for easy import
- Real-world use cases
- Customizable templates

### `/scripts` - Utility Tools
Helper scripts for common tasks:
- Starting the application
- Training samples
- Setting up development environment

### `.github/` - GitHub Configuration
GitHub-specific configuration:
- CI/CD workflows
- Issue templates
- PR templates

## File Organization Principles

1. **Modularity** - Each module has single responsibility
2. **Testability** - Easy to write and run tests
3. **Clarity** - Descriptive names and clear structure
4. **Scalability** - Easy to add new features
5. **Documentation** - Well documented code
6. **Conventions** - Consistent naming and patterns

## Next Steps

- **[Setup Project](../../SETUP.md)** - Get it running
- **[Contributing](../../CONTRIBUTING.md)** - How to contribute
- **[Documentation](.)** - Read the docs
- **[Examples](../../examples/)** - Try examples

---

This structure follows Python project best practices and is typical for professional open-source projects.
