# 🚀 Push to GitHub - Quick Guide

## Target Repository
- **Repository**: https://github.com/Jaivesh8/Trend_Setter
- **Branch**: `backend`
- **Directory**: `app/` (if it exists in the repo)

## ✅ Quick Method (Recommended)

Run the automated script:

```bash
cd /Users/charanjotsingh/Downloads/transcript
./setup_git.sh
```

This script will:
1. ✅ Initialize git (if needed)
2. ✅ Connect to your GitHub repo
3. ✅ Switch to backend branch
4. ✅ Check if `app/` directory exists
5. ✅ Copy files to the right location
6. ✅ Commit and push

## 📋 Manual Method

If you prefer to do it manually:

```bash
cd /Users/charanjotsingh/Downloads/transcript

# 1. Initialize git
git init

# 2. Add remote
git remote add origin https://github.com/Jaivesh8/Trend_Setter.git

# 3. Fetch and checkout backend branch
git fetch origin
git checkout -b backend origin/backend 2>/dev/null || git checkout -b backend

# 4. Check if app directory exists (optional)
# If app/ exists in remote, create it locally:
mkdir -p app
cp *.py app/
cp *.txt app/
cp *.md app/
cp .gitignore app/

# 5. Stage files
git add app/  # if app/ exists
# OR
git add *.py *.txt *.md .gitignore  # if pushing to root

# 6. Commit
git commit -m "Add transcript search API backend"

# 7. Push
git push origin backend
```

## 📁 What Gets Pushed

**Included:**
- ✅ All Python files (`*.py`)
- ✅ Requirements file (`requirements.txt`)
- ✅ Documentation (`*.md`)
- ✅ Git ignore (`.gitignore`)

**Excluded (via .gitignore):**
- ❌ `chroma_db/` directory (database files)
- ❌ `*.pkl` files (large embedding files)
- ❌ `__pycache__/` and other Python cache
- ❌ Virtual environment folders

## 🔐 Authentication

When pushing, GitHub will ask for credentials:

**Option 1: Personal Access Token**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate a token with `repo` permissions
3. Use token as password when prompted

**Option 2: SSH (if configured)**
```bash
git remote set-url origin git@github.com:Jaivesh8/Trend_Setter.git
```

## ✅ Verify After Push

Visit: https://github.com/Jaivesh8/Trend_Setter/tree/backend

Or if app directory exists:
https://github.com/Jaivesh8/Trend_Setter/tree/backend/app

## 🐛 Troubleshooting

**"Repository not found"**
- Check repository name and permissions
- Make sure you have write access

**"Branch does not exist"**
- Use: `git push -u origin backend` (creates branch)

**"Authentication failed"**
- Use Personal Access Token instead of password
- Or set up SSH keys

**"Large file"**
- PKL files are excluded by .gitignore
- If you need them, use Git LFS:
  ```bash
  git lfs track "*.pkl"
  git add .gitattributes
  git add *.pkl
  ```

## 📞 Need Help?

See detailed guides:
- `MANUAL_GIT_STEPS.md` - Step-by-step manual instructions
- `GITHUB_SETUP.md` - Complete setup guide
