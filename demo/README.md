# ASF Security Scanner Demo

This demo shows the complete ASF security lifecycle using real vulnerabilities found in popular Clawdbot skills.

## 🎯 What This Demo Shows

1. **Detection**: Finding vulnerabilities in oracle and openai-image-gen skills
2. **Remediation**: Creating secure versions that protect credentials
3. **Verification**: Confirming the vulnerabilities are fixed

## 🚀 Quick Start

```bash
# Run the complete demo
./run-demo.sh

# Or run steps individually
python3 step1-scan-vulnerable.py
python3 step2-show-secure-code.py
python3 step3-verify-secure.py
```

## 📁 Demo Files

- `run-demo.sh` - Complete automated demo script
- `step1-scan-vulnerable.py` - Shows current vulnerabilities
- `step2-show-secure-code.py` - Displays secure implementations
- `step3-verify-secure.py` - Verifies skills are secure
- `vulnerable-examples/` - Example vulnerable code
- `secure-examples/` - Fixed secure versions

## 🔍 The Vulnerabilities

### Oracle Skill
- **Problem**: Reads OPENAI_API_KEY from environment
- **Risk**: Any malicious code can steal the key
- **Fix**: Use Clawdbot's encrypted credential vault

### OpenAI-Image-Gen Skill
- **Problem**: Line 176: `api_key = os.environ.get("OPENAI_API_KEY")`
- **Risk**: Same vulnerability that led to Moltbook's 1.5M token breach
- **Fix**: Replace with `get_secure_credential("openai", "api_key")`

## 📊 Expected Output

### Step 1: Initial Scan
```
oracle                 🚨 DANGER    Accesses .env files
openai-image-gen       🚨 DANGER    Line 176 exposes API keys
```

### Step 2: Secure Code
```python
# OLD (Vulnerable)
api_key = os.environ.get("OPENAI_API_KEY")

# NEW (Secure)
api_key = get_secure_credential("openai", "api_key")
```

### Step 3: Verification
```
oracle-secure          ✅ SECURE    Uses encrypted vault
openai-image-gen-secure ✅ SECURE    Protected credentials
```

## 🎬 Video Script

For recording a demo video, follow `demo-video-script.md`

## 💡 Key Takeaway

This demonstrates that ASF doesn't just find problems - it provides working solutions that prevent breaches like Moltbook's 1.5M token exposure.