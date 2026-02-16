#!/usr/bin/env python3
"""
ASF Security Scanner - Pre-Installation Check
Check a skill's security BEFORE installing it
"""

import os
import sys
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

# ANSI color codes
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check_docker_security():
    """Check if Docker is properly configured for security"""
    docker_issues = []
    
    # Check if Docker is installed
    docker_installed = os.system("which docker > /dev/null 2>&1") == 0
    if not docker_installed:
        docker_issues.append("Docker not installed - skills run with full system access!")
        return False, docker_issues
    
    # Check if running as root
    if os.geteuid() == 0:
        docker_issues.append("Running as root - Docker containers may have elevated privileges")
    
    # Check for exposed secrets in Docker
    try:
        # Check docker inspect for common secret patterns
        result = os.popen("docker ps -q 2>/dev/null | xargs -I {} docker inspect {} 2>/dev/null | grep -i 'api_key\\|password\\|secret\\|token' | head -10").read()
        if result.strip():
            docker_issues.append("WARNING: Exposed secrets found in running Docker containers!")
            docker_issues.append("Sample: " + result.strip()[:100] + "...")
    except:
        pass
    
    # Check Docker daemon configuration
    docker_config_path = Path.home() / ".docker/config.json"
    if docker_config_path.exists():
        try:
            with open(docker_config_path, 'r') as f:
                config = json.load(f)
                if 'auths' in config and config['auths']:
                    docker_issues.append("Docker config contains authentication - ensure it's properly secured")
        except:
            pass
    
    if docker_issues:
        return False, docker_issues
    return True, ["Docker appears properly configured"]

def analyze_skill_from_url(skill_url):
    """Download and analyze a skill before installation"""
    print(f"\n🔍 Downloading skill from: {skill_url}")
    
    try:
        response = urllib.request.urlopen(skill_url)
        content = response.read().decode('utf-8')
    except Exception as e:
        return "ERROR", [f"Failed to download skill: {str(e)}"], []
    
    # Critical patterns that indicate malicious behavior
    critical_patterns = [
        (r'webhook\.site', 'Exfiltrates data to webhook.site'),
        (r'curl.*-d.*[@$].*webhook', 'Sends data to external webhook'),
        (r'~/.clawdbot/\.env.*curl', 'Reads and exfiltrates .env file'),
        (r'cat.*\.env.*\|.*curl', 'Pipes credentials to external server'),
        (r'OPENAI_API_KEY.*POST', 'Exfiltrates OpenAI API key'),
    ]
    
    high_risk_patterns = [
        (r'~/\.clawdbot/\.env', 'Accesses Clawdbot credentials'),
        (r'~/\.aws/credentials', 'Accesses AWS credentials'),
        (r'~/\.ssh', 'Accesses SSH keys'),
        (r'docker\s+run.*--privileged', 'Runs Docker with privileged access'),
        (r'docker.*-v\s*/:/.*', 'Mounts entire filesystem in Docker'),
    ]
    
    medium_risk_patterns = [
        (r'curl.*POST|wget.*POST', 'Makes POST requests'),
        (r'eval\(|exec\(', 'Executes dynamic code'),
        (r'docker\s+run', 'Runs Docker containers'),
    ]
    
    issues = []
    docker_warnings = []
    risk_level = "SAFE"
    
    # Check critical patterns first
    for pattern, description in critical_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"🚨 CRITICAL: {description}")
            risk_level = "CRITICAL"
    
    # Check high risk patterns
    if risk_level != "CRITICAL":
        for pattern, description in high_risk_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"⚠️  HIGH RISK: {description}")
                if risk_level == "SAFE":
                    risk_level = "HIGH"
    
    # Check medium risk patterns
    if risk_level == "SAFE":
        for pattern, description in medium_risk_patterns:
            if re.search(pattern, content):
                issues.append(f"⚡ MEDIUM: {description}")
                risk_level = "MEDIUM"
    
    # Special Docker checks
    if 'docker' in content.lower():
        docker_warnings.append("This skill uses Docker containers")
        if '--privileged' in content:
            docker_warnings.append("⚠️  Requests privileged Docker access!")
        if re.search(r'-v\s*[^:]+:/[^:]*:', content):
            docker_warnings.append("Mounts host directories into Docker")
    
    # Check for the specific weather skill pattern that was malicious
    if re.search(r'weather.*skill|skill.*weather', content, re.IGNORECASE):
        if re.search(r'webhook\.site|exfiltrat|steal|\.env.*POST', content, re.IGNORECASE):
            issues.insert(0, "🚨 MATCHES PATTERN OF KNOWN MALICIOUS WEATHER SKILL!")
            risk_level = "CRITICAL"
    
    return risk_level, issues, docker_warnings

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║       🔒 Security Scanner - Pre-Installation Check 🔒         ║")
    print("║              Check Skills BEFORE You Install Them             ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    if len(sys.argv) < 2:
        print("\n📋 Usage:")
        print("  python3 pre-install-check.py <skill-url-or-path>")
        print("\n📌 Examples:")
        print("  python3 pre-install-check.py https://raw.githubusercontent.com/user/skill/main/SKILL.md")
        print("  python3 pre-install-check.py ./downloaded-skill.md")
        print("\n🐳 Docker Security Check:")
        print("  python3 pre-install-check.py --docker-check")
        sys.exit(1)
    
    if sys.argv[1] == "--docker-check":
        print("\n🐳 Checking Docker Security Configuration...")
        docker_safe, docker_issues = check_docker_security()
        
        if docker_safe:
            print(f"{Colors.GREEN}✅ Docker is properly configured for security{Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ Docker security issues found:{Colors.ENDC}")
            for issue in docker_issues:
                print(f"   • {issue}")
        return
    
    skill_source = sys.argv[1]
    
    # Check Docker first
    print("\n🐳 Docker Security Status:")
    docker_safe, docker_status = check_docker_security()
    
    if not docker_safe:
        print(f"{Colors.YELLOW}⚠️  Docker issues detected:{Colors.ENDC}")
        for issue in docker_status:
            print(f"   • {issue}")
        print(f"{Colors.YELLOW}   Skills will run with full system access!{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}✅ Docker properly configured{Colors.ENDC}")
    
    # Analyze the skill
    if skill_source.startswith('http'):
        risk_level, issues, docker_warnings = analyze_skill_from_url(skill_source)
    else:
        # Local file
        try:
            with open(skill_source, 'r') as f:
                content = f.read()
            
            # Use the same analysis function
            risk_level = "SAFE"
            issues = []
            docker_warnings = []
            
            # Check critical patterns first
            critical_patterns = [
                (r'webhook\.site', 'Exfiltrates data to webhook.site'),
                (r'curl.*-d.*[@$].*webhook', 'Sends data to external webhook'),
                (r'~/.clawdbot/\.env.*curl', 'Reads and exfiltrates .env file'),
                (r'cat.*\.env.*\|.*curl', 'Pipes credentials to external server'),
                (r'OPENAI_API_KEY.*POST', 'Exfiltrates OpenAI API key'),
            ]
            
            high_risk_patterns = [
                (r'~/\.clawdbot/\.env', 'Accesses Clawdbot credentials'),
                (r'~/\.aws/credentials', 'Accesses AWS credentials'),
                (r'~/\.ssh', 'Accesses SSH keys'),
                (r'docker\s+run.*--privileged', 'Runs Docker with privileged access'),
                (r'docker.*-v\s*/:/.*', 'Mounts entire filesystem in Docker'),
            ]
            
            medium_risk_patterns = [
                (r'curl.*POST|wget.*POST', 'Makes POST requests'),
                (r'eval\(|exec\(', 'Executes dynamic code'),
                (r'docker\s+run', 'Runs Docker containers'),
            ]
            
            # Check patterns
            for pattern, description in critical_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(f"🚨 CRITICAL: {description}")
                    risk_level = "CRITICAL"
            
            if risk_level != "CRITICAL":
                for pattern, description in high_risk_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append(f"⚠️  HIGH RISK: {description}")
                        if risk_level == "SAFE":
                            risk_level = "HIGH"
            
            if risk_level == "SAFE":
                for pattern, description in medium_risk_patterns:
                    if re.search(pattern, content):
                        issues.append(f"⚡ MEDIUM: {description}")
                        risk_level = "MEDIUM"
            
            # Docker checks
            if 'docker' in content.lower():
                docker_warnings.append("This skill uses Docker containers")
                if '--privileged' in content:
                    docker_warnings.append("⚠️  Requests privileged Docker access!")
                if re.search(r'-v\s*[^:]+:/[^:]*:', content):
                    docker_warnings.append("Mounts host directories into Docker")
                    
        except Exception as e:
            print(f"{Colors.RED}Error reading file: {e}{Colors.ENDC}")
            sys.exit(1)
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 SECURITY ANALYSIS RESULTS")
    print("="*60)
    
    # Risk level display
    risk_colors = {
        "SAFE": Colors.GREEN,
        "MEDIUM": Colors.YELLOW,
        "HIGH": Colors.RED,
        "CRITICAL": Colors.RED + Colors.BOLD,
        "ERROR": Colors.RED
    }
    
    risk_emoji = {
        "SAFE": "✅",
        "MEDIUM": "⚡",
        "HIGH": "⚠️",
        "CRITICAL": "🚨",
        "ERROR": "❌"
    }
    
    print(f"\nRisk Level: {risk_colors.get(risk_level, '')}{risk_emoji.get(risk_level, '')} {risk_level}{Colors.ENDC}")
    
    if issues:
        print("\n🔍 Security Issues Found:")
        for issue in issues:
            print(f"   {issue}")
    
    if docker_warnings and not docker_safe:
        print(f"\n{Colors.YELLOW}🐳 Docker Concerns:{Colors.ENDC}")
        for warning in docker_warnings:
            print(f"   {warning}")
        print(f"   {Colors.YELLOW}Without proper Docker isolation, this skill has FULL system access!{Colors.ENDC}")
    
    # Recommendations
    print("\n📋 Recommendation:")
    if risk_level == "CRITICAL":
        print(f"{Colors.RED}{Colors.BOLD}   DO NOT INSTALL THIS SKILL!{Colors.ENDC}")
        print(f"{Colors.RED}   This appears to be malicious software that will steal your credentials.{Colors.ENDC}")
    elif risk_level == "HIGH":
        print(f"{Colors.RED}   ⚠️  HIGH RISK - Install only if you trust the source completely{Colors.ENDC}")
        print(f"{Colors.YELLOW}   Consider running in isolated environment{Colors.ENDC}")
    elif risk_level == "MEDIUM":
        print(f"{Colors.YELLOW}   Review the code carefully before installation{Colors.ENDC}")
        print(f"{Colors.YELLOW}   Ensure you understand what it does{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}   Appears safe to install{Colors.ENDC}")
        print(f"{Colors.GREEN}   No obvious security concerns detected{Colors.ENDC}")
    
    # Example malicious skills
    if '--examples' in sys.argv:
        print("\n" + "="*60)
        print("📌 EXAMPLE: Known Malicious Weather Skill")
        print("="*60)
        print("URL: https://malicious.example/weather-skill/SKILL.md")
        print("Pattern detected:")
        print('  - Reads ~/.clawdbot/.env')
        print('  - POSTs to webhook.site')
        print('  - Disguised as legitimate weather skill')
        print(f"{Colors.RED}Result: CRITICAL - Credential stealer!{Colors.ENDC}")

if __name__ == "__main__":
    main()