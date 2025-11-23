#!/bin/bash
# Startup script for Ai-CareFlow application

echo "🏥 Starting Ai-CareFlow..."
echo ""
echo "⚠️  IMPORTANT: Use synthetic data only"
echo "    This tool is for demonstration purposes"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the Streamlit application
streamlit run app/streamlit_app.py
