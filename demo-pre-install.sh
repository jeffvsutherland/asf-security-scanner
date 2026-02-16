#!/bin/bash

# Demo: Pre-Installation Security Checks

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         🔍 DEMO: Pre-Installation Security Check 🔍           ║"
echo "║     Checking Skills BEFORE Installing - Two Examples          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# First check Docker security
echo "Step 1: Checking your Docker security configuration..."
echo "=========================================="
python3 pre-install-check.py --docker-check
echo ""

# Example 1: The malicious weather skill
echo "Step 2: Checking the 'weather' skill that caused 4000+ comments..."
echo "=========================================="
echo "Checking: example-malicious-weather-skill.md"
echo ""
python3 pre-install-check.py example-malicious-weather-skill.md
echo ""
echo "Press Enter to continue..."
read

# Example 2: Docker skill with security issues
echo ""
echo "Step 3: Checking a Docker management skill..."
echo "=========================================="
echo "Checking: example-docker-skill.md"
echo ""
python3 pre-install-check.py example-docker-skill.md
echo ""

# Summary
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                     📊 SUMMARY 📊                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "The scanner detected:"
echo "1. ❌ Weather skill: CRITICAL risk - credential stealer using webhook.site"
echo "2. ⚠️  Docker skill: HIGH risk - requests privileged access + mounts filesystem"
echo ""
echo "This is why checking BEFORE installation is critical!"
echo ""
echo "To check any skill before installing:"
echo "  python3 pre-install-check.py <skill-url-or-file>"