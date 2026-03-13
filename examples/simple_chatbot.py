"""Simple Q&A Chatbot Module."""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class SimpleQAChatbot:
    """A basic chatbot that matches questions to a Q&A dataset."""
    
    def __init__(self, dataset_path: str):
        """Initialize chatbot with Q&A dataset.
        
        Args:
            dataset_path: Path to JSON file containing Q&A pairs
            
        Raises:
            FileNotFoundError: If dataset file doesn't exist
            ValueError: If dataset format is invalid
        """
        self.dataset_path = Path(dataset_path)
        self.qa_pairs = []
        self.chatbot_name = "Chatbot"
        self._load_dataset()
    
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
            self.chatbot_name = data.get('chatbot_name', 'Chatbot')
            
            print(f"✓ Loaded {len(self.qa_pairs)} Q&A pairs")
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for matching.
        
        Args:
            text: Raw text input
            
        Returns:
            Cleaned and lowercased text
        """
        # Remove punctuation and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()
    
    def _calculate_similarity(self, user_input: str, qa_pair: Dict) -> float:
        """Calculate similarity score between user input and Q&A pair.
        
        Args:
            user_input: User's question
            qa_pair: Q&A pair from dataset
            
        Returns:
            Similarity score (0-1)
        """
        user_words = set(self._preprocess_text(user_input).split())
        
        # Check against question
        question_words = set(self._preprocess_text(qa_pair['question']).split())
        question_match = len(user_words & question_words) / max(len(user_words), 1)
        
        # Check against keywords
        keyword_words = set()
        for keyword in qa_pair.get('keywords', []):
            keyword_words.update(self._preprocess_text(keyword).split())
        
        keyword_match = len(user_words & keyword_words) / max(len(user_words), 1)
        
        # Combined score (75% question, 25% keywords)
        similarity = (question_match * 0.75) + (keyword_match * 0.25)
        
        return similarity
    
    def find_answer(self, user_input: str, threshold: float = 0.3) -> Tuple[Optional[str], float]:
        """Find best matching answer for user input.
        
        Args:
            user_input: User's question
            threshold: Minimum similarity score (0-1)
            
        Returns:
            Tuple of (answer, confidence_score) or (None, 0) if no match
        """
        if not user_input.strip():
            return None, 0.0
        
        best_match = None
        best_score = 0.0
        
        # Find best matching Q&A pair
        for qa_pair in self.qa_pairs:
            similarity = self._calculate_similarity(user_input, qa_pair)
            
            if similarity > best_score:
                best_score = similarity
                best_match = qa_pair
        
        # Return answer if score exceeds threshold
        if best_score >= threshold and best_match:
            return best_match['answer'], best_score
        
        return None, best_score
    
    def chat(self) -> None:
        """Run interactive chat loop."""
        print(f"\n{'='*60}")
        print(f"  Welcome to {self.chatbot_name}")
        print(f"{'='*60}")
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
                
                answer, confidence = self.find_answer(user_input)
                
                if answer:
                    confidence_pct = int(confidence * 100)
                    print(f"\n{self.chatbot_name}: {answer}")
                    print(f"(Confidence: {confidence_pct}%)\n")
                else:
                    print(f"\n{self.chatbot_name}: Sorry, I don't have an answer to that. ")
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
        
        print("📖 Available Topics:")
        for i, qa in enumerate(self.qa_pairs, 1):
            print(f"  {i}. {qa['question']}")
        print()
    
    def list_questions(self) -> None:
        """Print all available questions."""
        print(f"\n{'='*60}")
        print(f"  {len(self.qa_pairs)} Questions Available")
        print(f"{'='*60}\n")
        
        for i, qa in enumerate(self.qa_pairs, 1):
            print(f"{i:2d}. {qa['question']}")
            keywords = ", ".join(qa.get('keywords', []))
            print(f"    Keywords: {keywords}\n")


def main():
    """Main entry point for the chatbot."""
    dataset_path = Path(__file__).parent / "qa_dataset.json"
    
    try:
        chatbot = SimpleQAChatbot(str(dataset_path))
        chatbot.chat()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please provide a valid dataset JSON file.")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
