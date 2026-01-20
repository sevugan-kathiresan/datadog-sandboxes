#!/usr/bin/env sh
set -e

echo "Initializing database..."
uv run python agri_api/init_db.py

echo "Starting FastAPI..."
exec uv run ddtrace-run uvicorn agri_api.main:app --host 0.0.0.0 --port 8000