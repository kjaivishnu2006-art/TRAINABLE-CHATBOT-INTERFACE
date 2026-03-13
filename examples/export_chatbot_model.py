"""
Chatbot Model Exporter for Mobile Applications
Exports trained chatbot models to portable JSON format for mobile deployment
"""

import json
import gzip
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ChatbotModelExporter:
    """Export chatbot models to JSON format for mobile apps."""
    
    def __init__(self, chatbot_instance):
        """Initialize exporter with chatbot instance.
        
        Args:
            chatbot_instance: SimpleQAChatbot or EmbeddingQAChatbot instance
        """
        self.chatbot = chatbot_instance
        self.export_date = datetime.now().isoformat()
    
    def export_full_model(
        self,
        output_path: str,
        include_embeddings: bool = False,
        compress: bool = False,
        pretty_print: bool = True
    ) -> Dict[str, Any]:
        """Export complete chatbot model and dataset.
        
        Args:
            output_path: Path where JSON will be saved
            include_embeddings: Whether to include embedding vectors (large file)
            compress: Whether to gzip compress the output
            pretty_print: Whether to prettify JSON (for readability)
            
        Returns:
            Export metadata with file size and statistics
        """
        model_data = self._build_model_data(include_embeddings=include_embeddings)
        
        # Serialize to JSON
        json_str = json.dumps(model_data, indent=2 if pretty_print else None)
        json_bytes = json_str.encode('utf-8')
        
        output_file = Path(output_path)
        
        if compress:
            # Compress with gzip
            compressed = gzip.compress(json_bytes)
            output_file.write_bytes(compressed)
            original_size = len(json_bytes)
            compressed_size = len(compressed)
            compression_ratio = 1 - (compressed_size / original_size)
        else:
            output_file.write_bytes(json_bytes)
            original_size = len(json_bytes)
            compressed_size = 0
            compression_ratio = 0
        
        return {
            'status': 'success',
            'output_file': str(output_file),
            'original_size_kb': round(original_size / 1024, 2),
            'compressed_size_kb': round(compressed_size / 1024, 2) if compress else None,
            'compression_ratio': round(compression_ratio * 100, 1) if compress else None,
            'include_embeddings': include_embeddings,
            'qa_pairs': len(self.chatbot.qa_pairs),
            'export_date': self.export_date
        }
    
    def export_lightweight(
        self,
        output_path: str,
        pretty_print: bool = True
    ) -> Dict[str, Any]:
        """Export lightweight version (no embeddings) for mobile apps.
        
        Optimized for mobile with:
        - Only Q&A pairs
        - No embedding vectors
        - Minimal metadata
        - Suitable for keyword matching
        
        Args:
            output_path: Path where JSON will be saved
            pretty_print: Whether to prettify JSON
            
        Returns:
            Export metadata
        """
        model_data = {
            'metadata': {
                'version': '2.0',
                'type': 'lightweight',
                'chatbot_name': self.chatbot.chatbot_name,
                'export_date': self.export_date,
                'total_qa_pairs': len(self.chatbot.qa_pairs)
            },
            'qa_pairs': [
                {
                    'id': idx,
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'keywords': qa.get('keywords', [])
                }
                for idx, qa in enumerate(self.chatbot.qa_pairs)
            ]
        }
        
        json_str = json.dumps(model_data, indent=2 if pretty_print else None)
        json_bytes = json_str.encode('utf-8')
        
        Path(output_path).write_bytes(json_bytes)
        
        return {
            'status': 'success',
            'output_file': str(output_path),
            'size_kb': round(len(json_bytes) / 1024, 2),
            'qa_pairs': len(self.chatbot.qa_pairs),
            'type': 'lightweight'
        }
    
    def export_embedding_model(
        self,
        output_path: str,
        quantize_embeddings: bool = True,
        pretty_print: bool = False
    ) -> Dict[str, Any]:
        """Export model with embeddings for intelligent mobile matching.
        
        Args:
            output_path: Path where JSON will be saved
            quantize_embeddings: Quantize embeddings to int8 (reduces size by 75%)
            pretty_print: Whether to prettify JSON
            
        Returns:
            Export metadata
        """
        # Check if embeddings are available
        if not hasattr(self.chatbot, 'question_embeddings'):
            raise ValueError("Chatbot instance does not have embeddings")
        
        if self.chatbot.question_embeddings is None:
            raise ValueError("Embeddings not initialized")
        
        # Convert embeddings to list
        embeddings_array = self.chatbot.question_embeddings.cpu().numpy().tolist()
        
        # Quantize if requested
        if quantize_embeddings:
            embeddings_array = self._quantize_embeddings(embeddings_array)
        
        model_data = {
            'metadata': {
                'version': '2.0',
                'type': 'embedding_model',
                'chatbot_name': self.chatbot.chatbot_name,
                'model_name': getattr(self.chatbot, 'model_name', 'unknown'),
                'similarity_threshold': getattr(self.chatbot, 'similarity_threshold', 0.3),
                'export_date': self.export_date,
                'total_qa_pairs': len(self.chatbot.qa_pairs),
                'embedding_dimension': len(embeddings_array[0]) if embeddings_array else 0,
                'quantized': quantize_embeddings
            },
            'qa_pairs': [
                {
                    'id': idx,
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'keywords': qa.get('keywords', []),
                    'embedding': embeddings_array[idx]
                }
                for idx, qa in enumerate(self.chatbot.qa_pairs)
            ]
        }
        
        json_str = json.dumps(model_data, indent=2 if pretty_print else None)
        json_bytes = json_str.encode('utf-8')
        
        Path(output_path).write_bytes(json_bytes)
        
        return {
            'status': 'success',
            'output_file': str(output_path),
            'size_kb': round(len(json_bytes) / 1024, 2),
            'qa_pairs': len(self.chatbot.qa_pairs),
            'embedding_dimension': len(embeddings_array[0]) if embeddings_array else 0,
            'quantized': quantize_embeddings,
            'type': 'embedding_model'
        }
    
    def export_web_bundle(
        self,
        output_dir: str,
        include_embeddings: bool = True
    ) -> Dict[str, Any]:
        """Export as web-ready bundle with HTML/JS client.
        
        Args:
            output_dir: Directory to save bundle
            include_embeddings: Whether to include embeddings
            
        Returns:
            Export metadata
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export model JSON
        model_path = output_dir / "model.json"
        model_info = self.export_lightweight(str(model_path))
        
        # Export HTML client
        html_path = output_dir / "chatbot.html"
        self._write_html_client(html_path)
        
        # Export JS client
        js_path = output_dir / "chatbot.js"
        self._write_js_client(js_path)
        
        return {
            'status': 'success',
            'output_directory': str(output_dir),
            'files': [
                str(model_path),
                str(html_path),
                str(js_path)
            ],
            'model_size_kb': model_info['size_kb']
        }
    
    def _build_model_data(self, include_embeddings: bool = False) -> Dict:
        """Build complete model data structure."""
        model_data = {
            'metadata': {
                'version': '2.0',
                'type': 'full_model',
                'chatbot_name': self.chatbot.chatbot_name,
                'export_date': self.export_date,
                'total_qa_pairs': len(self.chatbot.qa_pairs)
            },
            'qa_pairs': self.chatbot.qa_pairs
        }
        
        # Add embeddings if available and requested
        if include_embeddings and hasattr(self.chatbot, 'question_embeddings'):
            if self.chatbot.question_embeddings is not None:
                embeddings_array = self.chatbot.question_embeddings.cpu().numpy().tolist()
                model_data['embeddings'] = {
                    'type': 'cosine_similarity',
                    'dimension': len(embeddings_array[0]) if embeddings_array else 0,
                    'vectors': embeddings_array
                }
        
        return model_data
    
    @staticmethod
    def _quantize_embeddings(embeddings: List[List[float]]) -> List[List[int]]:
        """Quantize float embeddings to int8.
        
        Reduces file size by ~75% with minimal accuracy loss.
        """
        import numpy as np
        
        embeddings_array = np.array(embeddings)
        
        # Scale from [-1, 1] to [-128, 127]
        quantized = (embeddings_array * 127).astype(np.int8)
        
        return quantized.tolist()
    
    @staticmethod
    def _write_html_client(output_path: Path):
        """Write standalone HTML chatbot client."""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; height: 100vh; display: flex; flex-direction: column; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; }
        .messages { flex: 1; overflow-y: auto; padding: 1rem; background: #f5f5f5; }
        .message { margin: 0.5rem 0; padding: 0.75rem 1rem; border-radius: 8px; max-width: 80%; }
        .message.user { background: #667eea; color: white; margin-left: auto; }
        .message.bot { background: white; border: 1px solid #ddd; }
        .input-area { padding: 1rem; border-top: 1px solid #ddd; display: flex; gap: 0.5rem; }
        .input-area input { flex: 1; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; }
        .input-area button { padding: 0.75rem 1.5rem; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .input-area button:hover { background: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Chatbot</h1>
        </div>
        <div class="messages" id="messages"></div>
        <div class="input-area">
            <input type="text" id="input" placeholder="Type your message..." />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script src="chatbot.js"></script>
</body>
</html>
"""
        output_path.write_text(html_content)
    
    @staticmethod
    def _write_js_client(output_path: Path):
        """Write JavaScript chatbot client."""
        js_content = """
// Mobile Chatbot Client
class MobileChatbot {
    constructor(modelPath = 'model.json') {
        this.model = null;
        this.threshold = 0.3;
        this.loadModel(modelPath);
    }
    
    async loadModel(modelPath) {
        const response = await fetch(modelPath);
        this.model = await response.json();
        console.log('✓ Model loaded:', this.model.metadata);
    }
    
    findAnswer(question) {
        if (!this.model) {
            return { answer: 'Model not loaded', confidence: 0 };
        }
        
        const inputWords = question.toLowerCase().split(/\\s+/);
        let bestMatch = null;
        let bestScore = 0;
        
        for (const qa of this.model.qa_pairs) {
            const questionWords = qa.question.toLowerCase().split(/\\s+/);
            const keywords = (qa.keywords || []).join(' ').toLowerCase().split(/\\s+/);
            
            const questionMatch = this._calculateMatch(inputWords, questionWords);
            const keywordMatch = this._calculateMatch(inputWords, keywords);
            const score = questionMatch * 0.75 + keywordMatch * 0.25;
            
            if (score > bestScore) {
                bestScore = score;
                bestMatch = qa;
            }
        }
        
        return {
            answer: bestMatch ? bestMatch.answer : null,
            question: bestMatch ? bestMatch.question : null,
            confidence: bestScore
        };
    }
    
    _calculateMatch(words1, words2) {
        const set2 = new Set(words2);
        const matches = words1.filter(w => set2.has(w)).length;
        return matches / Math.max(words1.length, 1);
    }
}

// Initialize chatbot
const chatbot = new MobileChatbot('model.json');

// UI Functions
function sendMessage() {
    const input = document.getElementById('input');
    const question = input.value.trim();
    
    if (!question) return;
    
    // Add user message
    addMessage(question, 'user');
    input.value = '';
    
    // Get response
    setTimeout(() => {
        const result = chatbot.findAnswer(question);
        const answer = result.answer || "Sorry, I don't have an answer to that.";
        addMessage(answer, 'bot');
    }, 300);
}

function addMessage(text, sender) {
    const messages = document.getElementById('messages');
    const msgEl = document.createElement('div');
    msgEl.className = 'message ' + sender;
    msgEl.textContent = text;
    messages.appendChild(msgEl);
    messages.scrollTop = messages.scrollHeight;
}

// Allow Enter key to send
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
"""
        output_path.write_text(js_content)


def main():
    """Example usage of exporter."""
    from pathlib import Path
    
    # Load chatbot
    dataset_path = Path(__file__).parent / "qa_dataset.json"
    if not dataset_path.exists():
        print(f"Dataset not found: {dataset_path}")
        return
    
    # Try embedding chatbot first, fall back to simple
    try:
        from embedding_chatbot import EmbeddingQAChatbot
        chatbot = EmbeddingQAChatbot(str(dataset_path), use_embeddings=True)
        model_type = "Embedding"
    except ImportError:
        print("ℹ️  sentence-transformers not installed, using simple chatbot")
        from simple_chatbot import SimpleQAChatbot
        chatbot = SimpleQAChatbot(str(dataset_path))
        model_type = "Simple"
    
    # Create exporter
    exporter = ChatbotModelExporter(chatbot)
    
    # Export variants
    print(f"\n📦 Exporting Chatbot Models ({model_type})\n")
    
    # 1. Lightweight for mobile
    result = exporter.export_lightweight("chatbot_lightweight.json", pretty_print=True)
    print(f"✓ Lightweight: {result['size_kb']} KB")
    print(f"  → chatbot_lightweight.json")
    
    # 2. With embeddings (if available)
    if model_type == "Embedding":
        try:
            result = exporter.export_embedding_model("chatbot_embedding.json", quantize_embeddings=True)
            print(f"✓ Embedding model: {result['size_kb']} KB (quantized)")
            print(f"  → chatbot_embedding.json")
        except Exception as e:
            print(f"⚠️  Embedding export: {e}")
    
    # 3. Web bundle
    try:
        result = exporter.export_web_bundle("chatbot_web")
        print(f"✓ Web bundle: {len(result['files'])} files")
        print(f"  → chatbot_web/")
    except Exception as e:
        print(f"⚠️  Web bundle export: {e}")
    
    print("\n✅ Export complete!")
    print("\nNext steps:")
    print("1. Use the exported JSON in mobile apps")
    print("2. Deploy web bundle to web servers")
    print("3. See EXPORT_QUICK_START.md for integration examples")


if __name__ == "__main__":
    main()
