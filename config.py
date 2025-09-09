import os
from dotenv import load_dotenv

load_dotenv()

# API configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Free Hugging Face API

# Website configuration
WEBSITE_URL = "https://www.arymalabs.com"
DEMO_URL = "https://www.arymalabs.com/#contact"  # Contact section for demo requests

# Content categories
CATEGORIES = {
    "MMM_SERVICES": "MMM Services",
    "MMM_PRODUCTS": "MMM Products", 
    "EXPERIMENTATION_PRODUCTS": "Experimentation Products"
}
