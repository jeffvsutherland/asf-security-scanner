# ASF Demo Video Script

## Duration: ~3-5 minutes

### Opening (0:00-0:30)
"Hi, I'm going to show you how the Agent Security Framework prevents the kind of vulnerabilities that led to Moltbook's breach where 1.5 million API tokens were exposed.

We'll look at two popular AI agent skills - oracle and openai-image-gen - that have the exact same security flaws. Then I'll show you how ASF not only detects these issues but provides working solutions."

### Step 1: Detection (0:30-1:30)
"First, let's run the ASF scanner on these skills."

```bash
./run-demo.sh
```

"As you can see, both skills are flagged as dangerous:
- Oracle reads API keys from environment variables
- OpenAI-image-gen has the vulnerable code on line 176

This is exactly how Moltbook's breach happened - credentials stored in places where any code could access them."

*Show the vulnerable code snippet*

"Here's line 176 - it reads the OpenAI API key directly from the environment. Any malicious code, compromised dependency, or supply chain attack can steal this."

### Step 2: Solution (1:30-2:30)
*Press Enter to continue to Step 2*

"Now let's look at the secure versions we've created.

Instead of environment variables, we use Clawdbot's encrypted credential vault. The API keys are:
- Stored encrypted
- Access controlled by permissions
- Never exposed to other processes

Here's the key change - instead of os.environ.get(), we use get_secure_credential() which reads from the encrypted vault."

### Step 3: Verification (2:30-3:30)
*Press Enter to continue to Step 3*

"Let's verify the secure versions pass our security scan."

"Perfect! Both skills now pass with flying colors:
- No environment variable access
- Credentials properly protected
- Zero vulnerabilities detected

This is the complete ASF workflow - detect, fix, and verify."

### Closing (3:30-4:00)
"In just a few minutes, we've eliminated the exact vulnerabilities that caused the Moltbook breach. 

ASF is now available on GitHub. You can scan your own AI agent skills and prevent credential theft before it happens.

Visit github.com/jeffvsutherland/asf-security-scanner to get started.

Thanks for watching!"

## Recording Tips

1. **Terminal Setup**
   - Dark theme with good contrast
   - Font size 14-16pt
   - Window size ~100x30

2. **Pacing**
   - Pause after each major point
   - Let output display fully before continuing
   - Use mouse to highlight important lines

3. **Screen Recording**
   - 1920x1080 minimum
   - 60fps if possible
   - Include system audio for terminal beeps

4. **Post-Production**
   - Add title card with ASF logo
   - Highlight vulnerable code in red
   - Highlight secure code in green
   - Add GitHub URL as overlay at end