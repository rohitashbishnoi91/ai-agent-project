#!/bin/bash

# AI Agent Installation Script for macOS
echo "🚀 Setting up AI Agent for Aryma Labs..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
brew install libxml2 libxslt

# Set environment variables for compilation
export LDFLAGS="-L/opt/homebrew/opt/libxml2/lib -L/opt/homebrew/opt/libxslt/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libxml2/include -I/opt/homebrew/opt/libxslt/include"

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel

# Try to install lxml with pre-compiled wheels first
echo "🔧 Installing lxml (trying pre-compiled wheels first)..."
pip install --only-binary=all lxml || {
    echo "⚠️  Pre-compiled wheels failed, trying with system libraries..."
    pip install lxml
}

# Install remaining dependencies
echo "📦 Installing remaining dependencies..."
pip install -r requirements.txt

echo "✅ Installation complete!"
echo ""
echo "To run the app:"
echo "1. source venv/bin/activate"
echo "2. streamlit run app.py"
echo ""
echo "To deploy to Streamlit Cloud:"
echo "1. Go to https://share.streamlit.io"
echo "2. Connect your GitHub repository"
echo "3. Add HUGGINGFACE_API_KEY environment variable"
