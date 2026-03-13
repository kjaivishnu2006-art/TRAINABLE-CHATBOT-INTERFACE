"""Tests for Embedding-Based Q&A Chatbot."""

import pytest
import json
from pathlib import Path
from embedding_chatbot import EmbeddingQAChatbot, EMBEDDINGS_AVAILABLE


class TestEmbeddingQAChatbot:
    """Test suite for EmbeddingQAChatbot."""
    
    @pytest.fixture
    def chatbot_embedding(self):
        """Create chatbot with embeddings."""
        if not EMBEDDINGS_AVAILABLE:
            pytest.skip("sentence-transformers not installed")
        
        dataset_path = Path(__file__).parent / "qa_dataset.json"
        return EmbeddingQAChatbot(
            str(dataset_path),
            model_name="all-MiniLM-L6-v2",
            similarity_threshold=0.3,
            use_embeddings=True
        )
    
    @pytest.fixture
    def chatbot_keyword(self):
        """Create chatbot with keyword fallback."""
        dataset_path = Path(__file__).parent / "qa_dataset.json"
        return EmbeddingQAChatbot(
            str(dataset_path),
            similarity_threshold=0.3,
            use_embeddings=False
        )
    
    def test_initialization_with_embeddings(self, chatbot_embedding):
        """Test initialization with embeddings."""
        assert chatbot_embedding.qa_pairs
        assert len(chatbot_embedding.qa_pairs) > 0
        
        if EMBEDDINGS_AVAILABLE:
            assert chatbot_embedding.model is not None
            assert len(chatbot_embedding.question_embeddings) > 0
    
    def test_initialization_without_embeddings(self, chatbot_keyword):
        """Test initialization without embeddings."""
        assert chatbot_keyword.qa_pairs
        assert len(chatbot_keyword.qa_pairs) > 0
        assert not chatbot_keyword.use_embeddings
    
    def test_find_answer_direct_match_embedding(self, chatbot_embedding):
        """Test finding answer with direct question match using embeddings."""
        # Get first question from dataset
        first_question = chatbot_embedding.qa_pairs[0]['question']
        
        result = chatbot_embedding.find_answer(first_question)
        
        assert result['answer'] is not None
        assert result['confidence'] > 0.5  # Should be high for exact match
        assert result['method'] == 'embedding'
    
    def test_find_answer_similar_question_embedding(self, chatbot_embedding):
        """Test finding answer with similar question using embeddings."""
        # Use a paraphrased version of a question
        result = chatbot_embedding.find_answer("What programming language is Python?")
        
        assert result['answer'] is not None
        assert result['confidence'] > 0.3
        assert result['method'] == 'embedding'
    
    def test_find_answer_direct_match_keyword(self, chatbot_keyword):
        """Test finding answer with keyword matching."""
        first_question = chatbot_keyword.qa_pairs[0]['question']
        
        result = chatbot_keyword.find_answer(first_question)
        
        assert result['answer'] is not None
        assert result['confidence'] > 0.0
        assert result['method'] == 'keyword'
    
    def test_find_answer_no_match(self, chatbot_embedding):
        """Test when no suitable match is found."""
        result = chatbot_embedding.find_answer("xyzabc123xyz")
        
        assert result['answer'] is None
        assert result['confidence'] == 0.0
    
    def test_find_answer_empty_input(self, chatbot_embedding):
        """Test with empty input."""
        result = chatbot_embedding.find_answer("")
        
        assert result['answer'] is None
        assert result['confidence'] == 0.0
    
    def test_find_answer_with_all_scores(self, chatbot_embedding):
        """Test finding answer and returning all scores."""
        result = chatbot_embedding.find_answer(
            chatbot_embedding.qa_pairs[0]['question'],
            return_all_scores=True
        )
        
        assert result['answer'] is not None
        assert 'all_scores' in result
        assert len(result['all_scores']) > 0
        
        # All scores should be sorted descending
        scores = [s['score'] for s in result['all_scores']]
        assert scores == sorted(scores, reverse=True)
    
    def test_semantic_understanding(self, chatbot_embedding):
        """Test semantic understanding of similar phrases."""
        # Test that semantically similar questions get matched
        test_phrases = [
            "How do I use Python?",
            "Python usage",
            "teaching Python",
            "learning Python"
        ]
        
        results = [chatbot_embedding.find_answer(phrase) for phrase in test_phrases]
        
        # At least most should find an answer
        answered = sum(1 for r in results if r['answer'] is not None)
        assert answered >= len(test_phrases) * 0.5
    
    def test_embeddings_vs_keywords(self, chatbot_embedding, chatbot_keyword):
        """Compare embedding and keyword matching."""
        test_question = "What is Python?"
        
        result_embed = chatbot_embedding.find_answer(test_question)
        result_keyword = chatbot_keyword.find_answer(test_question)
        
        # Both should find an answer
        assert result_embed['answer'] is not None
        assert result_keyword['answer'] is not None
        
        # Embeddings typically have higher confidence for semantic matches
        # But might find different questions
        assert result_embed['method'] == 'embedding'
        assert result_keyword['method'] == 'keyword'
    
    def test_get_statistics(self, chatbot_embedding):
        """Test statistics method."""
        stats = chatbot_embedding.get_statistics()
        
        assert 'total_qa_pairs' in stats
        assert 'model_name' in stats
        assert 'using_embeddings' in stats
        assert 'similarity_threshold' in stats
        assert stats['total_qa_pairs'] > 0
        assert stats['similarity_threshold'] == 0.3
    
    def test_list_questions(self, chatbot_embedding):
        """Test that all questions can be listed."""
        questions = [qa['question'] for qa in chatbot_embedding.qa_pairs]
        
        assert len(questions) > 0
        assert all(isinstance(q, str) for q in questions)
        assert all(len(q) > 0 for q in questions)
    
    def test_threshold_filtering(self):
        """Test that similarity threshold is respected."""
        dataset_path = Path(__file__).parent / "qa_dataset.json"
        
        if EMBEDDINGS_AVAILABLE:
            chatbot_high_threshold = EmbeddingQAChatbot(
                str(dataset_path),
                similarity_threshold=0.9,
                use_embeddings=True
            )
            
            result = chatbot_high_threshold.find_answer("random text xyz123")
            
            # With very high threshold, should not find matches
            assert result['answer'] is None
    
    def test_dataset_loading(self):
        """Test that dataset loads correctly."""
        dataset_path = Path(__file__).parent / "qa_dataset.json"
        
        # Load raw dataset
        with open(dataset_path, 'r') as f:
            raw_data = json.load(f)
        
        # Create chatbot
        chatbot = EmbeddingQAChatbot(
            str(dataset_path),
            use_embeddings=False
        )
        
        # Check counts match
        assert len(chatbot.qa_pairs) == len(raw_data['qa_pairs'])
    
    def test_invalid_dataset_path(self):
        """Test error handling for invalid dataset path."""
        with pytest.raises(FileNotFoundError):
            EmbeddingQAChatbot("/nonexistent/path/dataset.json")
    
    def test_question_embedding_count(self, chatbot_embedding):
        """Test that all questions have embeddings."""
        if EMBEDDINGS_AVAILABLE and chatbot_embedding.use_embeddings:
            assert len(chatbot_embedding.question_embeddings) == len(chatbot_embedding.qa_pairs)
    
    def test_embedding_dimension(self, chatbot_embedding):
        """Test embedding dimensions."""
        if EMBEDDINGS_AVAILABLE and chatbot_embedding.use_embeddings:
            # MiniLM-L6 produces 384-dimensional embeddings
            embedding_shape = chatbot_embedding.question_embeddings.shape
            
            assert len(embedding_shape) == 2
            assert embedding_shape[0] == len(chatbot_embedding.qa_pairs)
            assert embedding_shape[1] == 384  # MiniLM-L6 dimension


class TestEmbeddingComparison:
    """Compare embedding-based vs keyword-based matching."""
    
    @pytest.fixture
    def test_cases(self):
        """Test cases for comparison."""
        return [
            "What is Python?",
            "How to install packages",
            "virtual environment setup",
            "JSON file format",
            "machine learning basics",
            "chatbot development",
        ]
    
    def test_consistency(self, test_cases):
        """Test that both methods are somewhat consistent."""
        dataset_path = Path(__file__).parent / "qa_dataset.json"
        
        if not EMBEDDINGS_AVAILABLE:
            pytest.skip("sentence-transformers not installed")
        
        chatbot_embed = EmbeddingQAChatbot(
            str(dataset_path),
            use_embeddings=True
        )
        chatbot_keyword = EmbeddingQAChatbot(
            str(dataset_path),
            use_embeddings=False
        )
        
        for test_input in test_cases:
            result_embed = chatbot_embed.find_answer(test_input)
            result_keyword = chatbot_keyword.find_answer(test_input)
            
            # Both should either find answer or not
            # (they might find different answers)
            both_found = (result_embed['answer'] is not None and 
                         result_keyword['answer'] is not None)
            both_not_found = (result_embed['answer'] is None and 
                             result_keyword['answer'] is None)
            
            assert both_found or both_not_found


class TestEmbeddingEdgeCases:
    """Test edge cases for embedding chatbot."""
    
    @pytest.fixture
    def chatbot(self):
        """Create chatbot for testing."""
        dataset_path = Path(__file__).parent / "qa_dataset.json"
        return EmbeddingQAChatbot(
            str(dataset_path),
            use_embeddings=False  # Use keyword for reliability
        )
    
    def test_very_long_input(self, chatbot):
        """Test with very long input."""
        long_input = "What is Python? " * 100
        result = chatbot.find_answer(long_input)
        
        # Should still work
        assert isinstance(result, dict)
        assert 'answer' in result
    
    def test_special_characters(self, chatbot):
        """Test with special characters."""
        special_input = "What!@#$%^&*()_+=-[]{}|;:',.<>?/is Python???"
        result = chatbot.find_answer(special_input)
        
        # Should handle gracefully
        assert isinstance(result, dict)
    
    def test_unicode_input(self, chatbot):
        """Test with unicode characters."""
        unicode_input = "What is Python? 你好 مرحبا"
        result = chatbot.find_answer(unicode_input)
        
        # Should handle gracefully
        assert isinstance(result, dict)
    
    def test_case_insensitivity(self, chatbot):
        """Test case insensitivity."""
        result_lower = chatbot.find_answer("what is python?")
        result_upper = chatbot.find_answer("WHAT IS PYTHON?")
        result_mixed = chatbot.find_answer("WhAt Is PyThOn?")
        
        # All should produce answer or all should not
        all_found = all(r['answer'] is not None for r in [result_lower, result_upper, result_mixed])
        all_not_found = all(r['answer'] is None for r in [result_lower, result_upper, result_mixed])
        
        assert all_found or all_not_found


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
