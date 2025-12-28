# .gitignore Guide for CV-lize

This document explains what's included in the `.gitignore` file and why.

## ✅ What's Already Ignored

### **Python & Backend**

#### Virtual Environments
```
venv/
env/
ENV/
.venv
```
**Why**: Virtual environments contain thousands of files and should be recreated locally using `requirements.txt`.

#### Python Cache Files
```
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
```
**Why**: These are compiled Python files that are automatically regenerated. Committing them causes conflicts.

#### Build Artifacts
```
build/
dist/
*.egg
wheels/
```
**Why**: These are generated during package building and deployment.

### **Sensitive Files**

#### Environment Variables
```
.env
.env.local
.env.*.local
backend/.env
```
**Why**: Contains API keys, database credentials, and secrets. **NEVER commit these!**

**What should be in `.env`:**
```env
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/db
OPENROUTER_API_KEY=sk-or-v1-xxxxx
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### **Application Files**

#### User Uploads & Quarantine
```
uploads/
quarantine/
backend/uploads/
backend/quarantine/
```
**Why**: User-uploaded CVs contain private data and shouldn't be in version control.

#### Log Files
```
*.log
backend/*.log
backend/backend.log
```
**Why**: Logs are generated at runtime and can contain sensitive information.

#### Generated PDFs
```
*.pdf
!test-resume.pdf
```
**Why**: Generated PDFs are outputs, not source code. The `!` allows keeping `test-resume.pdf` for testing.

#### spaCy Models
```
backend/en_core_web_*/
```
**Why**: Large ML models (100MB+) should be downloaded separately via `python -m spacy download en_core_web_sm`.

### **Development Tools**

#### IDE Files
```
.vscode/
.idea/
*.swp
*.swo
*~
```
**Why**: Editor configurations are personal preferences and differ between developers.

#### OS Files
```
.DS_Store
Thumbs.db
```
**Why**: Operating system metadata files that clutter the repository.

#### Testing
```
.pytest_cache/
.coverage
htmlcov/
.tox/
*.cover
.hypothesis/
```
**Why**: Test results and coverage reports are generated locally.

#### Jupyter Notebooks
```
.ipynb_checkpoints
*.ipynb
```
**Why**: Jupyter checkpoints and notebooks used for development/testing.

#### Python Version
```
.python-version
```
**Why**: pyenv version file - developers may use different Python versions locally.

### **Database**

```
*.db
*.sqlite3
*.db-journal
*.db-wal
```
**Why**: Database files contain user data and grow large. Use MongoDB Atlas instead.

### **Background Tasks**

```
celerybeat-schedule
celerybeat.pid
```
**Why**: Celery scheduler files (if you add background tasks in the future).

### **Frontend**

```
frontend/node_modules/
frontend/dist/
frontend/.next/
frontend/build/
```
**Why**: 
- `node_modules/`: Installed via `npm install`
- `dist/`, `build/`: Generated via `npm run build`
- `.next/`: Next.js cache (if you migrate to Next.js)

---

## 🚫 What Should NEVER Be Committed

### **Absolutely Never Commit:**

1. **`.env` files** - Contains secrets
2. **API keys** - In any form
3. **Database credentials** - Passwords, connection strings
4. **Private keys** - SSL certificates, SSH keys
5. **User data** - Uploaded CVs, personal information
6. **Binary files** - PDFs, large models
7. **node_modules/** - 100,000+ files
8. **venv/** - Virtual environment

### **Check Before Committing:**

```bash
# Review what will be committed
git status

# Review actual changes
git diff

# Check for sensitive data
git diff | grep -i "password\|secret\|key\|token"
```

---

## ✅ What SHOULD Be Committed

### **Essential Files:**

1. **Source code** - `.py`, `.tsx`, `.ts`, `.html`, `.css`
2. **Configuration** - `requirements.txt`, `package.json`, `tsconfig.json`
3. **Documentation** - `README.md`, `DEPLOYMENT.md`, `*.md`
4. **Templates** - HTML templates for PDFs
5. **Example files** - `.env.example` (without real values)
6. **Docker files** - `Dockerfile`, `docker-compose.yml`
7. **CI/CD configs** - `.github/workflows/*.yml`, `vercel.json`
8. **Tests** - `test_*.py`, `*.test.ts`

---

## 📝 Creating `.env.example`

Always create a template for other developers:

```bash
# Create example file
cp backend/.env backend/.env.example

# Remove all actual values
# Edit .env.example to look like:
```

**backend/.env.example:**
```env
# MongoDB Atlas Connection String
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database

# OpenRouter API Key for AI Analysis
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Allowed CORS Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend-url.vercel.app

# Environment
ENVIRONMENT=development
DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Upload Directories
UPLOAD_DIR=./uploads
QUARANTINE_DIR=./quarantine
```

**Commit this example file:**
```bash
git add backend/.env.example
git commit -m "Add environment variables example file"
```

---

## 🔍 Checking for Leaked Secrets

### **Before First Commit:**

```bash
# Check if .env is ignored
git check-ignore backend/.env
# Should output: backend/.env

# Check what's being tracked
git ls-files | grep -i "env\|secret\|key"
# Should NOT show .env files
```

### **If You Accidentally Committed Secrets:**

```bash
# Remove from Git history (DANGEROUS - coordinate with team)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (recommended)
bfg --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (WARNING: rewrites history)
git push origin --force --all

# IMPORTANT: Rotate all exposed secrets immediately!
# - Change MongoDB password
# - Regenerate API keys
# - Update all deployed environments
```

---

## 📦 Clean Repository Checklist

Before pushing to GitHub:

- [ ] `.env` files are not tracked
- [ ] No API keys in code
- [ ] No passwords in comments
- [ ] `uploads/` and `quarantine/` are empty and ignored
- [ ] No `*.pdf` files (except test files)
- [ ] No `node_modules/` or `venv/`
- [ ] No `*.log` files
- [ ] No database files
- [ ] `.gitignore` is comprehensive
- [ ] `.env.example` exists with dummy values

---

## 🚀 Commands Reference

```bash
# Check gitignore status
git status --ignored

# Remove files already tracked
git rm -r --cached uploads/
git rm --cached backend/.env

# Commit gitignore changes
git add .gitignore
git commit -m "Update .gitignore for backend files"

# Verify nothing sensitive is tracked
git ls-files | grep -E "\.env$|uploads/|quarantine/|\.log$"
# Should return nothing

# Check repository size
git count-objects -vH
```

---

## 🔐 Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use `.env.example`** - Provide templates for developers
3. **Rotate keys regularly** - Especially after team changes
4. **Use different keys** - Dev, staging, and production
5. **Enable secret scanning** - GitHub has built-in secret scanning
6. **Review PRs carefully** - Check for accidental secret commits
7. **Use git hooks** - Prevent commits with secrets

### **Pre-commit Hook Example:**

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash

# Check for .env files
if git diff --cached --name-only | grep -E "\.env$"; then
    echo "Error: .env file detected! Remove it before committing."
    exit 1
fi

# Check for common secrets
if git diff --cached | grep -iE "api[_-]?key|password|secret|token"; then
    echo "Warning: Potential secret detected! Review your changes."
    read -p "Continue anyway? (y/N): " confirm
    if [ "$confirm" != "y" ]; then
        exit 1
    fi
fi

exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

Your repository is now properly configured to avoid committing sensitive or unnecessary files! 🎉
