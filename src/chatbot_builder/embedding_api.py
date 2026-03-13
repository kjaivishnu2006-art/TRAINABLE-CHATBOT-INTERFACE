"""
Flask API Extension for Embedding-Based Q&A
Add these routes to the existing Flask API (app.py)
"""

from flask import request, jsonify
from typing import Dict, Optional

# Import the embedding chatbot
try:
    from embedding_chatbot import EmbeddingQAChatbot, EMBEDDINGS_AVAILABLE
except ImportError:
    EMBEDDINGS_AVAILABLE = False


class EmbeddingQAService:
    """Service for managing embedding-based Q&A."""
    
    _instance = None
    _chatbot = None
    
    @classmethod
    def get_instance(cls, dataset_path: Optional[str] = None):
        """Get singleton instance of EmbeddingQAService."""
        if cls._instance is None:
            cls._instance = cls(dataset_path)
        return cls._instance
    
    def __init__(self, dataset_path: Optional[str] = None):
        """Initialize service with embedding chatbot."""
        self.dataset_path = dataset_path
        self._initialize_chatbot()
    
    def _initialize_chatbot(self):
        """Initialize the embedding chatbot."""
        if not EMBEDDINGS_AVAILABLE:
            raise ImportError("sentence-transformers not installed")
        
        if self.dataset_path:
            try:
                self._chatbot = EmbeddingQAChatbot(
                    self.dataset_path,
                    model_name="all-MiniLM-L6-v2",
                    similarity_threshold=0.3,
                    use_embeddings=True
                )
            except Exception as e:
                raise RuntimeError(f"Failed to initialize embedding chatbot: {e}")
    
    def find_answer(self, question: str, return_all_scores: bool = False) -> Dict:
        """Find answer using embeddings."""
        if not self._chatbot:
            raise RuntimeError("Chatbot not initialized")
        
        return self._chatbot.find_answer(question, return_all_scores=return_all_scores)
    
    def get_stats(self) -> Dict:
        """Get chatbot statistics."""
        if not self._chatbot:
            raise RuntimeError("Chatbot not initialized")
        
        return self._chatbot.get_statistics()


# Flask API Routes to add to app.py

def setup_embedding_routes(app, embedding_service):
    """Register embedding-based routes to Flask app."""
    
    @app.route('/api/embedding/ask', methods=['POST'])
    def embedding_ask():
        """Find answer using semantic embeddings.
        
        Request:
            {
                "question": "What is Python?",
                "return_all_scores": false
            }
        
        Response:
            {
                "answer": "Python is a...",
                "confidence": 0.85,
                "method": "embedding",
                "question": "What is Python?",
                "all_scores": [...]  # if return_all_scores=true
            }
        """
        try:
            data = request.get_json()
            question = data.get('question', '').strip()
            return_all_scores = data.get('return_all_scores', False)
            
            if not question:
                return jsonify({'error': 'Question is required'}), 400
            
            result = embedding_service.find_answer(question, return_all_scores)
            return jsonify(result), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/embedding/batch', methods=['POST'])
    def embedding_batch_ask():
        """Find answers for multiple questions at once.
        
        Request:
            {
                "questions": ["What is Python?", "What is pip?"],
                "return_all_scores": false
            }
        
        Response:
            {
                "results": [
                    {"question": "...", "answer": "...", "confidence": 0.85, ...},
                    ...
                ],
                "total": 2,
                "answered": 2
            }
        """
        try:
            data = request.get_json()
            questions = data.get('questions', [])
            return_all_scores = data.get('return_all_scores', False)
            
            if not questions or not isinstance(questions, list):
                return jsonify({'error': 'Questions list is required'}), 400
            
            results = []
            answered_count = 0
            
            for question in questions:
                result = embedding_service.find_answer(question, return_all_scores)
                results.append({
                    'question': question,
                    **result
                })
                
                if result.get('answer'):
                    answered_count += 1
            
            return jsonify({
                'results': results,
                'total': len(questions),
                'answered': answered_count,
                'success_rate': answered_count / len(questions) if questions else 0
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/embedding/stats', methods=['GET'])
    def embedding_stats():
        """Get embedding chatbot statistics.
        
        Response:
            {
                "total_qa_pairs": 10,
                "model_name": "all-MiniLM-L6-v2",
                "using_embeddings": true,
                "similarity_threshold": 0.3,
                "model_loaded": true
            }
        """
        try:
            stats = embedding_service.get_stats()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/embedding/health', methods=['GET'])
    def embedding_health():
        """Check embedding service health.
        
        Response:
            {
                "status": "ok",
                "embeddings_available": true,
                "model_loaded": true,
                "message": "Embedding service is ready"
            }
        """
        try:
            stats = embedding_service.get_stats()
            return jsonify({
                'status': 'ok' if EMBEDDINGS_AVAILABLE else 'degraded',
                'embeddings_available': EMBEDDINGS_AVAILABLE,
                'model_loaded': stats.get('model_loaded', False),
                'message': 'Embedding service is ready' if EMBEDDINGS_AVAILABLE else 'Embeddings not available'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'embeddings_available': False,
                'model_loaded': False,
                'error': str(e),
                'message': 'Embedding service is not available'
            }), 503


# Integration code to add to Flask app initialization

"""
# In your Flask app initialization (app.py), add:

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Initialize embedding service if available
    embedding_service = None
    if EMBEDDINGS_AVAILABLE:
        try:
            from embedding_api import setup_embedding_routes, EmbeddingQAService
            embedding_service = EmbeddingQAService.get_instance('qa_dataset.json')
            setup_embedding_routes(app, embedding_service)
            print('✓ Embedding service initialized')
        except Exception as e:
            print(f'⚠️  Embedding service failed to initialize: {e}')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
"""
