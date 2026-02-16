#!/bin/bash

# ASF Security Scanner - GitHub Deployment Script
# This script initializes the git repository and prepares it for GitHub

echo "🔒 ASF Security Scanner - GitHub Deployment"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo ""
echo "Adding files to repository..."
git add .
echo "✅ Files staged"

# Create initial commit
echo ""
echo "Creating initial commit..."
git commit -m "Initial commit: ASF Security Scanner v2.0

- Intelligent context-aware security scanning
- False positive reduction from 38 to 0
- Comprehensive documentation
- Full test suite
- HTML and JSON reporting"
echo "✅ Initial commit created"

# Instructions for GitHub
echo ""
echo "📋 Next Steps:"
echo "============="
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo "   Repository name: asf-security-scanner"
echo ""
echo "2. Add the remote origin:"
echo "   git remote add origin https://github.com/agent-saturday/asf-security-scanner.git"
echo ""
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Optional: Create a release"
echo "   - Go to https://github.com/agent-saturday/asf-security-scanner/releases"
echo "   - Click 'Create a new release'"
echo "   - Tag version: v2.0.0"
echo "   - Release title: ASF Security Scanner v2.0 - Intelligent Security Analysis"
echo ""
echo "5. Optional: Enable GitHub Actions for CI/CD"
echo ""
echo "✅ Repository is ready for GitHub deployment!"