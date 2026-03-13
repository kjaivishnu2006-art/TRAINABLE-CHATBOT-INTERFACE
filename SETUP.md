# Setup Instructions

Complete guide for setting up the Trainable ChatBot Builder development environment.

## Prerequisites

- **Python 3.8 or higher** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **pip** - Usually comes with Python
- **Virtual environment tool** - `venv` or `virtualenv`

## 🖥️ Platform-Specific Setup

### Windows

```powershell
# Clone repository
git clone https://github.com/your-org/trainable-chatbot.git
cd trainable-chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify installation
python -c "import tensorflow; print(f'TensorFlow {tensorflow.__version__}')"
```

### macOS

```bash
# Clone repository
git clone https://github.com/your-org/trainable-chatbot.git
cd trainable-chatbot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify installation
python -c "import tensorflow; print(f'TensorFlow {tensorflow.__version__}')"
```

### Linux (Ubuntu/Debian)

```bash
# Clone repository
git clone https://github.com/your-org/trainable-chatbot.git
cd trainable-chatbot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify installation
python -c "import tensorflow; print(f'TensorFlow {tensorflow.__version__}')"
```

## 📦 Dependencies Installation

### Core Dependencies (`requirements.txt`)

```
tensorflow==2.13.0
tensorflow-lite==2.13.0
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
flask>=2.2.0
python-dotenv>=0.19.0
```

### Development Dependencies (`requirements-dev.txt`)

```
pytest>=7.2.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
sphinx>=5.0.0
```

## 🏗️ Project Structure Verification

After setup, verify your environment:

```bash
# List installed packages
pip list

# Show Python version
python --version

# Test imports
python -c "import tensorflow, numpy, pandas; print('All imports successful')"

# Check project structure
ls -la  # Unix/Mac
dir     # Windows
```

Expected structure:
```
trainable-chatbot/
├── venv/                    ✓ Virtual environment
├── src/
├── tests/
├── docs/
├── requirements.txt         ✓ Dependencies listed
├── setup.py                ✓ Package setup
└── README.md               ✓ Documentation
```

## 🚀 First Run

### Launch Training Interface

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # Unix/Mac
# or
venv\Scripts\activate     # Windows

# Start the application
python -m src.chatbot_builder.main

# Application should open at http://localhost:5000
```

### Run Sample Training

```bash
# Activate virtual environment
source venv/bin/activate

# Run sample training script
python scripts/train_sample_model.py

# Should create output in: models/sample_chat_bot/
```

### Run Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Expected output: All tests pass with >80% coverage
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# .env
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
MODEL_OUTPUT_DIR=./models/
UPLOAD_FOLDER=./uploads/
MAX_UPLOAD_SIZE=104857600  # 100MB
```

### IDE Setup (VS Code)

**Extensions to Install:**
- Python
- Pylance
- Pytest
- Black Formatter

**.vscode/settings.json:**
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length=88"],
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

### IDE Setup (PyCharm)

1. **File → Settings → Project → Python Interpreter**
   - Add Interpreter → Existing Environment → Select `venv/bin/python`

2. **File → Settings → Tools → Python Integrated Tools**
   - Default test runner: pytest
   - Docstring format: Google

3. **Code style → Python**
   - Line length: 88 characters

## 🧪 Testing Setup

### Configure Pytest

`.pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### Run Tests by Category

```bash
# Only unit tests
pytest -m unit

# Only integration tests
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# With verbose output
pytest -v

# Show test coverage
pytest --cov=src --cov-report=html
```

## 🐛 Troubleshooting

### Python Not Found

```bash
# Check Python installation
python --version

# If not found, reinstall Python or add to PATH
# Windows: https://docs.python.org/3/using/windows.html
# macOS: brew install python3
# Linux: sudo apt install python3
```

### Virtual Environment Not Activating

```bash
# Windows - Try cmd.exe instead of PowerShell
cmd.exe
venv\Scripts\activate

# Or use PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### TensorFlow Installation Issues

```bash
# Try CPU-only version
pip install tensorflow-cpu

# Or use pre-built wheel
pip install --upgrade tensorflow

# Check TensorFlow version
python -c "import tensorflow as tf; print(tf.__version__)"
```

### Permission Denied on Scripts

```bash
# macOS/Linux
chmod +x scripts/*.sh

# Run bash scripts
bash scripts/launch_builder.py
```

### Import Errors in Tests

```bash
# Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run pytest from project root
cd trainable-chatbot
pytest
```

## 📊 Verifying Your Setup

Run this verification script:

```bash
# verify_setup.py
python scripts/verify_setup.py
```

Expected output:
```
✓ Python 3.8+ installed
✓ TensorFlow available
✓ NumPy available
✓ Virtual environment active
✓ All dependencies installed
✓ Tests can be discovered
✓ Project structure valid

Setup verification: PASSED
```

## 🆘 Getting Help

1. **Check [docs/guides/faq.md](docs/guides/faq.md)** for common issues
2. **Search [existing issues](https://github.com/your-org/trainable-chatbot/issues)**
3. **Ask in [GitHub Discussions](https://github.com/your-org/trainable-chatbot/discussions)**
4. **Contact maintainers** via email

## 📚 Next Steps

After successful setup:

1. Read [docs/guides/getting_started.md](docs/guides/getting_started.md)
2. Explore [examples/](examples/) directory
3. Run sample training: `python scripts/train_sample_model.py`
4. Check [CONTRIBUTING.md](CONTRIBUTING.md) to start contributing

---

**Setup complete!** 🎉 You're ready to develop.
