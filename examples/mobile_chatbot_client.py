"""
Mobile Chatbot Client
Load and use exported chatbot models in mobile applications
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np


class MobileChatbotClient:
    """Load and use exported chatbot models."""
    
    def __init__(self, model_path: str):
        """Initialize mobile client with exported model.
        
        Args:
            model_path: Path to exported JSON model
        """
        self.model_path = Path(model_path)
        self.model = self._load_model()
        self.metadata = self.model.get('metadata', {})
        self.qa_pairs = self.model.get('qa_pairs', [])
        self.embeddings = self.model.get('embeddings', {})
        self.threshold = self.metadata.get('similarity_threshold', 0.3)
    
    def _load_model(self) -> Dict:
        """Load JSON model from file."""
        with open(self.model_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_answer(self, question: str) -> Dict:
        """Get answer using hybrid matching (keywords + embeddings).
        
        Args:
            question: User's question
            
        Returns:
            Dict with answer, confidence, method, and all scores
        """
        # Try embedding-based if available
        if self.embeddings and 'vectors' in self.embeddings:
            return self._get_answer_embedding(question)
        
        # Fall back to keyword matching
        return self._get_answer_keyword(question)
    
    def _get_answer_embedding(self, question: str) -> Dict:
        """Get answer using embedding similarity."""
        # For mobile, embeddings should be pre-computed
        # This would need a lightweight embedding library
        # For now, use keyword fallback
        return self._get_answer_keyword(question)
    
    def _get_answer_keyword(self, question: str) -> Dict:
        """Get answer using keyword matching (works offline)."""
        question_words = set(question.lower().split())
        
        best_answer = None
        best_score = 0
        all_scores = []
        
        for qa in self.qa_pairs:
            qa_question_words = set(qa['question'].lower().split())
            keywords = set(' '.join(qa.get('keywords', [])).lower().split())
            
            # Calculate overlap
            question_overlap = len(question_words & qa_question_words) / len(question_words | qa_question_words)
            keyword_overlap = len(question_words & keywords) / max(len(question_words | keywords), 1)
            
            # Combined score
            score = question_overlap * 0.75 + keyword_overlap * 0.25
            
            all_scores.append({
                'question': qa['question'],
                'score': min(1.0, score)
            })
            
            if score > best_score:
                best_score = score
                best_answer = qa
        
        # Sort all scores
        all_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'answer': best_answer['answer'] if best_answer else None,
            'original_question': best_answer['question'] if best_answer else None,
            'confidence': min(1.0, best_score),
            'method': 'keyword_matching',
            'all_scores': all_scores
        }
    
    def get_similar_questions(
        self,
        question: str,
        top_k: int = 3,
        threshold: Optional[float] = None
    ) -> List[Dict]:
        """Get similar questions from knowledge base.
        
        Args:
            question: Input question
            top_k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of similar questions with scores
        """
        if threshold is None:
            threshold = self.threshold
        
        result = self.get_answer(question)
        all_scores = result.get('all_scores', [])
        
        # Filter and limit
        similar = [
            q for q in all_scores
            if q['score'] >= threshold
        ][:top_k]
        
        return similar
    
    def search_by_keyword(
        self,
        keyword: str,
        match_type: str = 'any'
    ) -> List[Dict]:
        """Search Q&A pairs by keyword.
        
        Args:
            keyword: Search keyword
            match_type: 'any' (partial) or 'exact' (full word)
            
        Returns:
            Matching Q&A pairs
        """
        keyword_lower = keyword.lower()
        results = []
        
        for qa in self.qa_pairs:
            question_text = qa['question'].lower()
            answer_text = qa['answer'].lower()
            
            if match_type == 'exact':
                if keyword_lower in question_text.split() or keyword_lower in answer_text.split():
                    results.append(qa)
            else:  # 'any'
                if keyword_lower in question_text or keyword_lower in answer_text:
                    results.append(qa)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get model statistics and info."""
        return {
            'total_qa_pairs': len(self.qa_pairs),
            'model_type': self.metadata.get('type', 'unknown'),
            'chatbot_name': self.metadata.get('chatbot_name', 'Unknown'),
            'export_date': self.metadata.get('export_date', 'Unknown'),
            'has_embeddings': bool(self.embeddings),
            'threshold': self.threshold
        }
    
    def export_answers_csv(self, output_path: str):
        """Export Q&A pairs as CSV for analysis."""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'question', 'answer'])
            writer.writeheader()
            
            for idx, qa in enumerate(self.qa_pairs):
                writer.writerow({
                    'id': idx,
                    'question': qa['question'],
                    'answer': qa['answer']
                })


class FlutterChatbotClient(MobileChatbotClient):
    """Flutter mobile app chatbot client.
    
    Provides Dart-compatible API for Flutter apps.
    """
    
    def to_dart_map(self) -> str:
        """Export model as Dart map code for Flutter."""
        dart_code = f'''
const chatbotModel = {{
  'metadata': {{
    'chatbot_name': '{self.metadata.get('chatbot_name', 'ChatBot')}',
    'total_qa_pairs': {len(self.qa_pairs)},
    'threshold': {self.threshold}
  }},
  'qa_pairs': [
'''
        for qa in self.qa_pairs:
            dart_code += f"""    {{
      'question': '''{json.dumps(qa['question'])}''',
      'answer': '''{json.dumps(qa['answer'])}''',
      'keywords': {json.dumps(qa.get('keywords', []))}
    }},
"""
        dart_code += "  ]\n};"
        return dart_code


class ReactNativeChatbotClient(MobileChatbotClient):
    """React Native mobile app chatbot client."""
    
    def to_javascript_object(self) -> str:
        """Export model as JavaScript object for React Native."""
        return f"""
// Chatbot Model - React Native
export const chatbotModel = {json.dumps(self.model, indent=2)};

// Usage:
// import {{ chatbotModel }} from './model';
// const client = new ChatbotClient(chatbotModel);
// const response = client.getAnswer(userQuestion);
"""


def main():
    """Example usage."""
    # Load exported model
    model_path = Path("chatbot_lightweight.json")
    
    # Try lightweight first, then embedding
    if not model_path.exists():
        model_path = Path("sample_export_lightweight.json")
    
    if not model_path.exists():
        print("Model not found. Export a model first using export_chatbot_model.py")
        print("Available: run 'python export_chatbot_model.py' first")
        return
    
    client = MobileChatbotClient(str(model_path))
    
    print("\n📱 Mobile Chatbot Client\n")
    
    # Show statistics
    stats = client.get_statistics()
    print(f"Model: {stats['chatbot_name']}")
    print(f"Q&A Pairs: {stats['total_qa_pairs']}")
    print(f"Type: {stats['model_type']}\n")
    
    # Test answers
    test_questions = [
        "What is Python?",
        "How do I install Python?",
        "Tell me about Java"
    ]
    
    print("Testing Answers:")
    print("-" * 50)
    for q in test_questions:
        result = client.get_answer(q)
        print(f"\nQ: {q}")
        print(f"A: {result['answer'][:100]}..." if len(result['answer'] or '') > 100 else f"A: {result['answer']}")
        print(f"Confidence: {result['confidence']:.2%}")
    
    # Search by keyword
    print("\n\nKeyword Search Test:")
    print("-" * 50)
    results = client.search_by_keyword("Python")
    print(f"Found {len(results)} results for 'Python':")
    for r in results[:3]:
        print(f"  - {r['question']}")
    
    # Show similar questions
    print("\n\nSimilar Questions Test:")
    print("-" * 50)
    similar = client.get_similar_questions("How to use Python?", top_k=3)
    print("Similar to 'How to use Python?':")
    for s in similar:
        print(f"  - {s['question']} (score: {s['score']:.2%})")


if __name__ == "__main__":
    main()
