import json
import os
import requests
from typing import Dict, List, Optional
from huggingface_hub import InferenceClient
from config import HUGGINGFACE_API_KEY, CATEGORIES, DEMO_URL

class ArymalabsAgent:
    def __init__(self, scraped_data_path: str = "scraped_content.json"):
        self.hf_api_key = HUGGINGFACE_API_KEY
        self.hf_client = InferenceClient(token=self.hf_api_key) if self.hf_api_key else None
        self.scraped_data = self.load_scraped_data(scraped_data_path)
        self.conversation_history = []
        self.user_category = None
        
    def load_scraped_data(self, file_path: str) -> Dict:
        """Load scraped data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Scraped data file {file_path} not found. Please run the scraper first.")
            return {"main_content": "", "categorized_content": {}, "sections": {}}
    
    def get_initial_question(self) -> str:
        """Return the initial question for new users"""
        return "Hello! I'm the Aryma Labs AI Agent. I can help you learn about our MMM Services, MMM Products, or Experimentation Products. What would you like to know?"
    
    def handle_general_query(self, user_input: str) -> str:
        """Handle general queries about Aryma Labs"""
        print(f"🌐 [GENERAL] Handling general query: {user_input[:50]}...")
        
        # Get all available content for general queries
        all_content = ""
        for category, content in self.scraped_data.get("categorized_content", {}).items():
            all_content += f"\n\n{category}:\n{content}"
        
        # Add main content if available
        if self.scraped_data.get("main_content"):
            all_content = self.scraped_data["main_content"] + all_content
        
        if not all_content.strip():
            all_content = "Aryma Labs is a company specializing in Marketing Mix Modeling (MMM) solutions, products, and experimentation services."
        
        # Generate response using all available content
        response = self.generate_response(user_input, all_content, "GENERAL")
        
        # Add demo link
        response += f"\n\n[Contact Us for Demo]({DEMO_URL})"
        
        return response
    
    def process_user_response(self, user_input: str) -> str:
        """Process user response and determine their category"""
        print(f"\n🎯 [PROCESS] Processing user response: {user_input[:50]}...")
        user_input_lower = user_input.lower()
        
        # Determine user's category based on their response
        if any(keyword in user_input_lower for keyword in ['mmm service', 'service', 'services', 'mmm services']):
            self.user_category = "MMM_SERVICES"
            print(f"📂 [PROCESS] Category determined: MMM_SERVICES")
        elif any(keyword in user_input_lower for keyword in ['mmm product', 'product', 'products', 'mmm products']):
            self.user_category = "MMM_PRODUCTS"
            print(f"📂 [PROCESS] Category determined: MMM_PRODUCTS")
        elif any(keyword in user_input_lower for keyword in ['experimentation', 'experiment', 'testing', 'experimentation products']):
            self.user_category = "EXPERIMENTATION_PRODUCTS"
            print(f"📂 [PROCESS] Category determined: EXPERIMENTATION_PRODUCTS")
        elif 'mmm' in user_input_lower and not any(keyword in user_input_lower for keyword in ['service', 'product', 'experiment']):
            # If they just say "MMM" without specifying, default to services
            self.user_category = "MMM_SERVICES"
            print(f"📂 [PROCESS] Category determined: MMM_SERVICES (default for 'mmm')")
        else:
            # Handle general queries about Aryma Labs
            print(f"❓ [PROCESS] No clear category, trying to answer generally")
            return self.handle_general_query(user_input)
        
        # Get relevant content for the selected category
        relevant_content = self.get_relevant_content(self.user_category)
        print(f"📄 [PROCESS] Retrieved content: {len(relevant_content)} characters")
        
        # Generate response using LLM
        response = self.generate_response(user_input, relevant_content, self.user_category)
        
        # Add demo link
        response += f"\n\n[Contact Us for Demo]({DEMO_URL})"
        print(f"✅ [PROCESS] Final response ready: {len(response)} characters")
        # Determine response source based on length (AI responses are typically longer)
        response_source = "HUGGING FACE AI" if len(response) > 320 else "FALLBACK SYSTEM"
        print(f"🎯 [SUMMARY] Response source: {response_source}")
        
        return response
    
    def get_relevant_content(self, category: str) -> str:
        """Get content relevant to the user's selected category"""
        if category not in self.scraped_data.get("categorized_content", {}):
            return self.scraped_data.get("main_content", "")
        
        category_content = self.scraped_data["categorized_content"][category]
        if isinstance(category_content, list):
            return " ".join(category_content)
        return str(category_content)
    
    def generate_response(self, user_input: str, relevant_content: str, category: str) -> str:
        """Generate AI response using Hugging Face InferenceClient with fallback"""
        print(f"\n🤖 [AI AGENT] Generating response for category: {category}")
        print(f"📝 [AI AGENT] User input: {user_input[:100]}...")
        
        # Try Hugging Face InferenceClient first
        if self.hf_client:
            print("🔑 [AI AGENT] Hugging Face client available, attempting AI generation...")
            try:
                # Use summarization task which works with the current API
                try:
                    print("📊 [AI AGENT] Attempting Hugging Face summarization...")
                    # Create a dynamic context for summarization
                    if category == "GENERAL":
                        context = f"""Aryma Labs is a company that provides Marketing Mix Modeling (MMM) solutions, products, and experimentation services.

Available information about Aryma Labs: {relevant_content[:1500]}

User question: {user_input}

Please provide a comprehensive and helpful response about Aryma Labs based on the information above. Be specific and informative."""
                    else:
                        context = f"""Aryma Labs specializes in {CATEGORIES.get(category, category)}. 

Available content about {CATEGORIES.get(category, category)}: {relevant_content[:1500]}

User question: {user_input}

Please provide a detailed and helpful response about {CATEGORIES.get(category, category)} based on the content above. Be specific and informative."""
                    
                    # Use summarization to generate response
                    response = self.hf_client.summarization(context)
                    
                    if response and hasattr(response, 'summary_text'):
                        response_text = response.summary_text
                        if response_text and len(response_text) > 10:
                            print(f"✅ [HUGGING FACE] SUCCESS! Generated AI response via summarization")
                            print(f"📏 [HUGGING FACE] Response length: {len(response_text)} characters")
                            print(f"🔗 [HUGGING FACE] Adding demo link...")
                            return response_text
                        else:
                            print(f"⚠️ [HUGGING FACE] Summarization response too short: {len(response_text) if response_text else 0} chars")
                    else:
                        print(f"⚠️ [HUGGING FACE] No summary_text in response")
                    
                except Exception as summarization_error:
                    print(f"❌ [HUGGING FACE] Summarization failed: {str(summarization_error)[:100]}...")
                    
                # Try text generation with different approach
                try:
                    print("📝 [AI AGENT] Attempting Hugging Face text generation...")
                    # Use a simple prompt for text generation
                    simple_prompt = f"Answer this question about {CATEGORIES.get(category, category)}: {user_input}"
                    
                    response = self.hf_client.text_generation(simple_prompt, max_new_tokens=100)
                    
                    if response and len(response) > 10:
                        print(f"✅ [HUGGING FACE] SUCCESS! Generated AI response via text generation")
                        print(f"📏 [HUGGING FACE] Response length: {len(response)} characters")
                        print(f"🔗 [HUGGING FACE] Adding demo link...")
                        return response
                    else:
                        print(f"⚠️ [HUGGING FACE] Text generation response too short: {len(response) if response else 0} chars")
                        
                except Exception as text_gen_error:
                    print(f"❌ [HUGGING FACE] Text generation failed: {str(text_gen_error)[:100]}...")
                
            except Exception as e:
                print(f"❌ [HUGGING FACE] InferenceClient error: {e}")
                print("🔄 [AI AGENT] Falling back to keyword-based response...")
        else:
            print("❌ [AI AGENT] No Hugging Face client available")
            print("🔄 [AI AGENT] Using fallback response...")
        
        # Fallback to keyword-based response
        print("🔧 [FALLBACK] Generating keyword-based response...")
        fallback_response = self.generate_fallback_response(user_input, relevant_content, category)
        print(f"✅ [FALLBACK] Generated fallback response: {len(fallback_response)} characters")
        print(f"🔗 [FALLBACK] Adding demo link...")
        return fallback_response
    
    def generate_fallback_response(self, user_input: str, relevant_content: str, category: str) -> str:
        """Generate a dynamic fallback response when AI API is not available"""
        user_input_lower = user_input.lower()
        
        if category == "GENERAL":
            # For general queries, provide comprehensive information
            if "about" in user_input_lower or "what is" in user_input_lower or "tell me" in user_input_lower:
                return f"Aryma Labs is a company specializing in Marketing Mix Modeling (MMM) solutions. {relevant_content[:800]}..."
            elif "contact" in user_input_lower or "how to contact" in user_input_lower:
                return f"To contact Aryma Labs, you can reach out through our website or request a demo. {relevant_content[:400]}..."
            elif "services" in user_input_lower:
                return f"Aryma Labs offers comprehensive MMM services including analysis, consulting, and implementation. {relevant_content[:600]}..."
            elif "products" in user_input_lower:
                return f"Our MMM products include advanced analytics tools and platforms. {relevant_content[:600]}..."
            else:
                return f"Aryma Labs provides Marketing Mix Modeling solutions and services. {relevant_content[:600]}..."
        else:
            category_name = CATEGORIES.get(category, category)
            
            # Dynamic responses based on user intent
            if "what" in user_input_lower or "tell me" in user_input_lower:
                return f"Based on our {category_name.lower()}, here's what we offer: {relevant_content[:600]}..."
            elif "how" in user_input_lower:
                return f"For {category_name.lower()}, here's how we can help: {relevant_content[:600]}..."
            elif "contact" in user_input_lower or "demo" in user_input_lower:
                return f"To learn more about our {category_name.lower()}, please contact us for a demo. {relevant_content[:400]}..."
            elif "price" in user_input_lower or "cost" in user_input_lower:
                return f"For pricing information about our {category_name.lower()}, please contact us for a personalized quote. {relevant_content[:400]}..."
            else:
                return f"Here's detailed information about our {category_name.lower()}: {relevant_content[:600]}..."
    
    def handle_follow_up(self, user_input: str) -> str:
        """Handle follow-up questions"""
        print(f"\n🔄 [FOLLOW-UP] Handling follow-up: {user_input[:50]}...")
        
        user_input_lower = user_input.lower()
        
        # Check for general queries that should use all content
        general_queries = [
            'about aryma', 'what is aryma', 'tell me about aryma', 'who is aryma',
            'company', 'company info', 'about the company', 'what does aryma do',
            'overview', 'introduction', 'background', 'history', 'contact',
            'how to contact', 'where is aryma', 'aryma labs', 'more information'
        ]
        
        if any(query in user_input_lower for query in general_queries):
            print(f"🌐 [FOLLOW-UP] General query detected, using all content")
            return self.handle_general_query(user_input)
        
        if not self.user_category:
            # Try to determine category from user input
            print(f"❓ [FOLLOW-UP] No category set, processing as new response")
            return self.process_user_response(user_input)
        
        print(f"📂 [FOLLOW-UP] Current category: {self.user_category}")
        
        # Check for category change requests
        old_category = self.user_category
        
        # Check for category change requests
        if any(keyword in user_input_lower for keyword in ['product', 'products', 'tool', 'tools', 'platform']):
            if 'mmm' in user_input_lower or self.user_category == "MMM_SERVICES":
                self.user_category = "MMM_PRODUCTS"
                print(f"🔄 [FOLLOW-UP] Category switched: {old_category} → MMM_PRODUCTS")
        elif any(keyword in user_input_lower for keyword in ['experiment', 'testing', 'a/b test']):
            self.user_category = "EXPERIMENTATION_PRODUCTS"
            print(f"🔄 [FOLLOW-UP] Category switched: {old_category} → EXPERIMENTATION_PRODUCTS")
        elif any(keyword in user_input_lower for keyword in ['service', 'services', 'consulting']):
            self.user_category = "MMM_SERVICES"
            print(f"🔄 [FOLLOW-UP] Category switched: {old_category} → MMM_SERVICES")
        else:
            print(f"📂 [FOLLOW-UP] Category unchanged: {self.user_category}")
        
        # Get relevant content for the user's category
        relevant_content = self.get_relevant_content(self.user_category)
        print(f"📄 [FOLLOW-UP] Retrieved content: {len(relevant_content)} characters")
        
        # Generate response
        response = self.generate_response(user_input, relevant_content, self.user_category)
        
        # Add demo link
        response += f"\n\n[Contact Us for Demo]({DEMO_URL})"
        print(f"✅ [FOLLOW-UP] Final response ready: {len(response)} characters")
        # Determine response source based on length (AI responses are typically longer)
        response_source = "HUGGING FACE AI" if len(response) > 320 else "FALLBACK SYSTEM"
        print(f"🎯 [SUMMARY] Response source: {response_source}")
        
        return response
    
    def reset_conversation(self):
        """Reset the conversation state"""
        self.conversation_history = []
        self.user_category = None

def main():
    # Test the agent
    agent = ArymalabsAgent()
    
    print("Aryma Labs AI Agent")
    print("=" * 50)
    
    # Initial question
    print(agent.get_initial_question())
    
    # Simulate user responses
    test_responses = [
        "I'm interested in MMM Services",
        "What specific services do you offer?",
        "How do your services help with attribution?"
    ]
    
    for response in test_responses:
        print(f"\nUser: {response}")
        agent_response = agent.handle_follow_up(response)
        print(f"Agent: {agent_response}")

if __name__ == "__main__":
    main()
