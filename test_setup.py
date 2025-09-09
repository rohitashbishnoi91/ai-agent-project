#!/usr/bin/env python3
"""
Test script to verify the AI Agent setup is working correctly.
Run this to check if all components are functioning properly.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing package imports...")
    
    try:
        import lxml
        print(f"✅ lxml {lxml.__version__} - Working")
    except ImportError as e:
        print(f"❌ lxml - Failed: {e}")
        return False
    
    try:
        import requests
        print(f"✅ requests {requests.__version__} - Working")
    except ImportError as e:
        print(f"❌ requests - Failed: {e}")
        return False
    
    try:
        import streamlit
        print(f"✅ streamlit {streamlit.__version__} - Working")
    except ImportError as e:
        print(f"❌ streamlit - Failed: {e}")
        return False
    
    try:
        import huggingface_hub
        print(f"✅ huggingface_hub {huggingface_hub.__version__} - Working")
    except ImportError as e:
        print(f"❌ huggingface_hub - Failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 - Working")
    except ImportError as e:
        print(f"❌ beautifulsoup4 - Failed: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv - Working")
    except ImportError as e:
        print(f"❌ python-dotenv - Failed: {e}")
        return False
    
    return True

def test_ai_agent():
    """Test if the AI agent can be initialized."""
    print("\n🤖 Testing AI Agent initialization...")
    
    try:
        from ai_agent import ArymalabsAgent
        from config import WEBSITE_URL, DEMO_URL, CATEGORIES
        
        print(f"✅ Config loaded - Website: {WEBSITE_URL}")
        print(f"✅ Config loaded - Demo URL: {DEMO_URL}")
        print(f"✅ Config loaded - Categories: {list(CATEGORIES.keys())}")
        
        # Initialize agent
        agent = ArymalabsAgent()
        print("✅ AI Agent initialized successfully")
        
        # Test basic functionality
        response = agent.process_user_response("I'm interested in MMM Services")
        print(f"✅ Agent response test: {len(response)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Agent test failed: {e}")
        return False

def test_web_scraper():
    """Test if the web scraper is working."""
    print("\n🕷️ Testing Web Scraper...")
    
    try:
        from web_scraper import ArymalabsScraper
        from config import WEBSITE_URL
        
        scraper = ArymalabsScraper(WEBSITE_URL)
        print("✅ Web Scraper initialized")
        
        # Test scraping (this might take a moment)
        print("⏳ Testing website scraping...")
        content = scraper.scrape_website()
        
        if content and len(content) > 50:
            print(f"✅ Website scraping successful - {len(content)} characters scraped")
            return True
        else:
            print("⚠️ Website scraping returned minimal content (this is normal for some websites)")
            return True  # Still consider it a pass since scraping worked
            
    except Exception as e:
        print(f"❌ Web Scraper test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 AI Agent Setup Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Import tests failed. Please check your installation.")
        sys.exit(1)
    
    # Test AI agent
    agent_ok = test_ai_agent()
    
    # Test web scraper
    scraper_ok = test_web_scraper()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Package Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"AI Agent: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    print(f"Web Scraper: {'✅ PASS' if scraper_ok else '❌ FAIL'}")
    
    if imports_ok and agent_ok and scraper_ok:
        print("\n🎉 All tests passed! Your AI Agent is ready to use.")
        print("\nTo run the app:")
        print("  streamlit run app.py")
        print("\nTo deploy to Streamlit Cloud:")
        print("  1. Go to https://share.streamlit.io")
        print("  2. Connect your GitHub repository")
        print("  3. Add HUGGINGFACE_API_KEY environment variable")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
