# ASF Security Scanner Architecture

## Overview

The ASF Security Scanner uses a multi-layered approach to identify security risks in AI agent skills while minimizing false positives through intelligent context analysis.

## Core Components

### 1. Pattern Detection Engine

The scanner uses regex-based pattern matching organized into risk categories:

```python
dangerous_patterns = [...]  # High-risk patterns
warning_patterns = [...]    # Medium-risk patterns
destructive_patterns = [...] # Critical system commands
good_patterns = [...]       # Best practices to recognize
```

### 2. Context Analysis System

The key innovation is context-aware analysis that examines surrounding code:

```python
def analyze_context(content, pattern_match):
    # Examines 100 characters before/after match
    # Checks for negation words
    # Identifies documentation context
    # Detects comment blocks
    # Recognizes proper implementations
```

### 3. File Scanner

Scans multiple file types within each skill:
- `SKILL.md` - Main skill documentation
- `scripts/` - Executable scripts
- `references/` - Documentation files

### 4. Risk Assessment

Three-tier risk classification:
- **SAFE**: No security concerns found
- **WARNING**: Medium-risk patterns requiring review
- **DANGER**: High-risk patterns requiring immediate attention

## Scanning Flow

```
Start
  ↓
Identify Skill Directories
  ↓
For Each Skill:
  ├─→ Scan SKILL.md
  ├─→ Scan scripts/*.{py,js,sh,ts}
  └─→ Scan references/*.md
      ↓
  Pattern Matching
      ↓
  Context Analysis ← [Key Innovation]
      ↓
  False Positive Detection
      ↓
  Risk Classification
      ↓
Generate Report (HTML + JSON)
```

## False Positive Reduction

### Negation Detection
Recognizes security warnings as good practice:
- "don't", "never", "avoid", "warning"
- "should not", "must not", "careful"

### Documentation Context
Identifies educational content:
- "example:", "usage:", "note:"
- "best practice", "recommendation"

### Comment Recognition
Ignores patterns in comments:
- Python: `# comment`
- JavaScript: `// comment` or `/* block */`
- HTML: `<!-- comment -->`

### Proper Implementation Detection
Recognizes secure coding patterns:
- `os.environ.get()` - Correct env access
- `process.env.VAR` - Node.js best practice

## Scoring Algorithm

```python
security_score = 100 - (danger_skills * 10 + warning_skills * 3)
security_score = max(0, min(100, security_score))
```

## Output Generation

### JSON Report
Structured data for programmatic access:
```json
{
  "scan_date": "ISO-8601",
  "scanner_version": "2.0",
  "summary": {...},
  "skills": [...]
}
```

### HTML Report
Visual dashboard with:
- Summary statistics
- Risk categorization
- Detailed findings
- Recommendations

## Performance Considerations

- **Parallel Processing**: Each skill scanned independently
- **Memory Efficiency**: Stream large files
- **Cache Patterns**: Compiled regex patterns
- **Early Exit**: Stop scanning on critical findings

## Extensibility

### Adding New Patterns
1. Add regex to appropriate pattern list
2. Provide clear description
3. Test for false positives
4. Document in PATTERNS.md

### Custom Scanners
Inherit from base scanner class:
```python
class CustomScanner(BaseScanner):
    def scan_file(self, filepath):
        # Custom implementation
```

## Security Considerations

- Never execute scanned code
- Sanitize file paths
- Limit file sizes
- Handle malformed files gracefully
- Isolate scanning environment

## Future Enhancements

- [ ] Machine learning for pattern detection
- [ ] Behavioral analysis during execution
- [ ] Integration with CI/CD pipelines
- [ ] Real-time monitoring mode
- [ ] Distributed scanning for large codebases