#!/usr/bin/env python3
"""
Simple wrapper script for Kotlin integration
Analyzes code and returns structured output for language detection
"""

import sys
import json
from guess_lexer import GuessLexer

def analyze_code_for_kotlin(code: str, filename: str = None):
    """Analyze code and return structured output for Kotlin integration"""
    try:
        lexer = GuessLexer()
        result = lexer.analyze_code(code, filename)
        
        # Return structured output that Kotlin can easily parse
        output = {
            "language": result.language,
            "confidence": result.confidence,
            "framework": result.framework,
            "evidence": result.evidence
        }
        
        # Print in a format that Kotlin can parse line by line
        print(f"Language: {result.language}")
        print(f"Confidence: {result.confidence}")
        print(f"Framework: {result.framework or 'None'}")
        print("Evidence:")
        for evidence in result.evidence:
            print(f"  - {evidence}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_code.py <code_file> [filename]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        with open(code_file, 'r', encoding='utf-8') as f:
            code = f.read()
        analyze_code_for_kotlin(code, filename)
    except FileNotFoundError:
        print(f"Error: File {code_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        sys.exit(1)
