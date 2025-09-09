import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="Aryma Labs AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Aryma Labs AI Agent")
st.write("Welcome to the AI Agent for Aryma Labs!")

# Test environment
st.subheader("Environment Check")
st.write(f"Python version: {os.sys.version}")

# Test basic functionality
try:
    from ai_agent import ArymalabsAgent
    from config import WEBSITE_URL, DEMO_URL, CATEGORIES
    
    st.success("✅ All imports successful!")
    
    # Initialize agent
    agent = ArymalabsAgent()
    
    # Simple chat interface
    st.subheader("Chat with AI Agent")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add initial message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm the Aryma Labs AI Agent. Are you looking for MMM Services, MMM Products, or Experimentation Products?"
        })
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get agent response
        with st.spinner("AI Agent is thinking..."):
            try:
                if len(st.session_state.messages) == 2:  # First user response
                    response = agent.process_user_response(user_input)
                else:
                    response = agent.handle_follow_up(user_input)
            except Exception as e:
                response = f"I apologize, but I encountered an error: {str(e)}"
        
        # Add agent response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
        
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
