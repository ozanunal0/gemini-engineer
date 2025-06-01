#!/bin/bash
# Gemini Engineer Installation Script

set -e  # Exit on any error

echo "🤖 Setting up Gemini Engineer..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
required_version="3.11"

if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]]; then
    echo "✅ Python version $python_version is compatible"
else
    echo "❌ Python 3.11+ is required, but you have $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "📝 Copied env.example to .env"
        echo "📝 Please edit .env and add your Gemini API key"
    else
        echo "GEMINI_API_KEY=your_api_key_here" > .env
        echo "📝 Created .env file - please add your Gemini API key"
    fi
    echo "   Get your API key from: https://aistudio.google.com/app/apikey"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To get started:"
echo "1. Edit .env and add your Gemini API key"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python main.py"
echo ""
echo "Or simply run: ./run.sh" 