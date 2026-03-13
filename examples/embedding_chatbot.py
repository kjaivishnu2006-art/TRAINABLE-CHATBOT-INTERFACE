"""Advanced Embedding-Based Q&A Chatbot Module."""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings

try:
    from sentence_transformers import SentenceTransformer, util
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    warnings.warn(
        "sentence-transformers not installed. Install with: "
        "pip install sentence-transformers",
        ImportWarning
    )


class EmbeddingQAChatbot:
    """Advanced chatbot using semantic embeddings for Q&A matching.
    
    This chatbot uses pre-trained sentence transformers to create semantic
    embeddings of questions and answers, enabling intelligent matching based
    on meaning rather than just keywords.
    """
    
    def __init__(
        self,
        dataset_path: str,
        model_name: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.4,
        use_embeddings: bool = True
    ):
        """Initialize chatbot with embeddings model.
        
        Args:
            dataset_path: Path to JSON file containing Q&A pairs
            model_name: Name of sentence-transformer model to use
                - "all-MiniLM-L6-v2" (default) - Fast, good quality (33MB)
                - "all-mpnet-base-v2" - Better quality (438MB)
                - "paraphrase-MiniLM-L6-v2" - Good for paraphrasing (80MB)
            similarity_threshold: Minimum similarity score (0-1)
            use_embeddings: Whether to use embeddings or fallback to keyword
            
        Raises:
            FileNotFoundError: If dataset file doesn't exist
            ValueError: If dataset format is invalid
            ImportError: If sentence-transformers not installed
        """
        if not EMBEDDINGS_AVAILABLE and use_embeddings:
            raise ImportError(
                "sentence-transformers is required. Install with: "
                "pip install sentence-transformers"
            )
        
        self.dataset_path = Path(dataset_path)
        self.model_name = model_name
        self.similarity_threshold = similarity_threshold
        self.use_embeddings = use_embeddings and EMBEDDINGS_AVAILABLE
        
        self.qa_pairs = []
        self.chatbot_name = "Semantic Chatbot"
        self.model = None
        self.question_embeddings = []
        
        self._load_dataset()
        
        if self.use_embeddings:
            self._initialize_embeddings()
    
    def _load_dataset(self) -> None:
        """Load Q&A pairs from JSON file."""
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'qa_pairs' not in data:
                raise ValueError("Dataset must contain 'qa_pairs' key")
            
            self.qa_pairs = data['qa_pairs']
            self.chatbot_name = data.get('chatbot_name', 'Semantic Chatbot')
            
            print(f"✓ Loaded {len(self.qa_pairs)} Q&A pairs")
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    
    def _initialize_embeddings(self) -> None:
        """Initialize sentence transformer model and encode questions."""
        print(f"🔄 Loading embedding model: {self.model_name}...")
        
        try:
            self.model = SentenceTransformer(self.model_name)
            print("✓ Model loaded successfully")
            
            # Encode all questions
            print("🔄 Encoding questions...")
            questions = [qa['question'] for qa in self.qa_pairs]
            self.question_embeddings = self.model.encode(
                questions,
                convert_to_tensor=True,
                show_progress_bar=len(questions) > 10
            )
            print(f"✓ Encoded {len(questions)} questions")
            
        except Exception as e:
            print(f"❌ Error loading embeddings model: {e}")
            self.use_embeddings = False
            self.model = None
    
    def _calculate_embedding_similarity(
        self,
        user_input: str,
        top_k: int = 1
    ) -> List[Tuple[int, float]]:
        """Calculate similarity using embeddings.
        
        Args:
            user_input: User's question
            top_k: Number of top matches to return
            
        Returns:
            List of (qa_pair_index, similarity_score) tuples
        """
        if not self.model or not self.question_embeddings.size(0) > 0:
            return []
        
        # Encode user input
        user_embedding = self.model.encode(user_input, convert_to_tensor=True)
        
        # Calculate similarities
        similarities = util.pytorch_cos_sim(user_embedding, self.question_embeddings)[0]
        
        # Get top k matches
        top_results = []
        top_k_indices = np.argsort(-similarities.cpu().numpy())[:top_k]
        
        for idx in top_k_indices:
            similarity_score = float(similarities[idx])
            if similarity_score >= self.similarity_threshold:
                top_results.append((int(idx), similarity_score))
        
        return top_results
    
    def _calculate_keyword_similarity(
        self,
        user_input: str
    ) -> Tuple[Optional[int], float]:
        """Fallback keyword-based similarity (for when embeddings unavailable).
        
        Args:
            user_input: User's question
            
        Returns:
            Tuple of (qa_pair_index, similarity_score)
        """
        import re
        
        user_words = set(re.sub(r'[^\w\s]', ' ', user_input.lower()).split())
        best_idx = None
        best_score = 0.0
        
        for idx, qa_pair in enumerate(self.qa_pairs):
            # Check against question
            question_words = set(
                re.sub(r'[^\w\s]', ' ', qa_pair['question'].lower()).split()
            )
            question_match = len(user_words & question_words) / max(len(user_words), 1)
            
            # Check against keywords
            keyword_words = set()
            for keyword in qa_pair.get('keywords', []):
                keyword_words.update(
                    re.sub(r'[^\w\s]', ' ', keyword.lower()).split()
                )
            
            keyword_match = len(user_words & keyword_words) / max(len(user_words), 1)
            
            # Combined score
            similarity = (question_match * 0.75) + (keyword_match * 0.25)
            
            if similarity > best_score:
                best_score = similarity
                best_idx = idx
        
        return best_idx, best_score
    
    def find_answer(
        self,
        user_input: str,
        return_all_scores: bool = False
    ) -> Dict:
        """Find best matching answer for user input.
        
        Args:
            user_input: User's question
            return_all_scores: Whether to return all match scores
            
        Returns:
            Dictionary with:
                - answer: Matched answer text
                - confidence: Confidence score (0-1)
                - method: "embedding" or "keyword"
                - question: Original question from dataset
                - all_scores: List of all match scores (if return_all_scores=True)
        """
        if not user_input.strip():
            return {
                'answer': None,
                'confidence': 0.0,
                'method': None,
                'question': None
            }
        
        result = {
            'answer': None,
            'confidence': 0.0,
            'method': None,
            'question': None,
            'all_scores': []
        }
        
        if self.use_embeddings:
            # Use embedding-based matching
            top_matches = self._calculate_embedding_similarity(user_input, top_k=1)
            
            if top_matches:
                qa_idx, confidence = top_matches[0]
                qa_pair = self.qa_pairs[qa_idx]
                
                result['answer'] = qa_pair['answer']
                result['confidence'] = confidence
                result['method'] = 'embedding'
                result['question'] = qa_pair['question']
                
                if return_all_scores:
                    all_matches = self._calculate_embedding_similarity(user_input, top_k=len(self.qa_pairs))
                    result['all_scores'] = [
                        {
                            'question': self.qa_pairs[idx]['question'],
                            'score': float(score)
                        }
                        for idx, score in all_matches
                    ]
        else:
            # Fallback to keyword matching
            qa_idx, confidence = self._calculate_keyword_similarity(user_input)
            
            if qa_idx is not None and confidence >= self.similarity_threshold * 0.75:
                qa_pair = self.qa_pairs[qa_idx]
                
                result['answer'] = qa_pair['answer']
                result['confidence'] = confidence
                result['method'] = 'keyword'
                result['question'] = qa_pair['question']
        
        return result
    
    def chat(self) -> None:
        """Run interactive chat loop."""
        print(f"\n{'='*60}")
        print(f"  Welcome to {self.chatbot_name}")
        print(f"{'='*60}")
        
        method = "🧠 Semantic Embeddings" if self.use_embeddings else "🔑 Keyword Matching"
        print(f"Using: {method}")
        print(f"Similarity Threshold: {self.similarity_threshold}")
        print("Type 'quit' to exit, 'help' for options\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    print(f"{self.chatbot_name}: Goodbye! 👋")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'list':
                    self.list_questions()
                    continue
                
                result = self.find_answer(user_input)
                
                if result['answer']:
                    confidence_pct = int(result['confidence'] * 100)
                    method_emoji = "🧠" if result['method'] == 'embedding' else "🔑"
                    
                    print(f"\n{self.chatbot_name}: {result['answer']}")
                    print(f"({method_emoji} {result['method'].title()} - "
                          f"Confidence: {confidence_pct}%)\n")
                else:
                    print(f"\n{self.chatbot_name}: Sorry, I don't have an answer to that.")
                    print("Try asking about Python, JSON, machine learning, or virtual environments.\n")
                
            except KeyboardInterrupt:
                print(f"\n{self.chatbot_name}: Goodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_help(self) -> None:
        """Display available commands."""
        print("\n📚 Available Commands:")
        print("  - quit: Exit the chatbot")
        print("  - help: Show this message")
        print("  - list: Show all Q&A topics\n")
        
        method = "semantic" if self.use_embeddings else "keyword"
        print(f"Currently using: {method} matching\n")
    
    def list_questions(self) -> None:
        """Print all available questions."""
        print(f"\n{'='*60}")
        print(f"  {len(self.qa_pairs)} Questions Available")
        print(f"{'='*60}\n")
        
        for i, qa in enumerate(self.qa_pairs, 1):
            print(f"{i:2d}. {qa['question']}")
            if qa.get('keywords'):
                keywords = ", ".join(qa.get('keywords', []))
                print(f"    Keywords: {keywords}")
            print()
    
    def get_statistics(self) -> Dict:
        """Get chatbot statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_qa_pairs': len(self.qa_pairs),
            'model_name': self.model_name if self.use_embeddings else 'keyword',
            'using_embeddings': self.use_embeddings,
            'similarity_threshold': self.similarity_threshold,
            'model_loaded': self.model is not None
        }


def main():
    """Main entry point for the chatbot."""
    dataset_path = Path(__file__).parent / "qa_dataset.json"
    
    try:
        # Try to use embeddings, fallback to keywords if not available
        chatbot = EmbeddingQAChatbot(
            str(dataset_path),
            model_name="all-MiniLM-L6-v2",
            similarity_threshold=0.4,
            use_embeddings=True
        )
        chatbot.chat()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please provide a valid dataset JSON file.")
    except ValueError as e:
        print(f"Error: {e}")
    except ImportError as e:
        print(f"Warning: {e}")
        print("\nTo use embedding-based matching, install with:")
        print("  pip install sentence-transformers")
        print("\nFalling back to keyword-based matching...")
        
        try:
            from simple_chatbot import SimpleQAChatbot
            chatbot = SimpleQAChatbot(str(dataset_path))
            chatbot.chat()
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
