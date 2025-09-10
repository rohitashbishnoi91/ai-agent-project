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

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 1.2rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        border-radius: 20px 20px 5px 20px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideIn 0.3s ease-out;
    }
    .agent-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 20%;
        border-radius: 20px 20px 20px 5px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideIn 0.3s ease-out;
    }
    .demo-link {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3);
        transition: all 0.3s ease;
    }
    .demo-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,107,107,0.4);
        color: white;
        text-decoration: none;
    }
    .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    .status-online {
        background-color: #28a745;
    }
    .status-offline {
        background-color: #dc3545;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .stChatInput > div > div > div {
        border-radius: 25px !important;
        border: 2px solid #667eea !important;
    }
    .stChatInput > div > div > div:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    .quick-actions {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .quick-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .quick-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Aryma Labs AI Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your intelligent assistant for MMM Services, Products & Experimentation</p>', unsafe_allow_html=True)
    
    # Welcome card
    st.markdown("""
    <div class="welcome-card">
        <h3>🚀 Welcome to Aryma Labs AI Assistant!</h3>
        <p>I can help you learn about our Marketing Mix Modeling solutions, products, and experimentation services. 
        Ask me anything about our offerings or company!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("### 🎯 Quick Actions")
        
        # Quick action buttons
        if st.button("🏢 About Aryma Labs", key="about_btn"):
            st.session_state.quick_action = "about"
        if st.button("🔧 MMM Services", key="services_btn"):
            st.session_state.quick_action = "services"
        if st.button("📦 MMM Products", key="products_btn"):
            st.session_state.quick_action = "products"
        if st.button("🧪 Experimentation", key="experiment_btn"):
            st.session_state.quick_action = "experimentation"
        if st.button("📞 Contact Demo", key="demo_btn"):
            st.session_state.quick_action = "demo"
        
        st.markdown("### 📊 Status")
        st.markdown('<span class="status-indicator status-online"></span>AI Agent Online', unsafe_allow_html=True)
        st.markdown('<span class="status-indicator status-online"></span>Web Scraper Active', unsafe_allow_html=True)
        
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Ask about our services, products, or company
        - Be specific about what you need
        - I can help with technical questions
        - Request a demo anytime!
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.agent = None
        st.session_state.quick_action = None
    
    # Initialize agent
    if st.session_state.agent is None:
        with st.spinner("🤖 Initializing AI Agent..."):
            try:
                st.session_state.agent = ArymalabsAgent()
                st.success("✅ AI Agent ready!")
            except Exception as e:
                st.error(f"❌ Error initializing agent: {e}")
                return
    
    # Handle quick actions
    if st.session_state.quick_action:
        quick_actions = {
            "about": "Tell me about Aryma Labs",
            "services": "I'm interested in MMM Services",
            "products": "I'm interested in MMM Products", 
            "experimentation": "I'm interested in Experimentation Products",
            "demo": "I want to request a demo"
        }
        
        if st.session_state.quick_action in quick_actions:
            user_input = quick_actions[st.session_state.quick_action]
            st.session_state.quick_action = None
            
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get agent response
            with st.spinner("🤖 AI Agent is thinking..."):
                try:
                    if len(st.session_state.messages) == 1:
                        response = st.session_state.agent.process_user_response(user_input)
                    else:
                        response = st.session_state.agent.handle_follow_up(user_input)
                except Exception as e:
                    response = f"I apologize, but I'm having trouble processing your request. Please try again. Error: {str(e)}"
            
            # Add agent response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
    
    # Chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="agent-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("💬 Ask me anything about Aryma Labs...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get agent response
        with st.spinner("🤖 AI Agent is thinking..."):
            try:
                if len(st.session_state.messages) == 1:
                    response = st.session_state.agent.process_user_response(user_input)
                else:
                    response = st.session_state.agent.handle_follow_up(user_input)
            except Exception as e:
                response = f"I apologize, but I'm having trouble processing your request. Please try again. Error: {str(e)}"
        
        # Add agent response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; margin-top: 2rem;">
        <p>🤖 Powered by Aryma Labs AI | Built with Streamlit</p>
        <p>© 2024 Aryma Labs. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
