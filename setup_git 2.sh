#!/bin/bash

# Setup and push to GitHub repository
# Repository: https://github.com/Jaivesh8/Trend_Setter
# Branch: backend
# Directory: app (if exists)

cd /Users/charanjotsingh/Downloads/transcript

echo "🚀 Setting up Git for Trend_Setter repository..."
echo ""

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Add remote
echo "🔗 Configuring remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Jaivesh8/Trend_Setter.git

# Fetch branches
echo "📥 Fetching branches from GitHub..."
git fetch origin

# Check if backend branch exists remotely
if git ls-remote --heads origin backend | grep -q backend; then
    echo "✅ Backend branch exists remotely"
    git checkout -b backend origin/backend 2>/dev/null || git checkout backend
    git pull origin backend 2>/dev/null || true
else
    echo "📝 Creating new backend branch..."
    git checkout -b backend 2>/dev/null || git checkout backend
fi

# Check if app directory exists in remote
echo "📁 Checking repository structure..."
if git ls-tree -r --name-only origin/backend 2>/dev/null | grep -q "^app/"; then
    echo "✅ App directory exists in remote repository"
    echo "📂 Files will be pushed to app/ directory"
    
    # Create app directory locally if it doesn't exist
    mkdir -p app
    
    # Copy files to app directory (don't move, keep originals)
    echo "📋 Copying files to app/ directory..."
    cp *.py app/ 2>/dev/null || true
    cp *.txt app/ 2>/dev/null || true
    cp *.md app/ 2>/dev/null || true
    cp .gitignore app/ 2>/dev/null || true
    
    # Stage app directory
    git add app/
else
    echo "📝 No app directory found, pushing to root of backend branch"
    git add *.py *.txt *.md .gitignore 2>/dev/null || true
fi

# Show status
echo ""
echo "📊 Git status:"
git status --short

echo ""
read -p "💾 Commit and push? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Commit
    git commit -m "Add transcript search and mapping API backend

Features:
- FastAPI backend with REST endpoints
- ChromaDB integration for transcript embeddings  
- PKL file mapping for text and image embeddings
- Search and retrieval endpoints
- Kotlin frontend integration ready"

    # Push
    echo "⬆️  Pushing to GitHub..."
    git push origin backend
    
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "📍 View at: https://github.com/Jaivesh8/Trend_Setter/tree/backend"
    if [ -d app ]; then
        echo "📍 App directory: https://github.com/Jaivesh8/Trend_Setter/tree/backend/app"
    fi
else
    echo "❌ Cancelled. Run this script again when ready."
fi
