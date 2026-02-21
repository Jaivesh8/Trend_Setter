# Manual Git Steps to Push to GitHub

## Repository: https://github.com/Jaivesh8/Trend_Setter
## Branch: backend
## Directory: app (if it exists)

### Option 1: Use the Automated Script (Recommended)

```bash
cd /Users/charanjotsingh/Downloads/transcript
./setup_git.sh
```

### Option 2: Manual Steps

#### Step 1: Initialize Git

```bash
cd /Users/charanjotsingh/Downloads/transcript
git init
```

#### Step 2: Add Remote Repository

```bash
git remote add origin https://github.com/Jaivesh8/Trend_Setter.git
```

#### Step 3: Fetch and Checkout Backend Branch

```bash
# Fetch all branches
git fetch origin

# Checkout backend branch (create if it doesn't exist)
git checkout -b backend origin/backend 2>/dev/null || git checkout -b backend
```

#### Step 4: Check if App Directory Exists

```bash
# Check what's in the remote backend branch
git ls-tree -r --name-only origin/backend | head -20
```

**If `app/` directory exists:**

```bash
# Create app directory
mkdir -p app

# Copy files to app directory
cp *.py app/
cp *.txt app/
cp *.md app/
cp .gitignore app/

# Stage app directory
git add app/
```

**If `app/` directory doesn't exist:**

```bash
# Add files to root
git add *.py *.txt *.md .gitignore
```

#### Step 5: Commit

```bash
git commit -m "Add transcript search and mapping API backend"
```

#### Step 6: Push

```bash
git push origin backend
```

### Step 7: Verify

Visit: https://github.com/Jaivesh8/Trend_Setter/tree/backend

## Important Notes

1. **Large Files**: The `.pkl` files are large (5-6 MB each). They're excluded in `.gitignore`. If you need them in the repo:
   - Use Git LFS: `git lfs track "*.pkl"`
   - Or commit them separately

2. **ChromaDB**: The `chroma_db/` directory is excluded. Make sure to have it on your server.

3. **Authentication**: You may need to authenticate:
   ```bash
   # Using HTTPS (will prompt for credentials)
   git push origin backend
   
   # Or use SSH (if you have SSH keys set up)
   git remote set-url origin git@github.com:Jaivesh8/Trend_Setter.git
   ```

4. **First Time Push**: If backend branch doesn't exist:
   ```bash
   git push -u origin backend
   ```

## Troubleshooting

### Authentication Error
```bash
# Use personal access token instead of password
git push origin backend
# Username: your_username
# Password: your_personal_access_token
```

### Branch Already Exists
```bash
# Pull first, then push
git pull origin backend
git push origin backend
```

### Merge Conflicts
```bash
# Pull and resolve conflicts
git pull origin backend
# Fix conflicts, then:
git add .
git commit -m "Resolve conflicts"
git push origin backend
```
