#!/bin/bash

# Commit the new pre-installation check feature

echo "Committing pre-installation security check feature..."

git add pre-install-check.py
git add example-malicious-weather-skill.md
git add example-docker-skill.md
git add demo-pre-install.sh
git add README.md

git commit -m "feat: Add pre-installation security check

- New tool to check skills BEFORE installing them
- Detects credential theft attempts (webhook.site patterns)
- Identifies dangerous Docker configurations
- Includes examples of real malicious patterns
- Docker security verification built-in
- Demo script shows both attack vectors

This addresses the core problem: checking skills before they can steal credentials."

echo "✅ Changes committed"
echo ""
echo "Ready to push to GitHub!"