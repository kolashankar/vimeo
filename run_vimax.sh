#!/bin/bash
# ViMax Quick Start Script

echo "============================================"
echo "🎬 ViMax - Quick Start"
echo "============================================"
echo ""

# Activate virtual environment
source /app/.venv/bin/activate

# Check status
echo "📊 Checking API status..."
python /app/check_status.py

echo ""
echo "============================================"
echo "Choose an option:"
echo "============================================"
echo "1. Run Idea2Video (convert idea to video)"
echo "2. Run Script2Video (convert script to video)"
echo "3. Check API status again"
echo "4. Exit"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Idea2Video..."
        python /app/main_idea2video.py
        ;;
    2)
        echo ""
        echo "🚀 Starting Script2Video..."
        python /app/main_script2video.py
        ;;
    3)
        echo ""
        python /app/check_status.py
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
