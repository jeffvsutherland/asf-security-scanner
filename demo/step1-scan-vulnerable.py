#!/usr/bin/env python3
"""
Step 1: Demonstrate scanning vulnerable skills
Shows oracle and openai-image-gen have security issues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Simulated scanner output for demo
def demo_scan():
    print("🔍 ASF Security Scanner v1.0")
    print("━" * 60)
    print("Scanning skills for security vulnerabilities...\n")
    
    # Simulate scanning
    skills = [
        ("oracle", "DANGER", [
            "References sensitive data",
            "Accesses .env files",
            "Reads OPENAI_API_KEY from environment"
        ]),
        ("openai-image-gen", "DANGER", [
            "scripts/gen.py: Line 176 exposes API keys",
            "os.environ.get('OPENAI_API_KEY')",
            "Any code can steal credentials"
        ])
    ]
    
    print("Scanning: /opt/homebrew/lib/node_modules/clawdbot/skills/\n")
    
    for skill, status, issues in skills:
        if status == "DANGER":
            color = "\033[91m"  # Red
            symbol = "🚨"
        else:
            color = "\033[92m"  # Green
            symbol = "✅"
        
        print(f"{skill:<25} {color}{symbol} {status}\033[0m")
        for issue in issues:
            print(f"{'':>27} • {issue}")
        print()
    
    print("━" * 60)
    print("\n📊 Summary:")
    print("   Vulnerabilities Found: 2")
    print("   Risk Level: HIGH")
    print("\n⚠️  These are the same vulnerabilities that exposed")
    print("   1.5M tokens in the Moltbook breach!")
    
    # Show actual vulnerable code
    print("\n📝 Vulnerable Code Example (openai-image-gen line 176):")
    print("─" * 50)
    print("api_key = (os.environ.get('OPENAI_API_KEY') or '').strip()")
    print("if not api_key:")
    print("    print('Missing OPENAI_API_KEY', file=sys.stderr)")
    print("─" * 50)

if __name__ == "__main__":
    demo_scan()