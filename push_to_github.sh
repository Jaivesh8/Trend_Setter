#!/bin/bash

# Script to push transcript search API to GitHub
# Repository: https://github.com/Jaivesh8/Trend_Setter
# Branch: backend

set -e  # Exit on error

echo "🚀 Setting up Git repository..."
echo ""

cd /Users/charanjotsingh/Downloads/transcript

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Add remote repository
echo "🔗 Adding remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Jaivesh8/Trend_Setter.git

# Fetch existing branches
echo "📥 Fetching branches..."
git fetch origin || echo "⚠️  Could not fetch. Continuing..."

# Checkout backend branch
echo "🌿 Switching to backend branch..."
if git show-ref --verify --quiet refs/remotes/origin/backend; then
    git checkout -b backend origin/backend 2>/dev/null || git checkout backend
else
    git checkout -b backend 2>/dev/null || git checkout backend
fi

# Stage files
echo "📝 Staging files..."
git add *.py *.txt *.md .gitignore 2>/dev/null || true

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit."
else
    echo "💾 Committing changes..."
    git commit -m "Add transcript search and mapping API backend

- FastAPI backend with search endpoints
- ChromaDB integration for transcript embeddings
- PKL file mapping for text and image embeddings
- REST API for Kotlin frontend integration"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
echo ""
read -p "Push to origin/backend? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin backend
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "📍 Repository: https://github.com/Jaivesh8/Trend_Setter/tree/backend"
else
    echo "❌ Push cancelled."
fi
