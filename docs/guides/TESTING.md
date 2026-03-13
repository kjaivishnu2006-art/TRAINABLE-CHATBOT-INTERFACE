# Testing Documentation

Guide to testing the Trainable ChatBot Builder project.

## Test Structure

```
tests/
├── unit/                  # Unit tests for individual components
├── integration/           # End-to-end workflow tests
├── fixtures/             # Test data and fixtures
└── conftest.py           # Pytest configuration
```

## Running Tests

### All Tests
```bash
pytest
```

### Specific Test File
```bash
pytest tests/unit/test_trainer.py
```

### Specific Test Function
```bash
pytest tests/unit/test_trainer.py::test_train_model_success
```

### With Coverage Report
```bash
pytest --cov=src --cov-report=html
```

### By Category
```bash
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m slow -v       # Mark slow tests
```

## Test Categories

### Unit Tests (`tests/unit/`)
Test individual components in isolation.

- `test_intent_manager.py` - Intent CRUD operations
- `test_trainer.py` - Model training logic
- `test_preprocessor.py` - Text preprocessing
- `test_exporter.py` - Model export functionality
- `test_packager.py` - Package creation

### Integration Tests (`tests/integration/`)
Test complete workflows end-to-end.

- `test_full_pipeline.py` - Training → Export → Verify
- `test_mit_app_inventor_compat.py` - App Inventor compatibility
- `test_export_import.py` - Export format verification

## Writing Tests

### Example Unit Test

```python
import pytest
from src.chatbot_builder.intent_manager import IntentManager


class TestIntentManager:
    """Tests for IntentManager class."""

    @pytest.fixture
    def manager(self):
        """Provide initialized IntentManager."""
        return IntentManager()

    def test_add_intent_success(self, manager):
        """Test successfully adding new intent."""
        manager.add_intent("greeting", ["Hi", "Hello"])
        assert "greeting" in manager.intents

    def test_add_intent_duplicate_raises_error(self, manager):
        """Test that duplicate intent raises ValueError."""
        manager.add_intent("greeting", ["Hi"])
        with pytest.raises(ValueError):
            manager.add_intent("greeting", ["Hey"])

    def test_remove_intent_success(self, manager):
        """Test successfully removing intent."""
        manager.add_intent("greeting", ["Hi"])
        manager.remove_intent("greeting")
        assert "greeting" not in manager.intents
```

### Example Integration Test

```python
import pytest
from pathlib import Path
from src.training.trainer import Trainer
from src.export.exporter import Exporter


def test_full_training_pipeline(tmp_path):
    """Test complete training → export workflow."""
    # Setup
    training_file = tmp_path / "training.json"
    output_dir = tmp_path / "output"

    # Train
    trainer = Trainer()
    model = trainer.train_from_file(training_file)
    
    # Export
    exporter = Exporter()
    result = exporter.export(model, output_dir, quantize=True)
    
    # Verify
    assert output_dir.exists()
    assert (output_dir / "model.tflite").exists()
    assert result.success
```

## Fixtures

### Pytest Fixtures

Fixtures in `tests/conftest.py`:

```python
@pytest.fixture
def sample_training_data():
    """Provide sample training data."""
    return {
        "intents": [
            {"name": "greeting", "utterances": ["Hi", "Hello"]},
            {"name": "joke", "utterances": ["Tell me a joke"]}
        ]
    }

@pytest.fixture
def temp_model_dir(tmp_path):
    """Provide temporary directory for models."""
    return tmp_path / "models"
```

## Test Data

### Sample Training Data (`tests/fixtures/`)

- `sample_training_data.json` - Valid training data
- `sample_model.h5` - Pre-trained model for testing
- `sample_utterances.txt` - Utterance samples

## Continuous Integration

### GitHub Actions Workflow

Tests run automatically on:
- **Push** to `main` or `develop` branches
- **Pull Requests** to `main` or `develop`

### CI Configuration (`.github/workflows/tests.yml`)

- Runs on Ubuntu, Windows, macOS
- Tests Python 3.8, 3.9, 3.10, 3.11
- Code quality checks: black, flake8, mypy
- Coverage reporting to Codecov

## Coverage Requirements

- **Minimum for PR**: 80% coverage
- **Target for release**: 90%+
- **Coverage report**: `htmlcov/index.html` after running with `--cov-report=html`

## Debugging Tests

### Run with Debug Output
```bash
pytest -v -s tests/unit/test_trainer.py
```

### Drop into Debugger
```python
# In test file
def test_something():
    import pdb; pdb.set_trace()  # Debugger breaks here
    # ... test code ...
```

Or use CLI:
```bash
pytest --pdb tests/unit/test_trainer.py
```

### View Test Event Logs
```bash
pytest -vv --tb=long tests/unit/test_trainer.py
```

## Performance Testing

### Mark Slow Tests
```python
@pytest.mark.slow
def test_expensive_training():
    # Long-running test
    pass
```

Run excluding slow tests:
```bash
pytest -m "not slow"
```

Profile test execution:
```bash
pytest --profile tests/
```

## Mocking

### Example Mock Test

```python
from unittest.mock import Mock, patch


@patch('src.training.trainer.tf.keras.Model')
def test_train_with_mock_model(mock_model):
    """Test training with mocked TensorFlow model."""
    trainer = Trainer()
    trainer.train(mock_data)
    
    mock_model.fit.assert_called_once()
```

## Best Practices

1. **Test One Thing** - Each test should test one behavior
2. **Use Descriptive Names** - `test_add_intent_with_valid_data` ✓
3. **Arrange-Act-Assert** - Setup, execute, verify pattern
4. **DRY** - Use fixtures for common setup
5. **Fast** - Tests should run quickly (mock external calls)
6. **Independent** - Tests shouldn't depend on execution order
7. **Deterministic** - Same input should always give same output

## Troubleshooting

### Tests Fail with "Module not found"

```bash
# Ensure project is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### ModuleNotFoundError for src

```bash
# Run from project root
cd trainable-chatbot
pytest
```

### Permission Denied on test files

```bash
# Linux/macOS
chmod +x tests/**/*.py
```

### Memory issues during test

```bash
# Run tests serially instead of parallel
pytest -n 0
```

---

[Back to Documentation](../index.md)
