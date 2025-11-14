#!/bin/bash
# Startup script for Obsidian AI Assistant API Server

echo "🚀 Starting Obsidian AI Assistant API Server..."
echo ""

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python version
python_version=$(python3 --version 2>&1)
echo "✓ Python: $python_version"

# Check if we're in the right directory
if [ ! -f "api_server.py" ]; then
    echo "❌ Error: api_server.py not found in $SCRIPT_DIR"
    exit 1
fi

# Check environment variables
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "⚠️  Warning: DASHSCOPE_API_KEY not set"
    echo "   Set it in .env file or export DASHSCOPE_API_KEY=your-key"
fi

if [ -z "$TAVILY_API_KEY" ]; then
    echo "⚠️  Warning: TAVILY_API_KEY not set (web search disabled)"
    echo "   Set it in .env file or export TAVILY_API_KEY=your-key"
fi

# Install dependencies if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing API server dependencies..."
    pip install -r requirements-api.txt
fi

echo ""
echo "🌐 Starting server at http://localhost:8000"
echo "📖 API documentation at http://localhost:8000/docs"
echo "❤️  Health check at http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "─────────────────────────────────────────────────────"
echo ""

# Start the server
python3 api_server.py
