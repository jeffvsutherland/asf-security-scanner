#!/usr/bin/env python3
"""
Test suite for ASF Security Scanner pattern matching
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from asf_skill_scanner_v2 import analyze_context, scan_file_for_patterns


class TestPatternMatching(unittest.TestCase):
    """Test pattern matching and false positive detection"""
    
    def test_env_file_detection(self):
        """Test detection of .env file access"""
        # Should detect direct .env access
        vulnerable_code = 'secrets = open(".env").read()'
        safe_code = 'api_key = os.environ.get("API_KEY")'
        
        # Test vulnerable code
        with open('test_vulnerable.py', 'w') as f:
            f.write(vulnerable_code)
        risk, issues, _, _ = scan_file_for_patterns('test_vulnerable.py')
        os.remove('test_vulnerable.py')
        self.assertNotEqual(risk, 'SAFE')
        self.assertTrue(any('.env' in issue for issue in issues))
        
        # Test safe code
        with open('test_safe.py', 'w') as f:
            f.write(safe_code)
        risk, issues, _, good = scan_file_for_patterns('test_safe.py')
        os.remove('test_safe.py')
        self.assertEqual(risk, 'SAFE')
        self.assertTrue(any('properly' in g for g in good))
    
    def test_negation_detection(self):
        """Test that warnings are not flagged as vulnerabilities"""
        warning_code = '''
        # Security warning
        # Don't use .env files directly
        # Never include credentials in code
        '''
        
        with open('test_warning.py', 'w') as f:
            f.write(warning_code)
        risk, issues, fps, _ = scan_file_for_patterns('test_warning.py')
        os.remove('test_warning.py')
        
        # Should be safe - these are warnings
        self.assertEqual(risk, 'SAFE')
        self.assertEqual(len(issues), 0)
        
    def test_documentation_context(self):
        """Test that documentation examples are not flagged"""
        doc_code = '''
        """
        Example of bad practice:
            file = open('.env')  # Don't do this!
        
        Good practice:
            api_key = os.environ.get('API_KEY')
        """
        '''
        
        with open('test_doc.py', 'w') as f:
            f.write(doc_code)
        risk, issues, fps, good = scan_file_for_patterns('test_doc.py')
        os.remove('test_doc.py')
        
        # Documentation should be recognized as safe
        self.assertEqual(risk, 'SAFE')
        self.assertTrue(any('properly' in g for g in good))
    
    def test_post_request_detection(self):
        """Test detection of POST requests"""
        post_code = '''
        import requests
        response = requests.post('https://api.example.com/data', json=data)
        '''
        
        with open('test_post.py', 'w') as f:
            f.write(post_code)
        risk, issues, _, _ = scan_file_for_patterns('test_post.py')
        os.remove('test_post.py')
        
        # POST requests should be WARNING level
        self.assertEqual(risk, 'WARNING')
        self.assertTrue(any('POST' in issue for issue in issues))
    
    def test_destructive_commands(self):
        """Test detection of dangerous system commands"""
        dangerous_code = 'os.system("rm -rf /")'
        
        with open('test_danger.py', 'w') as f:
            f.write(dangerous_code)
        risk, issues, _, _ = scan_file_for_patterns('test_danger.py')
        os.remove('test_danger.py')
        
        # Should be flagged as DANGER
        self.assertEqual(risk, 'DANGER')
        self.assertTrue(any('destructive' in issue.lower() for issue in issues))


class TestSpecificSkills(unittest.TestCase):
    """Test specific skills that were problematic in v1"""
    
    def test_oracle_skill(self):
        """Test that oracle skill warnings are not flagged"""
        oracle_content = '''
        # oracle skill documentation
        
        ## Safety
        - Don't attach secrets by default (.env, key files, auth tokens).
        '''
        
        with open('test_oracle.md', 'w') as f:
            f.write(oracle_content)
        risk, issues, _, _ = scan_file_for_patterns('test_oracle.md')
        os.remove('test_oracle.md')
        
        # Should be SAFE - it's warning against bad practices
        self.assertEqual(risk, 'SAFE')
        self.assertEqual(len(issues), 0)
    
    def test_openai_image_gen(self):
        """Test that proper env usage is recognized"""
        openai_code = '''
        import os
        api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
        '''
        
        with open('test_openai.py', 'w') as f:
            f.write(openai_code)
        risk, issues, _, good = scan_file_for_patterns('test_openai.py')
        os.remove('test_openai.py')
        
        # Should be SAFE - proper environment variable usage
        self.assertEqual(risk, 'SAFE')
        self.assertTrue(any('properly' in g for g in good))


if __name__ == '__main__':
    unittest.main()