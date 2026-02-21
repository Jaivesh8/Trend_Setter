# GitHub Setup Guide

## Push to GitHub Repository

### Step 1: Initialize Git (if not already done)

```bash
cd /Users/charanjotsingh/Downloads/transcript
git init
```

### Step 2: Add Remote Repository

```bash
git remote add origin https://github.com/Jaivesh8/Trend_Setter.git
```

### Step 3: Check Current Branch

```bash
git branch
```

### Step 4: Switch to Backend Branch

```bash
# Fetch all branches
git fetch origin

# Checkout backend branch (or create it if it doesn't exist)
git checkout -b backend origin/backend 2>/dev/null || git checkout -b backend
```

### Step 5: Stage Files

```bash
# Add all files
git add .

# Or add specific files
git add *.py *.txt *.md .gitignore
```

### Step 6: Commit

```bash
git commit -m "Add transcript search API backend"
```

### Step 7: Push to Backend Branch

```bash
git push origin backend
```

## If App Directory Already Exists

If the `app` directory already exists in the backend branch:

```bash
# Create app directory structure
mkdir -p app

# Move files to app directory (or copy)
# Option 1: Move everything
mv *.py app/ 2>/dev/null || true
mv *.txt app/ 2>/dev/null || true
mv *.md app/ 2>/dev/null || true

# Option 2: Or keep structure and push to app subdirectory
git add app/
git commit -m "Add transcript search API to app directory"
git push origin backend
```

## Complete Setup Script

```bash
#!/bin/bash
cd /Users/charanjotsingh/Downloads/transcript

# Initialize git if needed
if [ ! -d .git ]; then
    git init
fi

# Add remote
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Jaivesh8/Trend_Setter.git

# Fetch branches
git fetch origin

# Switch to backend branch
git checkout -b backend origin/backend 2>/dev/null || git checkout -b backend

# Add files
git add *.py *.txt *.md .gitignore

# Commit
git commit -m "Add transcript search and mapping API backend"

# Push
git push origin backend
```
