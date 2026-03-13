"""
Integration example: Using export system with Flask API
Shows how to add export functionality to the existing Flask backend
"""

# In your Flask app.py, add these imports at the top:
# from export_api import setup_export_routes

# Then register the routes in your Flask app creation:
# from flask import Flask
# app = Flask(__name__)
# setup_export_routes(app)

# Full example Flask app integration:

from flask import Flask
from flask_cors import CORS
from export_api import setup_export_routes

def create_app():
    """Create Flask app with export routes."""
    app = Flask(__name__)
    CORS(app)
    
    # Setup export routes
    setup_export_routes(app)
    
    return app

# Usage endpoints that become available:
# GET  /api/export/formats              - List all export formats
# GET  /api/export/stats                - Export statistics  
# GET  /api/export/schema               - JSON schema definition
# GET  /api/export/health               - Health check
# GET  /api/export/lightweight/<id>    - Export lightweight JSON
# POST /api/export/embedding/<id>      - Export with embeddings (quantize param)
# GET  /api/export/web-bundle          - Export web bundle (ZIP)
# GET  /api/export/test-export         - Test export (format param)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)


# ============================================================================
# CLIENT USAGE EXAMPLES
# ============================================================================

import requests
import json

class ExportClient:
    """Client for chatbot export API."""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def get_formats(self):
        """Get available export formats."""
        response = requests.get(f"{self.base_url}/api/export/formats")
        return response.json()
    
    def export_lightweight(self, chatbot_id):
        """Export chatbot as lightweight JSON."""
        response = requests.get(
            f"{self.base_url}/api/export/lightweight/{chatbot_id}"
        )
        return response.content  # Binary JSON
    
    def export_embedding(self, chatbot_id, quantize=True):
        """Export with embeddings."""
        response = requests.post(
            f"{self.base_url}/api/export/embedding/{chatbot_id}",
            params={'quantize': str(quantize).lower()}
        )
        return response.json()
    
    def export_web_bundle(self):
        """Export web bundle."""
        response = requests.get(
            f"{self.base_url}/api/export/web-bundle"
        )
        return response.content  # ZIP file
    
    def get_stats(self):
        """Get export statistics."""
        response = requests.get(f"{self.base_url}/api/export/stats")
        return response.json()
    
    def get_schema(self):
        """Get export format schema."""
        response = requests.get(f"{self.base_url}/api/export/schema")
        return response.json()


# Usage examples:
if __name__ == "__main__":
    client = ExportClient()
    
    # List formats
    formats = client.get_formats()
    print(f"Available formats: {len(formats['formats'])}")
    for fmt in formats['formats']:
        print(f"  - {fmt['name']}: {fmt['size']}")
    
    # Export lightweight
    json_data = client.export_lightweight("chatbot_1")
    with open("exported_model.json", "wb") as f:
        f.write(json_data)
    print("✓ Lightweight export saved")
    
    # Export with embeddings
    result = client.export_embedding("chatbot_1", quantize=True)
    print(f"✓ Embedding export: {result['size_kb']} KB (quantized)")
    
    # Get stats
    stats = client.get_stats()
    print(f"Size estimates:")
    for key, value in stats['size_estimates_kb'].items():
        print(f"  - {key}: {value} KB")


# ============================================================================
# INTEGRATION WITH CHATBOT BUILDER
# ============================================================================

"""
To integrate with the ChatBot model class:

1. Add export method to ChatBot model:

class ChatBot(db.Model):
    # ... existing fields ...
    
    def export_json(self, format_type='lightweight'):
        '''Export chatbot model as JSON.'''
        # Build Q&A pairs from intents
        qa_pairs = []
        for intent in self.intents:
            if intent.responses and intent.utterances:
                qa_pairs.append({
                    'question': intent.utterances[0].text,
                    'answer': intent.responses[0].text,
                    'keywords': [u.text.split() for u in intent.utterances]
                })
        
        # Create exporter
        from export_chatbot_model import ChatbotModelExporter
        
        class TempChatbot:
            def __init__(self, name, qa_pairs):
                self.chatbot_name = name
                self.qa_pairs = qa_pairs
        
        temp = TempChatbot(self.name, qa_pairs)
        exporter = ChatbotModelExporter(temp)
        
        # Choose format
        if format_type == 'lightweight':
            result = exporter.export_lightweight(f"export_{self.id}.json")
        elif format_type == 'embedding':
            result = exporter.export_embedding_model(f"export_{self.id}.json")
        
        return result

2. Then use in API route:

@app.route('/api/chatbots/<int:id>/export/<format>', methods=['GET'])
def export_chatbot(id, format):
    chatbot = ChatBot.query.get(id)
    if not chatbot:
        return {'error': 'Not found'}, 404
    
    result = chatbot.export_json(format_type=format)
    
    with open(result['output_file'], 'rb') as f:
        return f.read(), 200, {
            'Content-Type': 'application/json',
            'Content-Disposition': f'attachment; filename="chatbot_{id}.json"'
        }
"""


# ============================================================================
# DEPLOYMENT EXAMPLE
# ============================================================================

"""
To deploy the export system:

1. Install dependencies:
   pip install flask flask-cors sentence-transformers torch

2. Create config for export:
   
   class Config:
        EXPORT_DIR = 'exports/'  # Directory for temporary exports
        EXPORT_MAX_SIZE = 100  # Max MB for downloads
        MODELS = {
            'lightweight': 'all-MiniLM-L6-v2',
            'embedding': 'all-mpnet-base-v2'
        }

3. Run the app:
   python app.py

4. Test endpoints:
   curl http://localhost:5000/api/export/formats
   curl http://localhost:5000/api/export/stats
   curl http://localhost:5000/api/export/health

5. Export a chatbot:
   curl http://localhost:5000/api/export/lightweight/1 > model.json
   
6. Use in mobile app:
   - Copy model.json to app assets
   - Load with MobileChatbotClient
   - Get answers: client.get_answer("question")

7. Deploy web bundle:
   curl http://localhost:5000/api/export/web-bundle > chatbot.zip
   unzip chatbot.zip
   # Upload folder to web server
"""


# ============================================================================
# MONITORING & LOGGING
# ============================================================================

"""
Add monitoring for export operations:

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In export routes, add logging:

@export_routes.route('/lightweight/<chatbot_id>', methods=['GET'])
def export_lightweight(chatbot_id):
    start_time = datetime.now()
    try:
        # ... export logic ...
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Exported lightweight: {chatbot_id} ({elapsed:.2f}s)")
        return result, 200
    except Exception as e:
        logger.error(f"Export failed: {chatbot_id} - {e}")
        return {'error': str(e)}, 500

# Monitor:
# - Export times
# - File sizes
# - Error rates
# - Which formats are most used
"""


# ============================================================================
# FRONTEND INTEGRATION
# ============================================================================

"""
Add export buttons to web UI (JavaScript):

async function exportChatbot(chatbotId, format) {
    try {
        const response = await fetch(`/api/export/${format}/${chatbotId}`);
        const blob = await response.blob();
        
        // Download file
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chatbot_${chatbotId}.json`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        
        showNotification('✓ Export successful');
    } catch (error) {
        showNotification(`✗ Export failed: ${error.message}`);
    }
}

// Add buttons to chatbot UI:
<button onclick="exportChatbot(1, 'lightweight')">Export for Mobile</button>
<button onclick="exportChatbot(1, 'embedding')">Export with AI</button>
<button onclick="exportChatbot(1, 'web_bundle')">Deploy Web App</button>
"""
