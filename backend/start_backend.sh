#!/bin/bash
# ViMax Backend Startup Script

cd /app/backend

# Set Python path to include backend directory
export PYTHONPATH="/app/backend:/app:${PYTHONPATH}"

# Run the FastAPI server
echo "Starting ViMax Backend Server..."
exec uvicorn server:app --host 0.0.0.0 --port 8001 --reload
