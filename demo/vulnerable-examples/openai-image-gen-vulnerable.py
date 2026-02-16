#!/usr/bin/env python3
"""
OpenAI Image Gen - Vulnerable Version
This shows the actual vulnerable code from line 176
"""

import os
import sys

# ... earlier code ...

def main():
    """Main function with vulnerable credential access"""
    
    # ❌ VULNERABLE CODE - Line 176
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    
    if not api_key:
        print("Missing OPENAI_API_KEY", file=sys.stderr)
        print("Set your OpenAI API key:", file=sys.stderr)
        print("  export OPENAI_API_KEY=sk-...", file=sys.stderr)
        sys.exit(1)
    
    # Problem: Any code can access this environment variable
    # including malicious skills or compromised dependencies
    
    # Use the key for API calls
    headers = {
        "Authorization": f"Bearer {api_key}",  # Key exposed!
        "Content-Type": "application/json"
    }
    
    # ... rest of the code ...

# Attack demonstration:
"""
Any other code running on the system can steal this key:

1. Malicious skill installation:
   - Reads all environment variables
   - Finds OPENAI_API_KEY
   - Sends to attacker's server

2. Compromised dependency:
   - npm/pip package with backdoor
   - Harvests environment on install
   - Exfiltrates credentials

3. Supply chain attack:
   - Popular package gets compromised
   - Update includes credential stealer
   - Thousands of installations affected

This is EXACTLY what happened in the Moltbook breach!
"""