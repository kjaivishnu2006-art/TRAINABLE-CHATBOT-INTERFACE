# Contributing to Trainable ChatBot Builder

Thank you for your interest in contributing! We welcome contributions from the community. This document provides guidelines and instructions for contributing.

## 📋 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🎯 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. Use the [Bug Report template](https://github.com/kjaivishnu2006-art/TRAINABLE-CHATBOT-INTERFACE/issues/new)
3. Include:
   - Python version and OS
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Requesting Features

1. Use the [Feature Request template](https://github.com/kjaivishnu2006-art/TRAINABLE-CHATBOT-INTERFACE/issues/new)
2. Clearly describe the feature and why it's needed
3. Provide usage examples if applicable

### Improving Documentation

1. Fork the repository
2. Create a branch: `git checkout -b docs/improvement`
3. Make changes to `.md` files in `docs/`
4. Submit a pull request

### Contributing Code

## 🔧 Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/trainable-chatbot.git
cd trainable-chatbot

# Add upstream remote
git remote add upstream https://github.com/kjaivishnu2006-art/TRAINABLE-CHATBOT-INTERFACE.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 📝 Development Workflow

### 1. Create a Branch

```bash
# Update main branch
git fetch upstream
git rebase upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

Code-contribution branch naming conventions:
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation improvements
- `refactor/description` - Code refactoring
- `test/description` - Test additions/improvements

### 2. Make Your Changes

```bash
# Write code following the style guide (see below)
# Add tests for new functionality
# Update documentation if needed
```

### 3. Run Tests & Linting

```bash
# Run all tests
pytest

# Check code coverage
pytest --cov=src tests/

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking (optional)
mypy src/
```

### 4. Commit Changes

```bash
# Follow conventional commits format
git add .

# Good commit messages:
# - feat: Add intent entity extraction
# - fix: Handle empty user input gracefully
# - docs: Update API reference
# - test: Add tests for export module
# - refactor: Simplify tokenizer logic
git commit -m "type: Clear, descriptive message"

# Push to your fork
git push origin feature/your-feature-name
```

### 5. Submit a Pull Request

1. Go to GitHub and create a Pull Request
2. Fill out the PR template with:
   - Description of changes
   - Related issues (use `Fixes #123`)
   - Type of change (feature/fix/docs)
   - Testing performed
3. Ensure CI checks pass
4. Request review from maintainers

## 📐 Code Style

### Python Style Guide

We follow **PEP 8** with formatting by **Black**:

```bash
black src/ tests/
```

Key guidelines:
- Max line length: 88 characters (Black default)
- Use type hints for function signatures
- Write docstrings for public functions/classes
- Use meaningful variable names

### Example:

```python
"""Module for training chatbot models."""

from typing import List, Dict, Tuple
from pathlib import Path
import tensorflow as tf


class IntentClassifier:
    """Trains and manages intent classification models."""
    
    def __init__(self, vocab_size: int, max_sequence_length: int) -> None:
        """Initialize the classifier.
        
        Args:
            vocab_size: Size of vocabulary for embeddings
            max_sequence_length: Maximum input sequence length
        """
        self.vocab_size = vocab_size
        self.max_sequence_length = max_sequence_length
        
    def train(
        self,
        texts: List[str],
        labels: List[int],
        epochs: int = 10
    ) -> Dict[str, float]:
        """Train the classifier on provided texts and labels.
        
        Args:
            texts: List of training text samples
            labels: Corresponding intent labels
            epochs: Number of training epochs
            
        Returns:
            Dictionary containing training metrics
        """
        # Implementation here
        pass
```

### Docstring Format

Use Google-style docstrings:

```python
def export_model(
    model_path: Path,
    output_dir: Path,
    quantize: bool = True
) -> str:
    """Export model to TensorFlow Lite format.
    
    Converts a trained model to TFLite format optimized for
    on-device inference on mobile devices.
    
    Args:
        model_path: Path to trained TensorFlow model
        output_dir: Directory to save exported files
        quantize: Whether to apply quantization
        
    Returns:
        Path to exported .tflite file
        
    Raises:
        FileNotFoundError: If model_path does not exist
        ValueError: If model format is unsupported
    """
    pass
```

## 🧪 Testing Requirements

- Write tests for all new features
- Minimum test coverage: 80%
- Use pytest fixtures for setup/teardown
- Test both happy path and error cases

### Example Test:

```python
import pytest
from src.chatbot_builder.intent_manager import IntentManager


@pytest.fixture
def intent_manager():
    """Fixture providing initialized IntentManager."""
    return IntentManager()


def test_add_intent_success(intent_manager):
    """Test successfully adding new intent."""
    intent_manager.add_intent("greeting", ["Hi", "Hello"])
    assert "greeting" in intent_manager.intents


def test_add_intent_duplicate_raises_error(intent_manager):
    """Test that adding duplicate intent raises error."""
    intent_manager.add_intent("greeting", ["Hi"])
    with pytest.raises(ValueError):
        intent_manager.add_intent("greeting", ["Hey"])


def test_add_empty_utterances_raises_error(intent_manager):
    """Test that empty utterances list raises error."""
    with pytest.raises(ValueError):
        intent_manager.add_intent("greeting", [])
```

## 📚 Documentation

When adding features:
1. Update relevant docstrings in code
2. Add/update docs in `docs/` directory
3. Update [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) if changing system design
4. Add examples in `examples/` if applicable

## 🔄 Pull Request Process

1. **Before submitting:**
   - [ ] Code follows style guide (run `black`)
   - [ ] Tests pass locally (`pytest`)
   - [ ] Coverage is adequate
   - [ ] Documentation updated
   - [ ] Commit messages are clear

2. **After submitting:**
   - Maintainer reviews code
   - Address feedback with new commits
   - CI/CD pipeline must pass
   - Minimum 2 approvals required
   - Squash commits before merge (if requested)

## 🐛 Debugging Tips

```bash
# Run single test with verbose output
pytest -v tests/unit/test_trainer.py::test_specific_test

# Run with print debugging
pytest -s tests/unit/test_trainer.py

# Profile code execution
python -m cProfile -s cumulative script.py

# Debug with pdb
pytest --pdb tests/unit/test_trainer.py
```

## 📦 Release Process (Maintainers)

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.0.0`
4. Build: `python setup.py sdist bdist_wheel`
5. Upload: `twine upload dist/*`
6. Create GitHub release with changelog

## ❓ Questions?

- Check [docs/guides/faq.md](docs/guides/faq.md)
- Open a discussion in [GitHub Discussions](https://github.com/your-org/trainable-chatbot/discussions)
- Contact project maintainers

## 🎓 Learning Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Python Docstring Conventions](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Workflow Guide](https://guides.github.com/introduction/flow/)

---

Thank you for helping make Trainable ChatBot Builder better! 🚀
