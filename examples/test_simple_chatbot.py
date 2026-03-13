"""Test cases for SimpleQAChatbot."""

import pytest
import json
from pathlib import Path
from simple_chatbot import SimpleQAChatbot


@pytest.fixture
def sample_dataset(tmp_path):
    """Create sample Q&A dataset for testing."""
    dataset = {
        "chatbot_name": "Test Bot",
        "qa_pairs": [
            {
                "id": 1,
                "question": "What is Python?",
                "keywords": ["python", "programming"],
                "answer": "Python is a programming language."
            },
            {
                "id": 2,
                "question": "How do I install Python?",
                "keywords": ["install", "python", "setup"],
                "answer": "Download from python.org and run the installer."
            }
        ]
    }
    
    file_path = tmp_path / "test_dataset.json"
    with open(file_path, 'w') as f:
        json.dump(dataset, f)
    
    return file_path


def test_chatbot_initialization(sample_dataset):
    """Test chatbot loads dataset correctly."""
    chatbot = SimpleQAChatbot(str(sample_dataset))
    assert chatbot.chatbot_name == "Test Bot"
    assert len(chatbot.qa_pairs) == 2


def test_chatbot_file_not_found():
    """Test error when dataset file not found."""
    with pytest.raises(FileNotFoundError):
        SimpleQAChatbot("nonexistent.json")


def test_preprocess_text(sample_dataset):
    """Test text preprocessing."""
    chatbot = SimpleQAChatbot(str(sample_dataset))
    
    processed = chatbot._preprocess_text("What is Python?")
    assert processed == "what is python"
    
    processed = chatbot._preprocess_text("  Multiple   spaces  ")
    assert processed == "multiple spaces"


def test_find_answer_exact_match(sample_dataset):
    """Test finding exact answer match."""
    chatbot = SimpleQAChatbot(str(sample_dataset))
    
    answer, confidence = chatbot.find_answer("What is Python?")
    assert answer == "Python is a programming language."
    assert confidence > 0.5


def test_find_answer_partial_match(sample_dataset):
    """Test finding answer with partial match."""
    chatbot = SimpleQAChatbot(str(sample_dataset))
    
    answer, confidence = chatbot.find_answer("python programming")
    assert answer is not None
    assert confidence >= 0.3


def test_find_answer_no_match(sample_dataset):
    """Test when no answer matches."""
    chatbot = SimpleQAChatbot(str(sample_dataset))
    
    answer, confidence = chatbot.find_answer("xyz abc def")
    assert answer is None
    assert confidence < 0.3


def test_find_answer_empty_input(sample_dataset):
    """Test empty input handling."""
    chatbot = SimpleQAChatbot(str(sample_dataset))
    
    answer, confidence = chatbot.find_answer("")
    assert answer is None
    assert confidence == 0.0


def test_similarity_calculation(sample_dataset):
    """Test similarity scoring."""
    chatbot = SimpleQAChatbot(str(sample_dataset))
    qa_pair = chatbot.qa_pairs[0]
    
    # High similarity
    score1 = chatbot._calculate_similarity("What is Python?", qa_pair)
    
    # Medium similarity
    score2 = chatbot._calculate_similarity("python", qa_pair)
    
    # Low similarity
    score3 = chatbot._calculate_similarity("javascript rust go", qa_pair)
    
    assert score1 > score2 > score3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
