import streamlit as st

st.title("🚀 AI Agent Test")
st.write("If you can see this, the basic deployment is working!")

# Test basic imports
try:
    import requests
    st.success("✅ requests imported successfully")
except Exception as e:
    st.error(f"❌ requests import failed: {e}")

try:
    from bs4 import BeautifulSoup
    st.success("✅ beautifulsoup4 imported successfully")
except Exception as e:
    st.error(f"❌ beautifulsoup4 import failed: {e}")

try:
    import lxml
    st.success("✅ lxml imported successfully")
except Exception as e:
    st.error(f"❌ lxml import failed: {e}")

try:
    import huggingface_hub
    st.success("✅ huggingface_hub imported successfully")
except Exception as e:
    st.error(f"❌ huggingface_hub import failed: {e}")

try:
    from dotenv import load_dotenv
    st.success("✅ python-dotenv imported successfully")
except Exception as e:
    st.error(f"❌ python-dotenv import failed: {e}")

# Test AI agent
try:
    from ai_agent import ArymalabsAgent
    st.success("✅ AI Agent imported successfully")
    
    # Test basic functionality
    agent = ArymalabsAgent()
    response = agent.process_user_response("I'm interested in MMM Services")
    st.success(f"✅ AI Agent working! Response length: {len(response)} characters")
    st.write("**Sample Response:**")
    st.write(response[:200] + "...")
    
except Exception as e:
    st.error(f"❌ AI Agent failed: {e}")
    import traceback
    st.code(traceback.format_exc())

st.write("---")
st.write("**Deployment Test Complete!**")
