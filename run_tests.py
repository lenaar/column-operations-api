#!/usr/bin/env python3
"""
Simple test runner script
"""
import subprocess
import sys

def run_tests():
    """Run all tests using pytest"""
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v',  # verbose
            '--tb=short'  # shorter traceback format
        ], check=True)
        
        print("✅ All tests passed!")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
