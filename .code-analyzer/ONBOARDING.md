================================================================================
ONBOARDING GUIDE: code-analyzer
================================================================================

📋 PROJECT OVERVIEW
--------------------------------------------------------------------------------
Complexity: Complex
Size: 26 files, 8,229 lines

Technologies:
  • Click (CLI framework)
  • pytest (testing)

Key Dependencies:
  • code_analyzer
  • rich
  • radon
  • inspect
  • json

🗺️  LEARNING PATH
--------------------------------------------------------------------------------
1. Start with README.md to understand the project's purpose
2. Read entry points to see how the application starts:
   - benchmark.py
   - code_analyzer/cli.py
   - examples/test_plugins.py
3. Study core modules to understand main functionality:
   - code_analyzer/analyzer.py (Analysis and processing)
   - code_analyzer/anonymizer.py (Analysis and processing)
   - code_analyzer/autofix.py (Analysis and processing)
   - code_analyzer/cli.py (Analysis and processing)
   - code_analyzer/code_library.py (Analysis and processing)
5. Read tests to understand expected behavior

🔑 KEY CONCEPTS
--------------------------------------------------------------------------------
Architecture: Command-Line Application

Main Classes (Top 5):
  • code_analyzer.anonymizer.CodeAnonymizer: Anonymizes code for external LLM analysis while preserving structure.
  • code_analyzer.analyzer.CodeAnalyzer: Main code analyzer that parses and analyzes Python code.
  • code_analyzer.important_sections.ImportantSectionIdentifier: Identifies important sections and patterns in code.
  • code_analyzer.improvement_detector.ImprovementDetector: Detects code that needs updates and improvements.
  • code_analyzer.autofix.AutoFixGenerator: Generate automatic fixes for common code issues.

🚀 QUICK START TIPS
--------------------------------------------------------------------------------
1. Install dependencies first - check setup.py or requirements.txt
2. Run tests to verify setup: pytest or python -m pytest
3. Try CLI commands with --help to explore functionality
4. Check examples/ directory for usage demonstrations
5. Start by reading docstrings in main classes and functions
6. Use an IDE with 'go to definition' to navigate the codebase

⚠️  COMMON PITFALLS
--------------------------------------------------------------------------------
  ⚠️  20 modules have high complexity - start with simpler ones
  ⚠️  Many dependencies - make sure you understand the core ones first

💻 HELPFUL COMMANDS
--------------------------------------------------------------------------------
  tree -L 2
    → View project structure

  find . -name '*.py' | wc -l
    → Count Python files

  grep -r 'class ' --include='*.py' | wc -l
    → Count classes

  pytest -v
    → Run tests with verbose output

  pytest --cov
    → Run tests with coverage

  python -m code_analyzer/cli --help
    → View CLI help

  pylint *.py
    → Check code quality

  radon cc . -a
    → Calculate cyclomatic complexity

  pydoc <module>
    → View module documentation

================================================================================
Good luck! 🎉
================================================================================