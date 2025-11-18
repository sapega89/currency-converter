# GitHub Repository Setup Instructions

## Step 1: Create Repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `currency-converter` (or any name you prefer)
   - **Description**: "Currency converter application following SOLID principles"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see instructions. Run these commands in your terminal:

```bash
# Navigate to your project directory
cd c:\Users\user\PycharmProjects\PythonProject1\convertert

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/currency-converter.git

# Or if you prefer SSH (if you have SSH keys set up):
# git remote add origin git@github.com:YOUR_USERNAME/currency-converter.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
gh repo create currency-converter --public --source=. --remote=origin --push
```

## Step 3: Verify

1. Go to your repository on GitHub
2. You should see all your files including README.md
3. The README will be automatically displayed on the repository page

## Useful Git Commands

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log
```

## Repository URL Format

- HTTPS: `https://github.com/YOUR_USERNAME/currency-converter.git`
- SSH: `git@github.com:YOUR_USERNAME/currency-converter.git`

Replace `YOUR_USERNAME` with your actual GitHub username.

