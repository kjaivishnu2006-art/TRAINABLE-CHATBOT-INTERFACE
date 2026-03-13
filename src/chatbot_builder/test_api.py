"""
Flask API Test Script
Validates API endpoints and functionality
"""

import requests
import json
import sys
from colorama import Fore, Style, init

init()  # Initialize colorama

class APITester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.chatbot_id = None
        self.intent_id = None
        self.tests_passed = 0
        self.tests_failed = 0

    def print_header(self, text):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{text.center(60)}")
        print(f"{'='*60}{Style.RESET_ALL}\n")

    def print_success(self, text):
        print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")
        self.tests_passed += 1

    def print_error(self, text):
        print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")
        self.tests_failed += 1

    def print_info(self, text):
        print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")

    def test_health(self):
        """Test API health check"""
        self.print_header("Testing Health Check")
        
        try:
            response = requests.get(f"{self.api_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok':
                    self.print_success(f"API is healthy: {data['message']}")
                    return True
                else:
                    self.print_error(f"Unexpected status: {data['status']}")
                    return False
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.print_error(f"Cannot connect to {self.api_url}")
            self.print_info("Make sure Flask API is running: python run.py")
            return False

    def test_create_chatbot(self):
        """Test chatbot creation"""
        self.print_header("Testing Chatbot Creation")
        
        payload = {
            "name": f"Test ChatBot {self.get_timestamp()}",
            "description": "A test chatbot"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chatbots",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.chatbot_id = data['id']
                self.print_success(f"Created chatbot: {data['name']} (ID: {data['id']})")
                self.print_info(f"Response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.print_error(f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_get_chatbots(self):
        """Test getting all chatbots"""
        self.print_header("Testing Get All Chatbots")
        
        try:
            response = requests.get(f"{self.api_url}/chatbots")
            
            if response.status_code == 200:
                data = response.json()
                count = len(data)
                self.print_success(f"Retrieved {count} chatbot(s)")
                
                if count > 0:
                    self.print_info(f"Sample chatbot: {data[0]['name']}")
                
                return True
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_create_intent(self):
        """Test intent creation"""
        self.print_header("Testing Intent Creation")
        
        if not self.chatbot_id:
            self.print_error("No chatbot ID available")
            return False
        
        payload = {
            "name": "greeting",
            "description": "Greet the user",
            "priority": "high",
            "utterances": ["hello", "hi", "hey there"],
            "responses": ["Hello! How can I help?", "Hi there!"]
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chatbots/{self.chatbot_id}/intents",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.intent_id = data['id']
                self.print_success(f"Created intent: {data['name']} (ID: {data['id']})")
                self.print_info(f"Utterances: {len(data['utterances'])}, Responses: {len(data['responses'])}")
                return True
            else:
                self.print_error(f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_get_chatbot_details(self):
        """Test getting chatbot with all details"""
        self.print_header("Testing Get Chatbot Details")
        
        if not self.chatbot_id:
            self.print_error("No chatbot ID available")
            return False
        
        try:
            response = requests.get(f"{self.api_url}/chatbots/{self.chatbot_id}")
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Retrieved chatbot: {data['name']}")
                self.print_info(f"Intents: {data['intent_count']}, Entities: {data['entity_count']}")
                
                if data['intent_count'] > 0:
                    intent = data['intents'][0]
                    self.print_info(f"First intent: {intent['name']} with {len(intent['utterances'])} utterances")
                
                return True
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_update_intent(self):
        """Test intent update"""
        self.print_header("Testing Intent Update")
        
        if not self.intent_id:
            self.print_error("No intent ID available")
            return False
        
        payload = {
            "name": "greeting",
            "description": "Updated description",
            "priority": "medium",
            "utterances": ["hello", "hi", "hey", "good morning"],
            "responses": ["Hello!", "Hi there!", "Good day!"]
        }
        
        try:
            response = requests.put(
                f"{self.api_url}/intents/{self.intent_id}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Updated intent: {data['name']}")
                self.print_info(f"New utterances: {len(data['utterances'])}, New responses: {len(data['responses'])}")
                return True
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_create_entity(self):
        """Test entity creation"""
        self.print_header("Testing Entity Creation")
        
        if not self.chatbot_id:
            self.print_error("No chatbot ID available")
            return False
        
        payload = {
            "entity_id": "entity.name",
            "entity_type": "NAME",
            "description": "Person's name",
            "examples": ["John", "Alice", "Bob"]
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chatbots/{self.chatbot_id}/entities",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.print_success(f"Created entity: {data['entity_id']} ({data['entity_type']})")
                self.print_info(f"Examples: {', '.join(data['examples'])}")
                return True
            else:
                self.print_error(f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_export_chatbot(self):
        """Test chatbot export"""
        self.print_header("Testing Chatbot Export")
        
        if not self.chatbot_id:
            self.print_error("No chatbot ID available")
            return False
        
        try:
            response = requests.get(f"{self.api_url}/chatbots/{self.chatbot_id}/export")
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Exported chatbot: {data['metadata']['name']}")
                stats = data['statistics']
                self.print_info(f"Stats - Intents: {stats['total_intents']}, "
                              f"Utterances: {stats['total_utterances']}, "
                              f"Responses: {stats['total_responses']}")
                return True
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_get_stats(self):
        """Test system statistics"""
        self.print_header("Testing System Statistics")
        
        try:
            response = requests.get(f"{self.api_url}/stats")
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Retrieved system statistics")
                
                for key, value in data.items():
                    display_key = key.replace('_', ' ').title()
                    self.print_info(f"{display_key}: {value}")
                
                return True
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_delete_intent(self):
        """Test intent deletion"""
        self.print_header("Testing Intent Deletion")
        
        if not self.intent_id:
            self.print_error("No intent ID available")
            return False
        
        try:
            response = requests.delete(f"{self.api_url}/intents/{self.intent_id}")
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Deleted intent: {data['message']}")
                return True
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def test_delete_chatbot(self):
        """Test chatbot deletion"""
        self.print_header("Testing Chatbot Deletion")
        
        if not self.chatbot_id:
            self.print_error("No chatbot ID available")
            return False
        
        try:
            response = requests.delete(f"{self.api_url}/chatbots/{self.chatbot_id}")
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Deleted chatbot: {data['message']}")
                return True
            else:
                self.print_error(f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all tests"""
        self.print_header("Flask API Test Suite")
        self.print_info(f"Testing API at: {self.api_url}")
        
        tests = [
            self.test_health,
            self.test_create_chatbot,
            self.test_get_chatbots,
            self.test_create_intent,
            self.test_get_chatbot_details,
            self.test_update_intent,
            self.test_create_entity,
            self.test_export_chatbot,
            self.test_get_stats,
            self.test_delete_intent,
            self.test_delete_chatbot,
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.print_error(f"Test failed with exception: {str(e)}")

        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print(f"{Fore.GREEN}Passed: {self.tests_passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.tests_failed}{Style.RESET_ALL}")
        print(f"Total:  {total}")
        print(f"Success Rate: {percentage:.1f}%")
        
        if self.tests_failed == 0:
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"{'All Tests Passed! ✓'.center(60)}")
            print(f"{'='*60}{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.RED}{'='*60}")
            print(f"{'Some Tests Failed!'.center(60)}")
            print(f"{'='*60}{Style.RESET_ALL}\n")

    @staticmethod
    def get_timestamp():
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5000"
    
    tester = APITester(base_url)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
