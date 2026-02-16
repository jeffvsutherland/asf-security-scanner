#!/usr/bin/env python3
"""
ASF Skill Scanner Demo - Sprint 2 Deliverable
Checks all skills in Clawdbot implementation for security risks
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print the header banner"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        🔒 Agent Security Framework - Skill Scanner 🔒         ║")
    print("║                    Sprint 2 Demo Version                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print(f"Scanning Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Scanning all skills in your Clawdbot implementation...")
    print()

def scan_file_for_patterns(filepath):
    """Scan a file for security patterns"""
    dangerous_patterns = [
        (r'~/\.clawdbot/\.env', 'Accesses Clawdbot credentials'),
        (r'~/\.ssh', 'Accesses SSH keys'),
        (r'~/\.aws', 'Accesses AWS credentials'),
        (r'process\.env', 'Reads environment variables'),
        (r'\.env', 'Accesses .env files'),
        (r'password|secret|token|api_key', 'References sensitive data'),
    ]
    
    warning_patterns = [
        (r'curl.*POST|wget.*POST|fetch.*POST', 'Makes POST requests'),
        (r'exec\(|eval\(|system\(|sh -c', 'Executes shell commands'),
        (r'fs\.write|writeFile', 'Writes to filesystem'),
        (r'net\.connect|http\.request', 'Makes network connections'),
    ]
    
    destructive_patterns = [
        (r'rm -rf', 'Contains destructive rm command'),
        (r'dd if=', 'Contains disk destroyer command'),
        (r'mkfs|format', 'Contains format commands'),
    ]
    
    issues = []
    risk_level = 'SAFE'
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Check dangerous patterns
        for pattern, description in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(description)
                risk_level = 'DANGER'
                
        # Check destructive patterns
        for pattern, description in destructive_patterns:
            if re.search(pattern, content):
                issues.append(description)
                risk_level = 'DANGER'
                
        # Check warning patterns (only if not already DANGER)
        if risk_level != 'DANGER':
            for pattern, description in warning_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(description)
                    risk_level = 'WARNING'
                    
    except Exception as e:
        pass
    
    return risk_level, issues

def scan_skill(skill_path):
    """Scan a skill directory for security issues"""
    skill_name = os.path.basename(skill_path)
    risk_level = 'SAFE'
    all_issues = []
    
    # Check SKILL.md
    skill_md_path = os.path.join(skill_path, 'SKILL.md')
    if os.path.exists(skill_md_path):
        level, issues = scan_file_for_patterns(skill_md_path)
        if level == 'DANGER':
            risk_level = 'DANGER'
        elif level == 'WARNING' and risk_level != 'DANGER':
            risk_level = 'WARNING'
        all_issues.extend(issues)
    
    # Check scripts directory
    scripts_path = os.path.join(skill_path, 'scripts')
    if os.path.exists(scripts_path):
        for script in os.listdir(scripts_path):
            script_path = os.path.join(scripts_path, script)
            if os.path.isfile(script_path):
                level, issues = scan_file_for_patterns(script_path)
                if level == 'DANGER':
                    risk_level = 'DANGER'
                elif level == 'WARNING' and risk_level != 'DANGER':
                    risk_level = 'WARNING'
                all_issues.extend([f"scripts/{script}: {issue}" for issue in issues])
    
    # Check references directory
    refs_path = os.path.join(skill_path, 'references')
    if os.path.exists(refs_path):
        for ref in os.listdir(refs_path):
            ref_path = os.path.join(refs_path, ref)
            if os.path.isfile(ref_path) and ref.endswith('.md'):
                level, issues = scan_file_for_patterns(ref_path)
                # Don't flag references as dangerous, just note them
                if issues:
                    all_issues.extend([f"references/{ref}: {issue}" for issue in issues])
    
    return {
        'name': skill_name,
        'status': risk_level,
        'issues': list(set(all_issues))  # Remove duplicates
    }

def main():
    """Main scanner function"""
    print_header()
    
    results = []
    
    # Scan built-in skills
    builtin_path = '/opt/homebrew/lib/node_modules/clawdbot/skills'
    print(f"📁 Scanning built-in skills in {builtin_path}")
    print("────────────────────────────────────────────────────────────────")
    
    if os.path.exists(builtin_path):
        for skill_dir in os.listdir(builtin_path):
            skill_path = os.path.join(builtin_path, skill_dir)
            if os.path.isdir(skill_path):
                result = scan_skill(skill_path)
                results.append(result)
                print(f"  Scanned: {skill_dir}")
    
    # Scan user skills
    user_path = '/Users/jeffsutherland/clawd/skills'
    print()
    print(f"📁 Scanning user skills in {user_path}")
    print("────────────────────────────────────────────────────────────────")
    
    if os.path.exists(user_path):
        for skill_dir in os.listdir(user_path):
            skill_path = os.path.join(user_path, skill_dir)
            if os.path.isdir(skill_path):
                result = scan_skill(skill_path)
                results.append(result)
                print(f"  Scanned: {skill_dir}")
    
    # Calculate summary
    total_skills = len(results)
    safe_skills = len([r for r in results if r['status'] == 'SAFE'])
    warning_skills = len([r for r in results if r['status'] == 'WARNING'])
    danger_skills = len([r for r in results if r['status'] == 'DANGER'])
    
    # Display results
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                     🔍 SCAN RESULTS 🔍                        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("📊 Summary:")
    print(f"   Total Skills Scanned: {total_skills}")
    print(f"   ✅ Safe Skills: {safe_skills}")
    print(f"   ⚠️  Warning Skills: {warning_skills}")
    print(f"   🚨 Danger Skills: {danger_skills}")
    print()
    
    # Display detailed results
    print("📋 Detailed Results:")
    print("────────────────────────────────────────────────────────────────")
    print(f"{'SKILL NAME':<30} {'STATUS':<12} {'ISSUES'}")
    print("────────────────────────────────────────────────────────────────")
    
    # Sort by risk level
    sorted_results = sorted(results, key=lambda x: {'DANGER': 0, 'WARNING': 1, 'SAFE': 2}[x['status']])
    
    for result in sorted_results:
        status_icon = {'SAFE': '✅', 'WARNING': '⚠️ ', 'DANGER': '🚨'}[result['status']]
        status_color = {'SAFE': Colors.GREEN, 'WARNING': Colors.YELLOW, 'DANGER': Colors.RED}[result['status']]
        
        print(f"{result['name']:<30} {status_color}{status_icon} {result['status']:<9}{Colors.ENDC} ", end='')
        if result['issues']:
            print(f"{result['issues'][0]}")
            for issue in result['issues'][1:]:
                print(f"{' '*44} {issue}")
        else:
            print()
    
    # Recommendations
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                 🛡️  RECOMMENDATIONS 🛡️                        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    if danger_skills > 0:
        print(f"{Colors.RED}🚨 CRITICAL: Found {danger_skills} skills with high-risk patterns!{Colors.ENDC}")
        print("   - Review these skills immediately")
        print("   - Check if credential access is legitimate")
        print("   - Consider sandboxing or removing if untrusted")
        print()
    
    if warning_skills > 0:
        print(f"{Colors.YELLOW}⚠️  WARNING: Found {warning_skills} skills with medium-risk patterns{Colors.ENDC}")
        print("   - Verify external POST requests are to trusted endpoints")
        print("   - Ensure shell commands are properly sanitized")
        print("   - Consider adding permission manifests")
        print()
    
    print("✅ General Recommendations:")
    print("   1. Always read SKILL.md before installing new skills")
    print("   2. Use skill sandboxing when available")
    print("   3. Regularly audit skills for changes")
    print("   4. Implement permission manifests for all skills")
    print("   5. Never store credentials in plain text files")
    print()
    
    # Calculate security score
    security_score = 100 - (danger_skills * 10 + warning_skills * 5)
    security_score = max(0, min(100, security_score))
    
    score_color = Colors.GREEN if security_score >= 80 else Colors.YELLOW if security_score >= 60 else Colors.RED
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print(f"║              {score_color}🏆 SECURITY SCORE: {security_score}/100 🏆{Colors.ENDC}               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Generate JSON report
    report = {
        'scan_date': datetime.now().isoformat(),
        'summary': {
            'total_skills': total_skills,
            'safe_skills': safe_skills,
            'warning_skills': warning_skills,
            'danger_skills': danger_skills,
            'security_score': security_score
        },
        'skills': results
    }
    
    report_path = '/Users/jeffsutherland/clawd/asf-skill-scan-report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Full report saved to: {report_path}")
    print()
    print("This is the ASF Skill Scanner - Part of Sprint 2 Deliverables")
    print("Next step: Deploy this to Discord bots and customer pilots")

if __name__ == '__main__':
    main()