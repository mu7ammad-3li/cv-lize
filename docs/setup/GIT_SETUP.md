# 🚀 Git Setup Guide - Pushing CV-lize to GitHub

This guide will walk you through connecting your local CV-lize project to GitHub.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] GitHub account created
- [ ] Git installed on your machine (`git --version`)
- [ ] SSH key configured with GitHub (or use HTTPS)
- [ ] Repository created on GitHub: `cv-lize`

---

## 🔐 Step 1: Configure Git (First Time Setup)

If you haven't configured Git before:

```bash
# Set your name (will appear in commits)
git config --global user.name "Muhammad Ali"

# Set your email (should match your GitHub email)
git config --global user.email "muhammad.3lii2@gmail.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Verify configuration
git config --list
```

---

## 🔑 Step 2: Set Up SSH Key (Recommended)

### Option A: Using SSH (Recommended - More Secure)

**Check if you already have an SSH key:**
```bash
ls -la ~/.ssh/
# Look for: id_rsa.pub or id_ed25519.pub
```

**If no SSH key exists, create one:**
```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "muhammad.3lii2@gmail.com"

# Press Enter to accept default location
# Optionally set a passphrase (or press Enter for none)

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add your SSH key
ssh-add ~/.ssh/id_ed25519
```

**Copy your public key:**
```bash
cat ~/.ssh/id_ed25519.pub
# Copy the entire output
```

**Add to GitHub:**
1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Give it a title (e.g., "My Laptop")
5. Click "Add SSH key"

**Test SSH connection:**
```bash
ssh -T git@github.com
# Should see: "Hi mu7ammad-3li! You've successfully authenticated..."
```

### Option B: Using HTTPS (Simpler but less secure)

You'll be prompted for username and password (or personal access token) when pushing.

---

## 📦 Step 3: Initialize Git Repository

```bash
# Navigate to your project directory
cd /media/muhammad/Work/Identity/cv-wizzard

# Initialize git repository
git init

# Verify initialization
git status
```

You should see:
```
On branch main

No commits yet

Untracked files:
  ...
```

---

## 🔗 Step 4: Connect to GitHub Remote

### Using SSH (if you set up SSH key):
```bash
git remote add origin git@github.com:mu7ammad-3li/cv-lize.git
```

### Using HTTPS (if you prefer HTTPS):
```bash
git remote add origin https://github.com/mu7ammad-3li/cv-lize.git
```

**Verify remote:**
```bash
git remote -v
```

Should show:
```
origin  git@github.com:mu7ammad-3li/cv-lize.git (fetch)
origin  git@github.com:mu7ammad-3li/cv-lize.git (push)
```

---

## 🧹 Step 5: Clean Up Before First Commit

**Important**: Remove sensitive files and test files:

```bash
# Remove any generated PDFs (except test file)
find . -name "*.pdf" ! -name "test-resume.pdf" -type f -delete

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

# Remove log files
rm -f backend/*.log
rm -f backend/backend.log

# Remove uploads and quarantine (keep directories)
rm -rf backend/uploads/*
rm -rf backend/quarantine/*

# Keep the directories but add .gitkeep
touch backend/uploads/.gitkeep
touch backend/quarantine/.gitkeep

# Remove node_modules if exists
rm -rf frontend/node_modules/

# Remove build artifacts
rm -rf frontend/dist/
rm -rf frontend/build/
```

**Verify .env files are NOT tracked:**
```bash
# These should NOT appear in git status
ls -la backend/.env
ls -la frontend/.env

# Make sure they're in .gitignore
grep -E "^\.env$" .gitignore
```

---

## 📁 Step 6: Stage Files for Commit

**Add all files:**
```bash
git add .
```

**Check what will be committed:**
```bash
git status
```

**Verify no sensitive files are staged:**
```bash
# Check for .env files
git status | grep -i ".env"
# Should return nothing (or only .env.example)

# Check for large files
git ls-files | xargs ls -lh | awk '$5 ~ /M$/ {print $5, $9}'
# Should not show files > 50MB
```

**If you see .env files, remove them:**
```bash
git reset backend/.env
git reset frontend/.env
```

---

## 💾 Step 7: Create First Commit

```bash
git commit -m "feat: initial commit - CV-lize AI-powered resume optimizer

- Add FastAPI backend with MongoDB integration
- Add React frontend with TypeScript and Vite
- Implement AI-powered CV analysis (Gemini & OpenRouter)
- Add multi-layer security validation
- Add professional resume templates
- Add deployment configurations
- Add comprehensive documentation"
```

---

## 🌿 Step 8: Create and Switch to Main Branch

```bash
# Rename current branch to main (if not already)
git branch -M main
```

---

## 🚀 Step 9: Push to GitHub

**First push:**
```bash
git push -u origin main
```

The `-u` flag sets up tracking so future pushes can just use `git push`.

**If you see errors:**

### Error: "remote contains work that you do not have locally"

This means GitHub repository has files (like README.md created on GitHub). Solution:

```bash
# Pull and merge
git pull origin main --allow-unrelated-histories

# Then push
git push -u origin main
```

### Error: "Authentication failed"

If using HTTPS, you need a Personal Access Token (not password):

1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when prompted

Or switch to SSH (recommended).

---

## ✅ Step 10: Verify Push Succeeded

**Check GitHub:**
1. Go to https://github.com/mu7ammad-3li/cv-lize
2. Refresh the page
3. You should see all your files!

**Check from terminal:**
```bash
git log --oneline
git remote show origin
```

---

## 🔄 Future Commits (After Initial Push)

Now that you're connected, making changes is easy:

```bash
# 1. Make your changes to files
# 2. Check what changed
git status
git diff

# 3. Add changed files
git add .
# Or add specific files
git add backend/main.py frontend/src/App.tsx

# 4. Commit with descriptive message
git commit -m "fix: improve ATS scoring algorithm"

# 5. Push to GitHub
git push
```

---

## 📝 Commit Message Convention

Follow conventional commits format:

```bash
# Format: <type>: <description>

# Types:
feat:     # New feature
fix:      # Bug fix
docs:     # Documentation changes
style:    # Code style changes (formatting)
refactor: # Code refactoring
test:     # Adding tests
chore:    # Maintenance tasks

# Examples:
git commit -m "feat: add PDF export functionality"
git commit -m "fix: resolve CORS issue with frontend"
git commit -m "docs: update README with deployment guide"
git commit -m "refactor: optimize AI analysis service"
```

---

## 🌿 Branching Strategy

For feature development:

```bash
# Create new branch
git checkout -b feature/add-cover-letter-generation

# Make changes and commit
git add .
git commit -m "feat: implement cover letter generation"

# Push branch to GitHub
git push -u origin feature/add-cover-letter-generation

# Create Pull Request on GitHub
# After approval, merge to main
```

---

## 🚨 Common Issues & Solutions

### Issue: "Permission denied (publickey)"

**Solution**: SSH key not configured correctly.
```bash
# Test SSH
ssh -T git@github.com

# If fails, reconfigure SSH key (see Step 2)
```

### Issue: ".env file was committed"

**Solution**: Remove from Git history
```bash
# Remove from current commit (before push)
git reset HEAD backend/.env
git commit --amend

# If already pushed (DANGEROUS - rewrites history)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# IMPORTANT: Change all secrets in .env immediately!
```

### Issue: "Repository is too large"

**Solution**: Check for large files
```bash
# Find large files
git ls-files | xargs ls -lh | sort -rh -k5 | head -20

# Remove from git if needed
git rm --cached large-file.pdf
git commit --amend
```

### Issue: "Updates were rejected"

**Solution**: Pull first, then push
```bash
git pull origin main --rebase
git push
```

---

## 📦 Recommended .gitignore (Already Created)

Your `.gitignore` should include:

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
.env

# JavaScript
node_modules/
dist/
.env

# Generated files
*.log
*.pdf
!test-resume.pdf
uploads/
quarantine/

# IDE
.vscode/
.idea/
```

---

## 🔒 Security Checklist Before Pushing

- [ ] `.env` files are NOT committed
- [ ] No API keys in code
- [ ] No passwords in comments  
- [ ] `uploads/` and `quarantine/` are empty
- [ ] No database files committed
- [ ] No large binary files (>50MB)
- [ ] `.gitignore` is comprehensive
- [ ] `.env.example` exists with dummy values

**Verify:**
```bash
# Check what will be pushed
git ls-files | grep -E "\.env$|\.log$|uploads/|quarantine/"
# Should return nothing (or only .gitkeep files)
```

---

## 🎯 Quick Reference

```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# View remote info
git remote -v

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Branching Strategy](https://nvie.com/posts/a-successful-git-branching-model/)

---

## ✨ You're Ready!

Your CV-lize project is now connected to GitHub. Future updates are just a `git push` away! 🚀

Happy coding! 🎉
