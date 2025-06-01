#!/bin/bash
# Gemini Engineer Run Script

set -e  # Exit on any error

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./install.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists and has API key
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./install.sh first"
    exit 1
fi

# Check if API key is set
if grep -q "your_api_key_here" .env; then
    echo "❌ Please set your Gemini API key in .env file"
    echo "   Get your API key from: https://aistudio.google.com/app/apikey"
    exit 1
fi

echo "🚀 Starting Gemini Engineer..."
python main.py 