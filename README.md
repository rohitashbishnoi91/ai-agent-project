# Aryma Labs AI Agent

An intelligent AI agent that helps users discover Aryma Labs' services and products through natural conversation.

## Features

- 🤖 **Intelligent Conversation**: Uses free Hugging Face API for contextual responses
- 🌐 **Web Scraping**: Automatically scrapes the Aryma Labs website for up-to-date content
- 📊 **Content Categorization**: Automatically categorizes content into MMM Services, MMM Products, and Experimentation Products
- 💬 **Interactive UI**: Clean, modern Streamlit interface for easy interaction
- 🔗 **Demo Integration**: Automatically appends "Contact Us for Demo" links to responses

## Project Structure

```
ai-agent-project/
├── app.py                 # Main Streamlit application
├── ai_agent.py           # AI agent logic and conversation handling
├── web_scraper.py        # Website scraping functionality
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── scraped_content.json  # Scraped website content (generated)
└── README.md            # This file
```

## Setup Instructions

### Quick Setup (macOS)

```bash
# Clone the repository
git clone https://github.com/rohitashbishnoi91/ai-agent-project.git
cd ai-agent-project

# Run the installation script
./install.sh
```

### Manual Setup

#### 1. Install System Dependencies (macOS)

```bash
brew install libxml2 libxslt
```

#### 2. Set Environment Variables

```bash
export LDFLAGS="-L/opt/homebrew/opt/libxml2/lib -L/opt/homebrew/opt/libxslt/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libxml2/include -I/opt/homebrew/opt/libxslt/include"
```

#### 3. Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set up Free API Key (Optional)

The agent works perfectly without any API keys! But for enhanced AI responses, you can add:

**Free Hugging Face API:**
```bash
echo "HUGGINGFACE_API_KEY=your_huggingface_token_here" > .env
```
Get your free token at: https://huggingface.co/settings/tokens

**Note:** Hugging Face API access may vary. If you encounter errors, the agent will automatically use the intelligent fallback system.

**Note:** Without API key, the agent uses intelligent fallback responses from scraped content.

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## How It Works

### 1. Website Scraping
- The agent first scrapes the Aryma Labs website to gather current content
- It categorizes content based on keywords related to MMM Services, MMM Products, and Experimentation Products
- Scraped data is saved to `scraped_content.json` for future use

### 2. User Interaction
- New users are greeted with: "Are you looking for MMM Services, MMM Products, or Experimentation Products?"
- The agent categorizes the user's interest based on their response
- Follow-up questions are answered using relevant content from the scraped data

### 3. AI-Powered Responses
- **Free API**: Uses Hugging Face's free API with 1000 requests/month
- **Fallback**: Intelligent keyword-based responses from scraped content
- Ensures responses are relevant to the user's selected category

### 4. Demo Integration
- Every response includes a "Contact Us for Demo" hyperlink
- Links point to the Aryma Labs contact section

## Usage Examples

### Initial Interaction
```
User: "I'm interested in MMM Services"
Agent: "Great! Based on our MMM Services, here's what we offer: [relevant content]... [Contact Us for Demo]"
```

### Follow-up Questions
```
User: "What specific services do you offer?"
Agent: "Our MMM Services include [detailed service information]... [Contact Us for Demo]"
```

## Technical Details

### Web Scraping
- Uses `requests` and `BeautifulSoup` for robust web scraping
- Implements respectful scraping with delays between requests
- Handles various HTML structures and content types

### AI Integration
- Uses OpenAI's Chat Completions API
- Implements fallback responses for reliability
- Context-aware prompting for better responses

### UI/UX
- Built with Streamlit for rapid development
- Responsive design with custom CSS
- Real-time conversation display
- Sidebar with additional information and controls

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Check that you have sufficient API credits

2. **Scraping Issues**
   - The website might be temporarily unavailable
   - Check your internet connection
   - Some content might be dynamically loaded

3. **Content Not Found**
   - The scraper might not have found relevant content
   - Try running the scraper again
   - Check the scraped_content.json file

## License

This project is open source and available under the MIT License.