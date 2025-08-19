#!/usr/bin/env python3
"""
Danis's Powerful Guess Lexer Application
Command-line interface for the code detection engine
"""

import click
import sys
import os
from pathlib import Path
from typing import List, Optional
from colorama import Fore, Style, init
import json

from guess_lexer import GuessLexer, format_result, DetectionResult

# Initialize colorama for cross-platform color support
init(autoreset=True)


class ColorFormatter:
    """Colorful output formatter for better UX"""
    
    @staticmethod
    def success(text: str) -> str:
        return f"{Fore.GREEN}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def warning(text: str) -> str:
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def error(text: str) -> str:
        return f"{Fore.RED}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def info(text: str) -> str:
        return f"{Fore.CYAN}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def header(text: str) -> str:
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          🎯 DANIS'S POWERFUL GUESS LEXER 🎯            ║
║                                                              ║
║              Advanced Code Language Detection Engine         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Danis's Powerful Guess Lexer - Advanced code language detection"""
    pass


@cli.command()
@click.argument('code', required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='Analyze code from file')
@click.option('--json-output', '-j', is_flag=True, help='Output results in JSON format')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed analysis')
def analyze(code: Optional[str], file: Optional[str], json_output: bool, verbose: bool):
    """Analyze code and detect language/framework"""
    
    if not json_output:
        print_banner()
    
    lexer = GuessLexer()
    
    # Determine input source
    if file:
        if not json_output:
            print(ColorFormatter.info(f"📂 Analyzing file: {file}"))
        result = lexer.analyze_file(file)
        source_info = f"File: {file}"
    elif code:
        if not json_output:
            print(ColorFormatter.info("📝 Analyzing provided code..."))
        result = lexer.analyze_code(code)
        source_info = "Direct input"
    else:
        if not json_output:
            print(ColorFormatter.info("📝 Reading code from stdin..."))
        code = sys.stdin.read()
        if not code.strip():
            print(ColorFormatter.error("❌ No code provided!"))
            sys.exit(1)
        result = lexer.analyze_code(code)
        source_info = "stdin"
    
    # Output results
    if json_output:
        output_data = {
            "source": source_info,
            "language": result.language,
            "confidence": result.confidence,
            "framework": result.framework,
            "evidence": result.evidence
        }
        print(json.dumps(output_data, indent=2))
    else:
        print("\n" + "="*60)
        print(ColorFormatter.header("🔍 DETECTION RESULTS"))
        print("="*60)
        
        # Format and colorize results
        confidence_color = Fore.GREEN if result.confidence > 0.7 else Fore.YELLOW if result.confidence > 0.4 else Fore.RED
        
        print(f"🎯 {ColorFormatter.success('Language:')} {ColorFormatter.header(result.language.upper())}")
        print(f"📊 {ColorFormatter.success('Confidence:')} {confidence_color}{result.confidence:.1%}{Style.RESET_ALL}")
        
        if result.framework:
            print(f"🚀 {ColorFormatter.success('Framework:')} {ColorFormatter.header(result.framework.upper())}")
        
        if verbose and result.evidence:
            print(f"\n📝 {ColorFormatter.info('Evidence:')}")
            for i, evidence in enumerate(result.evidence[:15], 1):
                print(f"  {i:2d}. {evidence}")
        
        # Confidence interpretation
        print(f"\n💡 {ColorFormatter.info('Confidence Level:')}")
        if result.confidence >= 0.8:
            print(f"   {ColorFormatter.success('🟢 Very High - Highly confident in detection')}")
        elif result.confidence >= 0.6:
            print(f"   {ColorFormatter.success('🟡 High - Good confidence in detection')}")
        elif result.confidence >= 0.4:
            print(f"   {ColorFormatter.warning('🟠 Medium - Moderate confidence')}")
        else:
            print(f"   {ColorFormatter.error('🔴 Low - Low confidence, may need more context')}")


@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('--recursive', '-r', is_flag=True, help='Scan directory recursively')
@click.option('--json-output', '-j', is_flag=True, help='Output results in JSON format')
@click.option('--min-confidence', '-c', type=float, default=0.3, help='Minimum confidence threshold')
@click.option('--extensions', '-e', multiple=True, help='Filter by file extensions (e.g., .py .js)')
def scan(directory: str, recursive: bool, json_output: bool, min_confidence: float, extensions: List[str]):
    """Scan directory for code files and analyze them"""
    
    if not json_output:
        print_banner()
        print(ColorFormatter.info(f"🔍 Scanning directory: {directory}"))
        if recursive:
            print(ColorFormatter.info("📁 Recursive scan enabled"))
    
    lexer = GuessLexer()
    results: List[dict] = []
    
    # Get file pattern
    pattern = "**/*" if recursive else "*"
    path_obj = Path(directory)
    
    # Common code file extensions if none specified
    if not extensions:
        extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.sql', '.html', '.css']
    
    # Scan files
    files_found = 0
    files_analyzed = 0
    
    for file_path in path_obj.glob(pattern):
        if file_path.is_file():
            # Check extension filter
            if extensions and not any(str(file_path).endswith(ext) for ext in extensions):
                continue
                
            files_found += 1
            
            try:
                result = lexer.analyze_file(str(file_path))
                
                if result.confidence >= min_confidence:
                    files_analyzed += 1
                    
                    file_info = {
                        "file": str(file_path.relative_to(path_obj)),
                        "language": result.language,
                        "confidence": result.confidence,
                        "framework": result.framework
                    }
                    results.append(file_info)
                    
                    if not json_output:
                        confidence_icon = "🟢" if result.confidence > 0.7 else "🟡" if result.confidence > 0.5 else "🟠"
                        framework_info = f" ({result.framework})" if result.framework else ""
                        print(f"{confidence_icon} {file_info['file']} → {result.language.upper()}{framework_info} ({result.confidence:.1%})")
                        
            except Exception as e:
                if not json_output:
                    print(ColorFormatter.error(f"❌ Error analyzing {file_path}: {str(e)}"))
    
    # Summary
    if json_output:
        summary = {
            "summary": {
                "directory": directory,
                "files_found": files_found,
                "files_analyzed": files_analyzed,
                "min_confidence": min_confidence
            },
            "results": results
        }
        print(json.dumps(summary, indent=2))
    else:
        print(f"\n{ColorFormatter.header('📊 SCAN SUMMARY')}")
        print("="*40)
        print(f"📁 Files found: {files_found}")
        print(f"🔍 Files analyzed: {files_analyzed}")
        print(f"📊 Min confidence: {min_confidence:.1%}")
        
        # Language distribution
        if results:
            language_counts = {}
            for result in results:
                lang = result['language']
                language_counts[lang] = language_counts.get(lang, 0) + 1
            
            print(f"\n{ColorFormatter.info('🏷️  Language Distribution:')}")
            for lang, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(results)) * 100
                print(f"  {lang.upper()}: {count} files ({percentage:.1f}%)")


@cli.command()
def info():
    """Show information about supported languages and frameworks"""
    print_banner()
    
    lexer = GuessLexer()
    
    print(ColorFormatter.header("🗂️  SUPPORTED LANGUAGES"))
    print("="*50)
    languages = lexer.get_supported_languages()
    for i, lang in enumerate(sorted(languages), 1):
        print(f"{i:2d}. {lang.upper()}")
    
    print(f"\n{ColorFormatter.header('🚀 SUPPORTED FRAMEWORKS')}")
    print("="*50)
    frameworks = lexer.get_supported_frameworks()
    for i, framework in enumerate(sorted(frameworks), 1):
        framework_info = lexer.framework_patterns[framework]
        print(f"{i:2d}. {framework.upper()} ({framework_info['language']})")
    
    print(f"\n{ColorFormatter.info('💡 Total: {len(languages)} languages, {len(frameworks)} frameworks')}")


@cli.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for test results')
def test(output):
    """Run comprehensive tests on the detection engine"""
    print_banner()
    print(ColorFormatter.info("🧪 Running comprehensive tests..."))
    
    lexer = GuessLexer()
    
    # Test cases with expected results
    test_cases = [
        {
            "name": "Python function",
            "code": "def calculate_sum(a: int, b: int) -> int:\n    return a + b\n\nif __name__ == '__main__':\n    print(calculate_sum(5, 3))",
            "expected_language": "python",
            "filename": "test.py"
        },
        {
            "name": "JavaScript ES6",
            "code": "const greeting = (name) => {\n    console.log(`Hello, ${name}!`);\n};\n\ngreeting('World');",
            "expected_language": "javascript",
            "filename": "test.js"
        },
        {
            "name": "React Component",
            "code": "import React, { useState } from 'react';\n\nfunction Counter() {\n    const [count, setCount] = useState(0);\n    return <div onClick={() => setCount(count + 1)}>{count}</div>;\n}",
            "expected_language": "javascript",
            "expected_framework": "react",
            "filename": "Counter.jsx"
        },
        {
            "name": "TypeScript Interface",
            "code": "interface User {\n    id: number;\n    name: string;\n    email?: string;\n}\n\nfunction getUser(id: number): User {\n    return { id, name: 'John' };\n}",
            "expected_language": "typescript",
            "filename": "user.ts"
        },
        {
            "name": "Django Model",
            "code": "from django.db import models\nfrom django.contrib.auth.models import User\n\nclass Post(models.Model):\n    title = models.CharField(max_length=200)\n    author = models.ForeignKey(User, on_delete=models.CASCADE)\n    created_at = models.DateTimeField(auto_now_add=True)",
            "expected_language": "python",
            "expected_framework": "django",
            "filename": "models.py"
        },
        {
            "name": "Java Class",
            "code": "public class Calculator {\n    public static void main(String[] args) {\n        System.out.println(\"Hello World\");\n    }\n    \n    public int add(int a, int b) {\n        return a + b;\n    }\n}",
            "expected_language": "java",
            "filename": "Calculator.java"
        }
    ]
    
    results = []
    passed = 0
    total = len(test_cases)
    
    print(f"\n{ColorFormatter.header('🧪 RUNNING TESTS')}")
    print("="*60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        
        result = lexer.analyze_code(test_case['code'], test_case.get('filename'))
        
        # Check language
        language_correct = result.language == test_case['expected_language']
        
        # Check framework if expected
        framework_correct = True
        if 'expected_framework' in test_case:
            framework_correct = result.framework == test_case['expected_framework']
        
        test_passed = language_correct and framework_correct
        
        if test_passed:
            passed += 1
            print(f"   {ColorFormatter.success('✅ PASSED')} - {result.language}")
            if result.framework:
                print(f"      Framework: {result.framework}")
        else:
            print(f"   {ColorFormatter.error('❌ FAILED')}")
            print(f"      Expected: {test_case['expected_language']}")
            print(f"      Got: {result.language}")
            if 'expected_framework' in test_case:
                print(f"      Expected framework: {test_case['expected_framework']}")
                print(f"      Got framework: {result.framework}")
        
        print(f"      Confidence: {result.confidence:.1%}")
        
        # Store result
        results.append({
            "test_name": test_case['name'],
            "expected_language": test_case['expected_language'],
            "expected_framework": test_case.get('expected_framework'),
            "detected_language": result.language,
            "detected_framework": result.framework,
            "confidence": result.confidence,
            "passed": test_passed
        })
    
    # Summary
    print(f"\n{ColorFormatter.header('📊 TEST SUMMARY')}")
    print("="*40)
    print(f"Tests passed: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print(f"{ColorFormatter.success('🎉 All tests passed!')}")
    else:
        print(f"{ColorFormatter.warning(f'⚠️  {total-passed} tests failed')}")


if __name__ == "__main__":
    cli()
