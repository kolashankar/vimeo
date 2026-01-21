#!/bin/bash
cd /app
source /app/.venv/bin/activate
exec uvicorn web_interface.server:app --host 0.0.0.0 --port 8001
