"""
Powerful Code Language and Framework Detection Engine
Created for Danis - A comprehensive lexical analysis system
"""

import re
import os
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict, Counter
import mimetypes


@dataclass
class DetectionResult:
    """Result of language/framework detection"""
    language: str
    confidence: float
    framework: Optional[str] = None
    evidence: List[str] = None
    
    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []


class GuessLexer:
    """
    Advanced code language and framework detection engine
    Uses multiple analysis techniques for accurate detection
    """
    
    def __init__(self):
        self.language_patterns: Dict[str, Dict[str, Any]] = self._initialize_patterns()
        self.framework_patterns: Dict[str, Dict[str, Any]] = self._initialize_framework_patterns()
        self.file_extensions: Dict[str, List[str]] = self._initialize_extensions()
        
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize language detection patterns"""
        return {
            'python': {
                'keywords': ['def', 'class', 'import', 'from', 'if __name__', 'elif', 'lambda', 'yield'],
                'patterns': [
                    r'^\s*def\s+\w+\s*\(',
                    r'^\s*class\s+\w+',
                    r'^\s*import\s+\w+',
                    r'^\s*from\s+\w+\s+import',
                    r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',
                    r'^\s*#.*python',
                    r'print\s*\(',
                    r'^\s*@\w+',  # decorators
                ],
                'anti_patterns': [r'console\.log', r'function\s*\(', r'var\s+\w+'],
                'weight': 1.0
            },
            'javascript': {
                'keywords': ['function', 'var', 'let', 'const', 'console.log', 'require', 'module.exports'],
                'patterns': [
                    r'function\s+\w+\s*\(',
                    r'console\.log\s*\(',
                    r'var\s+\w+\s*=',
                    r'let\s+\w+\s*=',
                    r'const\s+\w+\s*=',
                    r'require\s*\([\'"]',
                    r'module\.exports',
                    r'=>',  # arrow functions
                    r'\.then\s*\(',
                    r'async\s+function',
                ],
                'anti_patterns': [r'def\s+\w+', r'class\s+\w+.*:', r'import\s+\w+'],
                'weight': 1.0
            },
            'typescript': {
                'keywords': ['interface', 'type', 'enum', 'namespace', 'declare'],
                'patterns': [
                    r'interface\s+\w+',
                    r'type\s+\w+\s*=',
                    r'enum\s+\w+',
                    r':\s*\w+(\[\])?(\s*\|\s*\w+)*\s*[=;]',  # type annotations
                    r'<\w+>',  # generics
                    r'declare\s+',
                    r'namespace\s+\w+',
                ],
                'anti_patterns': [],
                'weight': 1.2
            },
            'java': {
                'keywords': ['public class', 'private', 'protected', 'static', 'void', 'import java'],
                'patterns': [
                    r'public\s+class\s+\w+',
                    r'private\s+\w+\s+\w+',
                    r'protected\s+\w+\s+\w+',
                    r'public\s+static\s+void\s+main',
                    r'import\s+java\.',
                    r'@\w+\s*\n\s*public',  # annotations
                    r'System\.out\.println',
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+'],
                'weight': 1.0
            },
            'csharp': {
                'keywords': ['using', 'namespace', 'class', 'static void Main', 'public', 'private'],
                'patterns': [
                    r'using\s+\w+;',
                    r'namespace\s+\w+',
                    r'public\s+class\s+\w+',
                    r'static\s+void\s+Main',
                    r'Console\.WriteLine',
                    r'\[assembly:',
                    r'#region',
                ],
                'anti_patterns': [r'import\s+', r'def\s+\w+'],
                'weight': 1.0
            },
            'cpp': {
                'keywords': ['#include', 'using namespace', 'int main', 'std::', 'class'],
                'patterns': [
                    r'#include\s*<\w+>',
                    r'using\s+namespace\s+std',
                    r'int\s+main\s*\(',
                    r'std::\w+',
                    r'cout\s*<<',
                    r'cin\s*>>',
                    r'class\s+\w+\s*{',
                ],
                'anti_patterns': [r'def\s+\w+', r'import\s+'],
                'weight': 1.0
            },
            'c': {
                'keywords': ['#include', 'int main', 'printf', 'scanf', 'malloc'],
                'patterns': [
                    r'#include\s*<\w+\.h>',
                    r'int\s+main\s*\(',
                    r'printf\s*\(',
                    r'scanf\s*\(',
                    r'malloc\s*\(',
                    r'free\s*\(',
                ],
                'anti_patterns': [r'class\s+\w+', r'using\s+namespace', r'def\s+\w+'],
                'weight': 1.0
            },
            'go': {
                'keywords': ['package', 'import', 'func', 'var', 'const', 'type'],
                'patterns': [
                    r'package\s+\w+',
                    r'import\s*\(',
                    r'func\s+\w+\s*\(',
                    r'func\s+main\s*\(\s*\)',
                    r'fmt\.Print',
                    r':=',  # short variable declaration
                    r'go\s+\w+\(',  # goroutines
                ],
                'anti_patterns': [r'def\s+\w+', r'class\s+\w+'],
                'weight': 1.0
            },
            'rust': {
                'keywords': ['fn', 'let', 'mut', 'impl', 'trait', 'use'],
                'patterns': [
                    r'fn\s+\w+\s*\(',
                    r'let\s+\w+\s*=',
                    r'let\s+mut\s+\w+',
                    r'impl\s+\w+',
                    r'trait\s+\w+',
                    r'use\s+\w+::',
                    r'println!\s*\(',
                    r'#\[derive\(',
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+', r'import\s+[\'"]package:', r'class\s+\w+\s+extends', r'StatelessWidget', r'StatefulWidget'],
                'weight': 1.0
            },
            'ruby': {
                'keywords': ['def', 'class', 'end', 'require', 'puts', 'attr_accessor'],
                'patterns': [
                    r'def\s+\w+',
                    r'class\s+\w+',
                    r'end\s*$',
                    r'require\s+[\'"]',
                    r'puts\s+',
                    r'attr_accessor\s+',
                    r'@\w+',  # instance variables
                    r'=>\s*',  # hash syntax
                ],
                'anti_patterns': [r'def\s+\w+\s*\(.*\):', r'import\s+'],
                'weight': 1.0
            },
            'php': {
                'keywords': ['<?php', 'function', 'class', 'echo', '$', 'require_once'],
                'patterns': [
                    r'<\?php',
                    r'function\s+\w+\s*\(',
                    r'class\s+\w+',
                    r'echo\s+',
                    r'\$\w+',  # variables
                    r'require_once\s+',
                    r'->\w+',  # object properties
                    r'public\s+function',
                ],
                'anti_patterns': [r'def\s+\w+', r'import\s+'],
                'weight': 1.0
            },
            'swift': {
                'keywords': ['func', 'var', 'let', 'import', 'class', 'struct'],
                'patterns': [
                    r'func\s+\w+\s*\(',
                    r'var\s+\w+\s*:',
                    r'let\s+\w+\s*=',
                    r'import\s+\w+',
                    r'class\s+\w+\s*:',
                    r'struct\s+\w+',
                    r'print\s*\(',
                    r'@\w+\s*\n',  # attributes
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+', r'import\s+[\'"]package:', r'StatelessWidget', r'StatefulWidget'],
                'weight': 1.0
            },
            'kotlin': {
                'keywords': ['fun', 'val', 'var', 'class', 'object', 'package'],
                'patterns': [
                    r'fun\s+\w+\s*\(',
                    r'val\s+\w+\s*=',
                    r'var\s+\w+\s*=',
                    r'class\s+\w+',
                    r'object\s+\w+',
                    r'package\s+\w+',
                    r'println\s*\(',
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+', r'import\s+[\'"]package:', r'StatelessWidget', r'StatefulWidget'],
                'weight': 1.0
            },
            'sql': {
                'keywords': ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE'],
                'patterns': [
                    r'SELECT\s+.*FROM',
                    r'INSERT\s+INTO',
                    r'UPDATE\s+\w+\s+SET',
                    r'DELETE\s+FROM',
                    r'CREATE\s+TABLE',
                    r'ALTER\s+TABLE',
                    r'DROP\s+TABLE',
                    r'WHERE\s+\w+\s*=',
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+', r'class\s+\w+'],
                'weight': 1.0
            },
            'html': {
                'keywords': ['<html>', '<head>', '<body>', '<div>', '<script>'],
                'patterns': [
                    r'<!DOCTYPE\s+html>',
                    r'<html.*>',
                    r'<head>',
                    r'<body.*>',
                    r'<div.*>',
                    r'<script.*>',
                    r'<link\s+.*rel=',
                    r'<meta\s+.*>',
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+(?!\s*\()'],
                'weight': 1.0
            },
            'css': {
                'keywords': ['{', '}', ':', ';', '@media', '@import'],
                'patterns': [
                    r'\w+\s*\{[^}]*\}',
                    r'@media\s*\(',
                    r'@import\s+',
                    r'#\w+\s*\{',  # id selectors
                    r'\.\w+\s*\{',  # class selectors
                    r':\w+\s*\{',  # pseudo selectors
                    r'\w+:\s*\w+;',  # property declarations
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+', r'class\s+\w+(?!\s*\{)'],
                'weight': 1.0
            },
            'dart': {
                'keywords': ['void', 'main', 'class', 'import', 'library', 'part', 'abstract', 'extends', 'implements'],
                'patterns': [
                    r'void\s+main\s*\(\s*\)',  # main function
                    r'import\s+[\'"]package:',  # package imports
                    r'import\s+[\'"]dart:',  # dart core imports
                    r'class\s+\w+\s+extends\s+\w+',  # class inheritance
                    r'class\s+\w+\s+implements\s+\w+',  # interface implementation
                    r'abstract\s+class\s+\w+',  # abstract classes
                    r'library\s+\w+;',  # library declaration
                    r'part\s+of\s+\w+;',  # part of library
                    r'part\s+[\'"][^\'\"]+\.dart[\'"];',  # part files
                    r'@override',  # override annotation
                    r'final\s+\w+',  # final variables
                    r'const\s+\w+',  # const variables
                    r'var\s+\w+\s*=',  # var declarations
                    r'\w+\?\s+\w+',  # nullable types
                    r'\w+<\w+>',  # generics
                    r'List<\w+>',  # List types
                    r'Map<\w+,\s*\w+>',  # Map types
                    r'Set<\w+>',  # Set types
                    r'Future<\w+>',  # Future types
                    r'Stream<\w+>',  # Stream types
                    r'async\s*\{',  # async functions
                    r'await\s+\w+',  # await keyword
                    r'=>\s*\w+',  # arrow functions
                    r'print\s*\(',  # print function
                ],
                'anti_patterns': [r'def\s+\w+', r'function\s+\w+', r'console\.log', r'System\.out\.println'],
                'weight': 1.0
            }
        }
    
    def _initialize_framework_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize framework detection patterns"""
        return {
            'react': {
                'language': 'javascript',
                'patterns': [
                    r'import\s+.*from\s+[\'"]react[\'"]',
                    r'React\.Component',
                    r'useState\s*\(',
                    r'useEffect\s*\(',
                    r'jsx',
                    r'className=',
                    r'<\w+.*>.*</\w+>',  # JSX tags
                    r'return\s*\(',
                ],
                'keywords': ['React', 'useState', 'useEffect', 'Component', 'jsx'],
                'weight': 1.2
            },
            'vue': {
                'language': 'javascript',
                'patterns': [
                    r'import\s+.*from\s+[\'"]vue[\'"]',
                    r'Vue\.component',
                    r'<template>',
                    r'<script>',
                    r'v-if=',
                    r'v-for=',
                    r'@click=',
                ],
                'keywords': ['Vue', 'template', 'v-if', 'v-for'],
                'weight': 1.2
            },
            'angular': {
                'language': 'typescript',
                'patterns': [
                    r'import\s+.*from\s+[\'"]@angular',
                    r'@Component\s*\(',
                    r'@Injectable\s*\(',
                    r'@NgModule\s*\(',
                    r'selector:\s*[\'"]',
                    r'templateUrl:\s*[\'"]',
                ],
                'keywords': ['@Component', '@Injectable', '@NgModule', 'Angular'],
                'weight': 1.2
            },
            'django': {
                'language': 'python',
                'patterns': [
                    r'from\s+django',
                    r'import\s+django',
                    r'models\.Model',
                    r'HttpResponse',
                    r'render\s*\(',
                    r'urlpatterns\s*=',
                    r'@login_required',
                ],
                'keywords': ['django', 'models', 'HttpResponse', 'urlpatterns'],
                'weight': 1.2
            },
            'flask': {
                'language': 'python',
                'patterns': [
                    r'from\s+flask',
                    r'import\s+flask',
                    r'Flask\s*\(',
                    r'@app\.route',
                    r'render_template\s*\(',
                    r'request\.form',
                ],
                'keywords': ['Flask', '@app.route', 'render_template'],
                'weight': 1.2
            },
            'fastapi': {
                'language': 'python',
                'patterns': [
                    r'from\s+fastapi',
                    r'import\s+fastapi',
                    r'FastAPI\s*\(',
                    r'@app\.(get|post|put|delete)',
                    r'Pydantic',
                    r'BaseModel',
                ],
                'keywords': ['FastAPI', 'Pydantic', 'BaseModel'],
                'weight': 1.2
            },
            'express': {
                'language': 'javascript',
                'patterns': [
                    r'require\s*\([\'"]express[\'"]',
                    r'import\s+.*from\s+[\'"]express[\'"]',
                    r'app\.get\s*\(',
                    r'app\.post\s*\(',
                    r'app\.listen\s*\(',
                    r'express\s*\(\s*\)',
                ],
                'keywords': ['express', 'app.get', 'app.post', 'app.listen'],
                'weight': 1.2
            },
            'spring': {
                'language': 'java',
                'patterns': [
                    r'import\s+org\.springframework',
                    r'@RestController',
                    r'@Service',
                    r'@Repository',
                    r'@Autowired',
                    r'@RequestMapping',
                    r'@GetMapping',
                ],
                'keywords': ['@RestController', '@Service', '@Autowired', 'springframework'],
                'weight': 1.2
            },
            'flutter': {
                'language': 'dart',
                'patterns': [
                    r'import\s+[\'"]package:flutter/',  # Flutter package imports
                    r'import\s+[\'"]package:flutter/material\.dart[\'"]',  # Material design
                    r'import\s+[\'"]package:flutter/cupertino\.dart[\'"]',  # Cupertino design
                    r'import\s+[\'"]package:flutter/widgets\.dart[\'"]',  # Base widgets
                    r'class\s+\w+\s+extends\s+StatelessWidget',  # StatelessWidget
                    r'class\s+\w+\s+extends\s+StatefulWidget',  # StatefulWidget
                    r'class\s+\w+\s+extends\s+State<\w+>',  # State class
                    r'Widget\s+build\s*\(',  # build method
                    r'@override\s+Widget\s+build',  # override build
                    r'MaterialApp\s*\(',  # MaterialApp
                    r'CupertinoApp\s*\(',  # CupertinoApp
                    r'Scaffold\s*\(',  # Scaffold widget
                    r'AppBar\s*\(',  # AppBar widget
                    r'Container\s*\(',  # Container widget
                    r'Column\s*\(',  # Column widget
                    r'Row\s*\(',  # Row widget
                    r'Text\s*\(',  # Text widget
                    r'RaisedButton\s*\(',  # RaisedButton (deprecated)
                    r'ElevatedButton\s*\(',  # ElevatedButton
                    r'TextButton\s*\(',  # TextButton
                    r'OutlinedButton\s*\(',  # OutlinedButton
                    r'FloatingActionButton\s*\(',  # FloatingActionButton
                    r'ListView\s*\(',  # ListView widget
                    r'GridView\s*\(',  # GridView widget
                    r'Stack\s*\(',  # Stack widget
                    r'Positioned\s*\(',  # Positioned widget
                    r'Padding\s*\(',  # Padding widget
                    r'Margin\s*\(',  # Margin widget
                    r'SizedBox\s*\(',  # SizedBox widget
                    r'Expanded\s*\(',  # Expanded widget
                    r'Flexible\s*\(',  # Flexible widget
                    r'Navigator\.\w+',  # Navigator methods
                    r'setState\s*\(',  # setState method
                    r'initState\s*\(',  # initState method
                    r'dispose\s*\(',  # dispose method
                    r'didChangeDependencies\s*\(',  # lifecycle method
                    r'runApp\s*\(',  # runApp function
                    r'MaterialPageRoute\s*\(',  # MaterialPageRoute
                    r'CupertinoPageRoute\s*\(',  # CupertinoPageRoute
                    r'Theme\.\w+',  # Theme usage
                    r'MediaQuery\.\w+',  # MediaQuery usage
                    r'ValueNotifier<\w+>',  # ValueNotifier
                    r'ValueListenableBuilder<\w+>',  # ValueListenableBuilder
                    r'StreamBuilder<\w+>',  # StreamBuilder
                    r'FutureBuilder<\w+>',  # FutureBuilder
                    r'AnimationController\s*\(',  # AnimationController
                    r'SingleTickerProviderStateMixin',  # Animation mixin
                    r'TickerProviderStateMixin',  # Animation mixin
                    r'GestureDetector\s*\(',  # GestureDetector
                    r'InkWell\s*\(',  # InkWell
                    r'onTap:\s*\(',  # onTap callback
                    r'onPressed:\s*\(',  # onPressed callback
                    r'CrossAxisAlignment\.\w+',  # CrossAxisAlignment
                    r'MainAxisAlignment\.\w+',  # MainAxisAlignment
                    r'TextAlign\.\w+',  # TextAlign
                    r'FontWeight\.\w+',  # FontWeight
                    r'Colors\.\w+',  # Colors
                    r'Icons\.\w+',  # Icons
                    r'EdgeInsets\.\w+',  # EdgeInsets
                    r'BorderRadius\.\w+',  # BorderRadius
                    r'Decoration\s*\(',  # BoxDecoration
                    r'BoxDecoration\s*\(',  # BoxDecoration
                ],
                'keywords': [
                    'Flutter', 'StatelessWidget', 'StatefulWidget', 'Widget', 'build',
                    'MaterialApp', 'CupertinoApp', 'Scaffold', 'AppBar', 'Container',
                    'Column', 'Row', 'Text', 'ElevatedButton', 'FloatingActionButton',
                    'ListView', 'GridView', 'Stack', 'Positioned', 'Navigator',
                    'setState', 'initState', 'dispose', 'runApp', 'Theme', 'MediaQuery',
                    'StreamBuilder', 'FutureBuilder', 'AnimationController', 'GestureDetector',
                    'CrossAxisAlignment', 'MainAxisAlignment', 'Colors', 'Icons'
                ],
                'weight': 1.3
            }
        }
    
    def _initialize_extensions(self) -> Dict[str, List[str]]:
        """Initialize file extension mappings"""
        return {
            'python': ['.py', '.pyw', '.pyx'],
            'javascript': ['.js', '.mjs', '.cjs'],
            'typescript': ['.ts', '.tsx'],
            'java': ['.java'],
            'csharp': ['.cs'],
            'cpp': ['.cpp', '.cxx', '.cc', '.c++'],
            'c': ['.c', '.h'],
            'go': ['.go'],
            'rust': ['.rs'],
            'ruby': ['.rb'],
            'php': ['.php'],
            'swift': ['.swift'],
            'kotlin': ['.kt', '.kts'],
            'sql': ['.sql'],
            'html': ['.html', '.htm'],
            'css': ['.css'],
            'dart': ['.dart']
        }
    
    def analyze_code(self, code: str, filename: Optional[str] = None) -> DetectionResult:
        """
        Analyze code and detect language/framework
        
        Args:
            code: The source code to analyze
            filename: Optional filename for extension-based hints
            
        Returns:
            DetectionResult with language, confidence, framework, and evidence
        """
        if not code.strip():
            return DetectionResult("unknown", 0.0, evidence=["Empty code"])
        
        # Get extension hint if filename provided
        extension_hint: Optional[str] = None
        if filename:
            extension_hint = self._get_extension_hint(filename)
        
        # Analyze languages
        language_scores: Dict[str, float] = {}
        language_evidence: Dict[str, List[str]] = defaultdict(list)
        
        for lang, patterns in self.language_patterns.items():
            score, evidence = self._score_language(code, lang, patterns)
            if score > 0:
                language_scores[lang] = score
                language_evidence[lang] = evidence
        
        # Apply extension hint bonus
        if extension_hint and extension_hint in language_scores:
            language_scores[extension_hint] *= 1.5
            language_evidence[extension_hint].append(f"File extension hint: {filename}")
        
        # Find best language
        if not language_scores:
            return DetectionResult("unknown", 0.0, evidence=["No patterns matched"])
        
        best_language: str = max(language_scores.keys(), key=lambda x: language_scores[x])
        confidence: float = min(language_scores[best_language], 1.0)
        
        # Analyze frameworks for the detected language
        framework_result: Optional[Tuple[str, float, List[str]]] = self._detect_framework(
            code, best_language
        )
        
        framework: Optional[str] = None
        framework_evidence: List[str] = []
        if framework_result:
            framework, framework_confidence, framework_evidence = framework_result
            confidence = min(confidence + framework_confidence * 0.3, 1.0)
        
        # Combine evidence
        all_evidence: List[str] = language_evidence[best_language] + framework_evidence
        
        return DetectionResult(
            language=best_language,
            confidence=confidence,
            framework=framework,
            evidence=all_evidence
        )
    
    def _get_extension_hint(self, filename: str) -> Optional[str]:
        """Get language hint from file extension"""
        _, ext = os.path.splitext(filename.lower())
        for lang, extensions in self.file_extensions.items():
            if ext in extensions:
                return lang
        return None
    
    def _score_language(self, code: str, language: str, patterns: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Score how well code matches a language"""
        score: float = 0.0
        evidence: List[str] = []
        
        # Check patterns
        pattern_matches: int = 0
        for pattern in patterns['patterns']:
            matches = re.findall(pattern, code, re.MULTILINE | re.IGNORECASE)
            if matches:
                pattern_matches += len(matches)
                evidence.append(f"Pattern match: {pattern} ({len(matches)} times)")
        
        # Check keywords
        keyword_matches: int = 0
        for keyword in patterns['keywords']:
            if keyword.lower() in code.lower():
                keyword_matches += 1
                evidence.append(f"Keyword found: {keyword}")
        
        # Check anti-patterns (negative scoring)
        anti_pattern_matches: int = 0
        for anti_pattern in patterns.get('anti_patterns', []):
            matches = re.findall(anti_pattern, code, re.MULTILINE | re.IGNORECASE)
            if matches:
                anti_pattern_matches += len(matches)
                evidence.append(f"Anti-pattern found: {anti_pattern} (-{len(matches)})")
        
        # Calculate score
        base_score: float = (pattern_matches * 0.6 + keyword_matches * 0.4) * patterns['weight']
        penalty: float = anti_pattern_matches * 0.3
        score = max(0, base_score - penalty)
        
        return score, evidence
    
    def _detect_framework(self, code: str, language: str) -> Optional[Tuple[str, float, List[str]]]:
        """Detect framework within detected language"""
        framework_scores: Dict[str, float] = {}
        framework_evidence: Dict[str, List[str]] = defaultdict(list)
        
        for framework, patterns in self.framework_patterns.items():
            if patterns['language'] != language:
                continue
                
            pattern_matches: int = 0
            evidence: List[str] = []
            
            # Check patterns
            for pattern in patterns['patterns']:
                matches = re.findall(pattern, code, re.MULTILINE | re.IGNORECASE)
                if matches:
                    pattern_matches += len(matches)
                    evidence.append(f"Framework pattern: {pattern}")
            
            # Check keywords
            keyword_matches: int = 0
            for keyword in patterns['keywords']:
                if keyword.lower() in code.lower():
                    keyword_matches += 1
                    evidence.append(f"Framework keyword: {keyword}")
            
            if pattern_matches > 0 or keyword_matches > 0:
                score = (pattern_matches * 0.7 + keyword_matches * 0.3) * patterns['weight']
                framework_scores[framework] = score
                framework_evidence[framework] = evidence
        
        if not framework_scores:
            return None
            
        best_framework: str = max(framework_scores.keys(), key=lambda x: framework_scores[x])
        confidence: float = min(framework_scores[best_framework] / 5.0, 1.0)  # Normalize
        
        return best_framework, confidence, framework_evidence[best_framework]
    
    def analyze_file(self, filepath: str) -> DetectionResult:
        """
        Analyze a file and detect its language/framework
        
        Args:
            filepath: Path to the file to analyze
            
        Returns:
            DetectionResult with detection information
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.analyze_code(code, os.path.basename(filepath))
        except Exception as e:
            return DetectionResult("unknown", 0.0, evidence=[f"Error reading file: {str(e)}"])
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.language_patterns.keys())
    
    def get_supported_frameworks(self) -> List[str]:
        """Get list of supported frameworks"""
        return list(self.framework_patterns.keys())


def format_result(result: DetectionResult) -> str:
    """Format detection result for display"""
    output: List[str] = []
    output.append(f"🔍 Language: {result.language.upper()}")
    output.append(f"📊 Confidence: {result.confidence:.1%}")
    
    if result.framework:
        output.append(f"🚀 Framework: {result.framework.upper()}")
    
    if result.evidence:
        output.append("\n📝 Evidence:")
        for evidence in result.evidence[:10]:  # Limit to top 10 evidence items
            output.append(f"  • {evidence}")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Example usage
    lexer = GuessLexer()
    
    # Test with some sample code
    test_codes = [
        ("def hello_world():\n    print('Hello, World!')", "sample.py"),
        ("function hello() {\n    console.log('Hello!');\n}", "sample.js"),
        ("import React from 'react';\nfunction App() {\n    return <div>Hello</div>;\n}", "App.jsx"),
    ]
    
    print("🎯 Danis's Powerful Guess Lexer Engine - Test Results\n")
    print("=" * 60)
    
    for code, filename in test_codes:
        print(f"\n📄 Analyzing: {filename}")
        print("-" * 40)
        result = lexer.analyze_code(code, filename)
        print(format_result(result))
        print()
