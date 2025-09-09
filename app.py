import streamlit as st
import json
from ai_agent import ArymalabsAgent
from web_scraper import ArymalabsScraper
import time

# Page configuration
st.set_page_config(
    page_title="Aryma Labs AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #ff6b6b;
    }
    .agent-message {
        background-color: #e8f4fd;
        border-left-color: #1f77b4;
    }
    .demo-link {
        background-color: #ff6b6b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
    }
    .demo-link:hover {
        background-color: #ff5252;
        color: white;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'scraping_completed' not in st.session_state:
        st.session_state.scraping_completed = False

def scrape_website():
    """Scrape the website and initialize the agent"""
    with st.spinner("Scraping Aryma Labs website..."):
        scraper = ArymalabsScraper()
        result = scraper.scrape_website()
        
        # Save the scraped data
        with open('scraped_content.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Initialize the agent
        st.session_state.agent = ArymalabsAgent()
        st.session_state.scraping_completed = True
        
        st.success("Website scraping completed! AI Agent is ready.")
        return True

def display_chat_message(role, content):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message agent-message">
            <strong>AI Agent:</strong> {content}
        </div>
        """, unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Aryma Labs AI Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.write("This AI agent helps you discover Aryma Labs' services and products:")
        st.write("• **MMM Services** - Marketing Mix Modeling services")
        st.write("• **MMM Products** - Marketing Mix Modeling tools")
        st.write("• **Experimentation Products** - A/B testing and experimentation tools")
        
        st.header("Actions")
        if st.button("🔄 Reset Conversation"):
            st.session_state.conversation_started = False
            st.session_state.messages = []
            st.session_state.agent = None
            st.session_state.scraping_completed = False
            st.rerun()
        
        if st.button("📊 View Scraped Data"):
            if st.session_state.scraping_completed:
                with open('scraped_content.json', 'r') as f:
                    data = json.load(f)
                st.json(data)
            else:
                st.warning("Please scrape the website first.")
    
    # Main content area
    # Check if we need to scrape the website
    if not st.session_state.scraping_completed:
        st.info("👋 Welcome! Let's start by scraping the Aryma Labs website to gather the latest information.")
        if st.button("🚀 Start Scraping", type="primary"):
            if scrape_website():
                st.rerun()
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display conversation
            st.subheader("💬 Chat with AI Agent")
            
            # Display existing messages
            for message in st.session_state.messages:
                display_chat_message(message["role"], message["content"])
            
            # Start conversation if not started
            if not st.session_state.conversation_started:
                initial_question = st.session_state.agent.get_initial_question()
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": initial_question
                })
                display_chat_message("assistant", initial_question)
                st.session_state.conversation_started = True
        
        # Chat input - moved outside columns to avoid StreamlitAPIException
        user_input = st.chat_input("Type your message and press Enter...")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get agent response
            with st.spinner("AI Agent is thinking..."):
                try:
                    # Debug: Print what we're actually processing
                    print(f"Processing user input: '{user_input}'")
                    print(f"Message count: {len(st.session_state.messages)}")
                    
                    # Check if this is the first user response after the initial question
                    if len(st.session_state.messages) == 1:
                        # First response after initial question
                        print("Using process_user_response")
                        response = st.session_state.agent.process_user_response(user_input)
                    else:
                        # Follow-up questions
                        print("Using handle_follow_up")
                        response = st.session_state.agent.handle_follow_up(user_input)
                except Exception as e:
                    st.error(f"Error: {e}")
                    response = "I apologize, but I'm having trouble processing your request. Please try again."
            
            # Add agent response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()  # Refresh to show the new messages
        
        with col2:
            st.subheader("📋 Quick Info")
            
            if st.session_state.scraping_completed:
                # Display some stats about scraped data
                try:
                    with open('scraped_content.json', 'r') as f:
                        data = json.load(f)
                    
                    st.metric("Pages Scraped", data.get("total_pages_scraped", 0))
                    st.metric("Links Found", data.get("links_found", 0))
                    
                    # Show categories
                    categories = data.get("categorized_content", {})
                    if categories:
                        st.write("**Content Categories:**")
                        for category, content in categories.items():
                            if content:
                                st.write(f"• {category.replace('_', ' ').title()}")
                    
                except FileNotFoundError:
                    st.warning("Scraped data not found.")
            else:
                st.info("Scrape the website to see content statistics.")
            
            # Demo link
            st.markdown("---")
            st.markdown("### 🎯 Try Our Demo")
            st.markdown(f"[Visit Demo Page](https://www.arymalabs.com)")

if __name__ == "__main__":
    main()
