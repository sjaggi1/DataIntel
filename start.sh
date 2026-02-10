#!/bin/bash

echo "=================================="
echo "Enterprise Data Intelligence Platform"
echo "=================================="
echo ""
echo "Starting application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade requirements
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "=================================="
echo "Application starting on http://localhost:8501"
echo "=================================="
echo ""

# Start Streamlit
streamlit run app.py
