#!/usr/bin/env python3
"""
Deployment test script for Streamlit Cloud.
This script tests if all components work in a deployment environment.
"""

def test_deployment():
    """Test all components for deployment compatibility."""
    print("🚀 Testing deployment compatibility...")
    
    try:
        # Test basic imports
        import streamlit as st
        import requests
        import lxml
        from bs4 import BeautifulSoup
        import huggingface_hub
        from dotenv import load_dotenv
        print("✅ All basic imports successful")
        
        # Test app components
        from config import WEBSITE_URL, DEMO_URL, CATEGORIES, HUGGINGFACE_API_KEY
        print("✅ Config loaded successfully")
        
        # Test AI agent
        from ai_agent import ArymalabsAgent
        agent = ArymalabsAgent()
        print("✅ AI Agent initialized")
        
        # Test web scraper
        from web_scraper import ArymalabsScraper
        scraper = ArymalabsScraper(WEBSITE_URL)
        print("✅ Web Scraper initialized")
        
        # Test basic functionality
        response = agent.process_user_response("I'm interested in MMM Services")
        print(f"✅ Agent response generated: {len(response)} characters")
        
        print("\n🎉 All deployment tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Deployment test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_deployment()
