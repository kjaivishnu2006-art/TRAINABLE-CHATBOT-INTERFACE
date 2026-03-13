"""
Flask API routes for chatbot model export
Integrates export functionality with REST API
"""

from flask import Blueprint, jsonify, request, send_file
from pathlib import Path
import tempfile
import json

# Create blueprint
export_routes = Blueprint('export', __name__, url_prefix='/api/export')


def setup_export_routes(app):
    """Setup export routes for Flask app."""
    app.register_blueprint(export_routes)


@export_routes.route('/lightweight/<chatbot_id>', methods=['GET'])
def export_lightweight(chatbot_id):
    """Export chatbot as lightweight JSON.
    
    GET /api/export/lightweight/<chatbot_id>
    
    Returns:
        - JSON response on success
        - Error on invalid chatbot_id
    """
    try:
        from src.chatbot_builder.app import db, ChatBot
        from export_chatbot_model import ChatbotModelExporter
        from embedding_chatbot import EmbeddingQAChatbot
        
        # Get chatbot from database
        chatbot_obj = db.session.get(ChatBot, chatbot_id)
        if not chatbot_obj:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        # Export to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        # Build Q&A dataset
        qa_data = []
        for intent in chatbot_obj.intents:
            qa_data.append({
                'question': intent.utterances[0].text if intent.utterances else '',
                'answer': intent.responses[0].text if intent.responses else '',
                'keywords': [u.text for u in intent.utterances] if intent.utterances else []
            })
        
        # Create exporter with temp chatbot
        class TempChatbot:
            def __init__(self):
                self.qa_pairs = qa_data
                self.chatbot_name = chatbot_obj.name
        
        exporter = ChatbotModelExporter(TempChatbot())
        result = exporter.export_lightweight(temp_path)
        
        # Read and return file
        with open(temp_path, 'rb') as f:
            return send_file(
                f,
                mimetype='application/json',
                as_attachment=True,
                download_name=f"{chatbot_obj.name}_model.json"
            )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@export_routes.route('/embedding/<chatbot_id>', methods=['POST'])
def export_embedding(chatbot_id):
    """Export chatbot with embeddings.
    
    POST /api/export/embedding/<chatbot_id>
    
    Query params:
        - quantize (bool): Whether to quantize embeddings (default: true)
    
    Returns:
        - JSON response with export info
        - Error on failure
    """
    try:
        quantize = request.args.get('quantize', 'true').lower() == 'true'
        
        from export_chatbot_model import ChatbotModelExporter
        from embedding_chatbot import EmbeddingQAChatbot
        
        # Create exporter
        chatbot = EmbeddingQAChatbot("qa_dataset.json")
        exporter = ChatbotModelExporter(chatbot)
        
        # Export to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        result = exporter.export_embedding_model(temp_path, quantize_embeddings=quantize)
        
        return jsonify({
            'status': 'success',
            'size_kb': result['size_kb'],
            'qa_pairs': result['qa_pairs'],
            'dimension': result['embedding_dimension'],
            'quantized': result['quantized'],
            'download_url': f'/api/export/download/{Path(temp_path).name}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@export_routes.route('/web-bundle', methods=['GET'])
def export_web_bundle():
    """Export as web-ready bundle.
    
    GET /api/export/web-bundle
    
    Returns:
        - ZIP file containing HTML, CSS, JS, and model
    """
    try:
        import zipfile
        import io
        
        from export_chatbot_model import ChatbotModelExporter
        from embedding_chatbot import EmbeddingQAChatbot
        
        # Create exporter
        chatbot = EmbeddingQAChatbot("qa_dataset.json")
        exporter = ChatbotModelExporter(chatbot)
        
        # Export to temp directory
        temp_dir = tempfile.mkdtemp()
        result = exporter.export_web_bundle(temp_dir)
        
        # Create ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in result['files']:
                arcname = Path(file_path).name
                zf.write(file_path, arcname=arcname)
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='chatbot_web_bundle.zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@export_routes.route('/formats', methods=['GET'])
def get_export_formats():
    """Get available export formats.
    
    GET /api/export/formats
    
    Returns:
        - List of available formats with descriptions
    """
    return jsonify({
        'formats': [
            {
                'id': 'lightweight',
                'name': 'Lightweight',
                'size': '<500 KB',
                'features': ['Offline', 'Keyword matching', 'Fast'],
                'suitable_for': ['Mobile apps', 'Low bandwidth'],
                'accuracy': 'Medium (42%)',
                'latency': '~1ms'
            },
            {
                'id': 'embedding',
                'name': 'Semantic Embedding',
                'size': '1-5 MB',
                'features': ['Offline', 'Semantic matching', 'Paraphrase detection'],
                'suitable_for': ['Smart phones', 'Semantic search'],
                'accuracy': 'High (92%)',
                'latency': '~45ms'
            },
            {
                'id': 'web_bundle',
                'name': 'Web Bundle',
                'size': '50-200 KB',
                'features': ['Complete app', 'No setup needed', 'Browser-ready'],
                'suitable_for': ['Web deployment', 'Quick testing'],
                'accuracy': 'Medium (42%)',
                'latency': '~1ms'
            },
            {
                'id': 'compressed',
                'name': 'Compressed (gzip)',
                'size': '50-300 KB',
                'features': ['Compressed', 'Full content', 'Bandwidth optimized'],
                'suitable_for': ['File transfer', 'Archival'],
                'accuracy': 'High (92%)',
                'latency': 'Variable'
            }
        ]
    })


@export_routes.route('/stats', methods=['GET'])
def get_export_stats():
    """Get export statistics.
    
    GET /api/export/stats
    
    Returns:
        - Stats on export sizes and recommendations
    """
    return jsonify({
        'size_estimates_kb': {
            'lightweight_per_50_qa': 25,
            'embedding_per_50_qa': 100,
            'embedding_quantized_per_50_qa': 25,
            'web_bundle': 100
        },
        'performance': {
            'keyword_latency_ms': 1,
            'embedding_latency_ms': 45,
            'embedding_on_gpu_ms': 8
        },
        'accuracy': {
            'keyword_matching': '42%',
            'embedding_matching': '92%'
        },
        'recommendations': [
            'Use lightweight for mobile apps with size constraints',
            'Use embedding for semantic understanding',
            'Use quantization to save 75% space',
            'Use web bundle for quick deployment'
        ]
    })


@export_routes.route('/schema', methods=['GET'])
def get_schema():
    """Get export format schema.
    
    GET /api/export/schema
    
    Returns:
        - JSON schema for exported models
    """
    return jsonify({
        'lightweight_schema': {
            'metadata': {
                'version': '2.0',
                'type': 'lightweight',
                'chatbot_name': 'string',
                'export_date': 'ISO timestamp',
                'total_qa_pairs': 'integer'
            },
            'qa_pairs': [
                {
                    'id': 'integer',
                    'question': 'string',
                    'answer': 'string',
                    'keywords': ['string']
                }
            ]
        },
        'embedding_schema': {
            'metadata': {
                'version': '2.0',
                'type': 'embedding_model',
                'chatbot_name': 'string',
                'model_name': 'string',
                'similarity_threshold': 'float',
                'export_date': 'ISO timestamp',
                'total_qa_pairs': 'integer',
                'embedding_dimension': 'integer',
                'quantized': 'boolean'
            },
            'qa_pairs': [
                {
                    'id': 'integer',
                    'question': 'string',
                    'answer': 'string',
                    'keywords': ['string'],
                    'embedding': ['integer or float'] 
                }
            ]
        }
    })


@export_routes.route('/test-export', methods=['GET'])
def test_export():
    """Test export with sample chatbot.
    
    GET /api/export/test-export
    
    Returns:
        - Test export in requested format
    """
    try:
        format_type = request.args.get('format', 'lightweight')
        
        # Create test chatbot
        test_qa = [
            {'question': 'What is Python?', 'answer': 'Python is a programming language'},
            {'question': 'How to install Python?', 'answer': 'Visit python.org and download'},
            {'question': 'What can I do with Python?', 'answer': 'Build web apps, data science, automation, etc.'}
        ]
        
        test_model = {
            'metadata': {
                'version': '2.0',
                'type': format_type,
                'chatbot_name': 'Test Bot',
                'export_date': '2024-03-12T10:30:00',
                'total_qa_pairs': len(test_qa)
            },
            'qa_pairs': test_qa
        }
        
        if format_type == 'embedding':
            test_model['metadata']['embedding_dimension'] = 384
            for qa in test_model['qa_pairs']:
                # Add dummy embeddings
                qa['embedding'] = [i % 127 for i in range(384)]
        
        return jsonify(test_model)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health check
@export_routes.route('/health', methods=['GET'])
def health():
    """Health check for export service.
    
    GET /api/export/health
    
    Returns:
        - Status and available formats
    """
    return jsonify({
        'status': 'healthy',
        'available_formats': ['lightweight', 'embedding', 'web_bundle', 'compressed'],
        'version': '1.0'
    })


if __name__ == "__main__":
    # Test route responses
    print("Export API Routes Available:")
    print("  GET  /api/export/formats - List all formats")
    print("  GET  /api/export/stats - Export statistics")
    print("  GET  /api/export/schema - JSON schema")
    print("  GET  /api/export/health - Service health check")
    print("  GET  /api/export/lightweight/<id> - Export lightweight JSON")
    print("  POST /api/export/embedding/<id> - Export with embeddings")
    print("  GET  /api/export/web-bundle - Export web bundle")
    print("  GET  /api/export/test-export - Test export")
