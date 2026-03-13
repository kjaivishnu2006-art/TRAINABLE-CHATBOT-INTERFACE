"""
Comprehensive tests for chatbot model export system
"""

import json
import tempfile
from pathlib import Path
import pytest

# Test color output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class TestExporterSetup:
    """Test exporter initialization."""
    
    def test_import_exporter(self):
        """✓ Can import exporter module."""
        try:
            from export_chatbot_model import ChatbotModelExporter
            assert ChatbotModelExporter is not None
            print(f"{GREEN}✓{RESET} Exporter imports successfully")
        except ImportError as e:
            pytest.fail(f"Failed to import exporter: {e}")
    
    def test_import_mobile_client(self):
        """✓ Can import mobile client module."""
        try:
            from mobile_chatbot_client import MobileChatbotClient
            assert MobileChatbotClient is not None
            print(f"{GREEN}✓{RESET} Mobile client imports successfully")
        except ImportError as e:
            pytest.fail(f"Failed to import mobile client: {e}")


class TestLightweightExport:
    """Test lightweight export for mobile."""
    
    @pytest.fixture
    def setup(self):
        """Setup test environment."""
        from embedding_chatbot import EmbeddingQAChatbot
        
        chatbot = EmbeddingQAChatbot("qa_dataset.json")
        from export_chatbot_model import ChatbotModelExporter
        exporter = ChatbotModelExporter(chatbot)
        
        return chatbot, exporter
    
    def test_lightweight_export(self, setup):
        """✓ Export lightweight JSON."""
        chatbot, exporter = setup
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = f.name
        
        try:
            result = exporter.export_lightweight(output_path)
            
            assert result['status'] == 'success'
            assert result['qa_pairs'] > 0
            assert 'size_kb' in result
            print(f"{GREEN}✓{RESET} Lightweight export: {result['size_kb']} KB")
            
            # Verify file exists and is valid JSON
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            assert 'metadata' in data
            assert 'qa_pairs' in data
            assert data['metadata']['type'] == 'lightweight'
            
        finally:
            Path(output_path).unlink()
    
    def test_lightweight_qa_format(self, setup):
        """✓ Lightweight format has correct structure."""
        chatbot, exporter = setup
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = f.name
        
        try:
            exporter.export_lightweight(output_path)
            
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            # Check each Q&A pair
            for qa in data['qa_pairs']:
                assert 'id' in qa
                assert 'question' in qa
                assert 'answer' in qa
                assert isinstance(qa['id'], int)
                assert isinstance(qa['question'], str)
                assert isinstance(qa['answer'], str)
            
            print(f"{GREEN}✓{RESET} Q&A format correct ({len(data['qa_pairs'])} pairs)")
            
        finally:
            Path(output_path).unlink()


class TestEmbeddingExport:
    """Test embedding model export."""
    
    @pytest.fixture
    def setup(self):
        """Setup test environment."""
        from embedding_chatbot import EmbeddingQAChatbot
        from export_chatbot_model import ChatbotModelExporter
        
        chatbot = EmbeddingQAChatbot("qa_dataset.json", use_embeddings=True)
        exporter = ChatbotModelExporter(chatbot)
        
        return chatbot, exporter
    
    def test_embedding_export(self, setup):
        """✓ Export embedding model."""
        chatbot, exporter = setup
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = f.name
        
        try:
            result = exporter.export_embedding_model(output_path, quantize_embeddings=False)
            
            assert result['status'] == 'success'
            assert result['embedding_dimension'] > 0
            assert result['quantized'] == False
            print(f"{GREEN}✓{RESET} Embedding export: {result['size_kb']} KB")
            
        finally:
            Path(output_path).unlink()
    
    def test_embedding_quantization(self, setup):
        """✓ Quantize embeddings (reduces size by 75%)."""
        chatbot, exporter = setup
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            unquantized_path = f.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            quantized_path = f.name
        
        try:
            # Export without quantization
            result1 = exporter.export_embedding_model(unquantized_path, quantize_embeddings=False)
            size1 = result1['size_kb']
            
            # Export with quantization
            result2 = exporter.export_embedding_model(quantized_path, quantize_embeddings=True)
            size2 = result2['size_kb']
            
            reduction = (1 - size2 / size1) * 100
            assert reduction > 50, "Quantization should reduce size by >50%"
            print(f"{GREEN}✓{RESET} Quantization: {size1:.1f}KB → {size2:.1f}KB ({reduction:.0f}% smaller)")
            
        finally:
            Path(unquantized_path).unlink()
            Path(quantized_path).unlink()


class TestMobileClient:
    """Test mobile chatbot client."""
    
    @pytest.fixture
    def setup(self):
        """Setup test environment."""
        from embedding_chatbot import EmbeddingQAChatbot
        from export_chatbot_model import ChatbotModelExporter
        from mobile_chatbot_client import MobileChatbotClient
        
        # Create and export model
        chatbot = EmbeddingQAChatbot("qa_dataset.json")
        exporter = ChatbotModelExporter(chatbot)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            model_path = f.name
        
        exporter.export_lightweight(model_path)
        client = MobileChatbotClient(model_path)
        
        return client, model_path
    
    def test_client_initialization(self, setup):
        """✓ Initialize mobile client."""
        client, _ = setup
        
        assert client.model is not None
        assert len(client.qa_pairs) > 0
        print(f"{GREEN}✓{RESET} Mobile client initialized with {len(client.qa_pairs)} Q&A pairs")
    
    def test_get_answer(self, setup):
        """✓ Get answer from mobile client."""
        client, _ = setup
        
        result = client.get_answer("What is Python?")
        
        assert 'answer' in result
        assert 'confidence' in result
        assert 'method' in result
        assert result['answer'] is not None or result['confidence'] == 0
        assert 0 <= result['confidence'] <= 1
        print(f"{GREEN}✓{RESET} Answer retrieved (confidence: {result['confidence']:.1%})")
    
    def test_similar_questions(self, setup):
        """✓ Find similar questions."""
        client, _ = setup
        
        similar = client.get_similar_questions("How to use Python?", top_k=3)
        
        assert isinstance(similar, list)
        assert len(similar) <= 3
        
        for item in similar:
            assert 'question' in item
            assert 'score' in item
            assert 0 <= item['score'] <= 1
        
        print(f"{GREEN}✓{RESET} Found {len(similar)} similar questions")
    
    def test_keyword_search(self, setup):
        """✓ Search by keyword."""
        client, _ = setup
        
        results = client.search_by_keyword("Python")
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        for result in results:
            assert 'question' in result
            assert 'answer' in result
        
        print(f"{GREEN}✓{RESET} Found {len(results)} results for keyword search")
    
    def test_statistics(self, setup):
        """✓ Get model statistics."""
        client, _ = setup
        
        stats = client.get_statistics()
        
        assert 'total_qa_pairs' in stats
        assert 'model_type' in stats
        assert 'threshold' in stats
        assert stats['total_qa_pairs'] > 0
        
        print(f"{GREEN}✓{RESET} Stats: {stats['total_qa_pairs']} pairs, {stats['model_type']} type")
    
    def test_csv_export(self, setup):
        """✓ Export to CSV."""
        client, _ = setup
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name
        
        try:
            client.export_answers_csv(csv_path)
            
            # Verify CSV exists and has content
            with open(csv_path, 'r') as f:
                lines = f.readlines()
            
            assert len(lines) > 1  # Header + data
            assert 'question' in lines[0]
            
            print(f"{GREEN}✓{RESET} CSV export: {len(lines)-1} rows")
            
        finally:
            Path(csv_path).unlink()


class TestWebBundle:
    """Test web bundle export."""
    
    @pytest.fixture
    def setup(self):
        """Setup test environment."""
        from embedding_chatbot import EmbeddingQAChatbot
        from export_chatbot_model import ChatbotModelExporter
        
        chatbot = EmbeddingQAChatbot("qa_dataset.json")
        exporter = ChatbotModelExporter(chatbot)
        
        return exporter
    
    def test_web_bundle_export(self, setup):
        """✓ Export web bundle."""
        exporter = setup
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export_web_bundle(tmpdir, include_embeddings=False)
            
            assert result['status'] == 'success'
            assert len(result['files']) == 3  # model.json, chatbot.html, chatbot.js
            
            for file_path in result['files']:
                assert Path(file_path).exists()
            
            print(f"{GREEN}✓{RESET} Web bundle created: {len(result['files'])} files")
    
    def test_html_client_content(self, setup):
        """✓ HTML client has correct content."""
        exporter = setup
        
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter.export_web_bundle(tmpdir)
            
            html_path = Path(tmpdir) / "chatbot.html"
            html_content = html_path.read_text()
            
            assert '<!DOCTYPE html>' in html_content
            assert 'MobileChatbot' in html_content
            assert 'sendMessage' in html_content
            
            print(f"{GREEN}✓{RESET} HTML client is valid")


class TestExportScenarios:
    """Test real-world export scenarios."""
    
    @pytest.fixture
    def setup(self):
        """Setup test environment."""
        from embedding_chatbot import EmbeddingQAChatbot
        from export_chatbot_model import ChatbotModelExporter
        
        chatbot = EmbeddingQAChatbot("qa_dataset.json")
        exporter = ChatbotModelExporter(chatbot)
        
        return exporter
    
    def test_mobile_app_scenario(self, setup):
        """✓ Scenario: Export for Flutter app."""
        exporter = setup
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            model_path = f.name
        
        try:
            # Export lightweight model
            result = exporter.export_lightweight(model_path)
            
            # Verify it's small enough for mobile (< 1 MB)
            assert result['size_kb'] < 1000, "Model too large for mobile"
            
            print(f"{GREEN}✓{RESET} Mobile model size: {result['size_kb']} KB (suitable for mobile)")
            
        finally:
            Path(model_path).unlink()
    
    def test_web_app_scenario(self, setup):
        """✓ Scenario: Export for web app."""
        exporter = setup
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export_web_bundle(tmpdir)
            
            # Check total size
            total_size = sum(
                Path(f).stat().st_size
                for f in result['files']
            ) / 1024
            
            print(f"{GREEN}✓{RESET} Web bundle total: {total_size:.1f} KB")


def run_all_tests():
    """Run all tests with summary."""
    print(f"\n{BLUE}Running Chatbot Export Tests{RESET}\n")
    
    # Run pytest
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == "__main__":
    run_all_tests()
