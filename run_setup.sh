#!/bin/bash
# Quick setup script for Scope 3 Tracker

echo "🚀 Scope 3 Tracker - Setup Script"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🗄️  Creating database migrations..."
python manage.py makemigrations

echo ""
echo "📊 Running migrations..."
python manage.py migrate

echo ""
echo "👤 Creating superuser (admin account)..."
echo "   (You'll be prompted for username, email, and password)"
python manage.py createsuperuser

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 Starting development server..."
echo "   Open http://127.0.0.1:8000/admin/ in your browser"
echo ""
python manage.py runserver

