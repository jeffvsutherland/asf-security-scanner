# Contributing to ASF Security Scanner

Thank you for your interest in contributing to the Agent Security Framework Security Scanner! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## 🐛 Reporting Issues

### Security Vulnerabilities
If you discover a security vulnerability in the scanner itself, please:
1. **Do NOT** open a public issue
2. Email details to: asf-security@agentsaturday.dev
3. Include steps to reproduce and potential impact

### Bug Reports
For bugs, please open an issue with:
- Scanner version
- Python version
- OS/Platform
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## 🚀 Feature Requests

Open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Alternative approaches considered
- Impact on existing functionality

## 📝 Pull Requests

### Before You Start
1. Check existing issues/PRs to avoid duplicates
2. For major changes, open an issue first to discuss
3. Fork the repository and create a feature branch

### Development Process
1. **Setup**
   ```bash
   git clone https://github.com/yourusername/asf-security-scanner.git
   cd asf-security-scanner
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow existing code style
   - Add tests for new patterns
   - Update documentation
   - Ensure all tests pass

3. **Commit Guidelines**
   ```
   feat: Add new security pattern detection
   fix: Correct false positive in env detection
   docs: Update installation instructions
   test: Add tests for POST request detection
   refactor: Simplify context analysis logic
   ```

4. **Submit PR**
   - Clear description of changes
   - Link related issues
   - Include test results
   - Update version number if needed

### Code Style
- Python 3.9+ compatible
- Follow PEP 8
- Use type hints where appropriate
- Add docstrings for new functions
- Keep line length under 100 characters

## 🧪 Testing

### Running Tests
```bash
python3 -m pytest tests/
```

### Adding Tests
- Test new patterns in `tests/test_patterns.py`
- Include both positive and negative cases
- Test false positive scenarios
- Document expected behavior

### Test Coverage
Aim for 90%+ coverage for new code:
```bash
python3 -m pytest --cov=asf_skill_scanner_v2 tests/
```

## 📚 Documentation

### What to Document
- New patterns and their detection logic
- Configuration options
- API changes
- Usage examples
- Performance impacts

### Where to Document
- Code: Inline comments and docstrings
- Features: Update README.md
- Technical: Add to docs/ folder
- Examples: Add to examples/ folder

## 🔧 Pattern Contributions

When adding new security patterns:

1. **Research the Risk**
   - Understand the security implication
   - Find real-world examples
   - Consider false positive scenarios

2. **Implement Detection**
   ```python
   # Add to appropriate pattern list
   dangerous_patterns = [
       (r'your_regex_pattern', 'Clear description of risk'),
   ]
   ```

3. **Add Context Analysis**
   - Consider when the pattern is legitimate
   - Add false positive detection
   - Test with real skill examples

4. **Document the Pattern**
   - Add to `docs/PATTERNS.md`
   - Include examples of risky vs safe usage
   - Explain remediation steps

## 🏷️ Version Guidelines

- **Major** (X.0.0): Breaking changes, new scanning approach
- **Minor** (0.X.0): New patterns, features, significant improvements
- **Patch** (0.0.X): Bug fixes, minor improvements, documentation

## 📋 Checklist for Contributors

Before submitting:
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog entry added
- [ ] Version bumped if needed
- [ ] PR description is clear
- [ ] Related issues linked
- [ ] CI/CD passes

## 🙏 Recognition

Contributors will be acknowledged in:
- GitHub contributors list
- CONTRIBUTORS.md file
- Release notes

Thank you for helping make AI agents more secure!