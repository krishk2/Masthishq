#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Starting Build Process..."

# 1. Install Backend Dependencies
echo "📦 Installing Python Dependencies..."
pip install -r requirements.txt
pip install gunicorn uvicorn

# 2. Build Frontend
echo "⚛️ Building React Frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build Complete!"
