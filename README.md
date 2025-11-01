# Code Analyzer

**Deep source code analysis and documentation tool for Python projects**

Code Analyzer is a comprehensive tool that reads source code, understands its structure, identifies critical sections, detects potential issues, and generates detailed documentation. It integrates with Logseq for documentation and repo-tickets for issue tracking.

## Features

- 🔍 **Deep Code Analysis**: AST-based parsing to understand code structure and dependencies
- 🎯 **Critical Section Identification**: Automatically identifies important code locations and critical paths
- 🐛 **Bug Detection**: Static analysis to find potential bugs, security issues, and code smells
- 🔌 **Plugin System**: Extensible architecture for custom analyzers and rules
- 📚 **Code Library**: Learn from classified code examples (excellent/good/smelly/bad patterns)
- 🔒 **Privacy-First**: Code anonymization for external LLM analysis while keeping sensitive code local
- 📝 **Logseq Integration**: Automatic documentation generation in your Logseq graph
- 🎫 **Ticket Management**: Auto-creates epics and prioritized tickets for discovered issues
- 📊 **Comprehensive Reports**: Detailed analysis reports with metrics and insights
- 🚫 **Non-Invasive**: Never modifies source code, stores all analysis in separate directory
- ⚡ **Fast & Efficient**: 28.5 files/sec, 10k+ lines/sec, < 10 MB memory

## Installation

```bash
cd /Volumes/Projects/code-analyzer
pip install -e .
```

## Quick Start

```bash
# Analyze a Python project
code-analyzer analyze /path/to/project --depth deep

# Deep analysis with all features
code-analyzer analyze /path/to/project \
  --depth deep \
  --create-tickets \
  --generate-docs \
  --logseq-graph ~/logseq

# Use custom plugins and code library
code-analyzer analyze /path/to/project \
  --plugins ./my-plugins \
  --code-library ./team-code-library.yaml

# Use built-in default code library
code-analyzer analyze /path/to/project --use-default-library

# Anonymize code for external analysis
code-analyzer anonymize /path/to/project --output /tmp/anonymized
```

## Configuration

Create `.code-analyzer.yaml` in your project root:

```yaml
analysis:
  depth: deep  # shallow, medium, deep
  include_tests: true
  ignore_patterns:
    - "*/migrations/*"
    - "*/build/*"

plugins:
  directory: "./code-analyzer-plugins"

code_library:
  path: "./team-code-library.yaml"
  # OR use built-in examples:
  # use_default: true

documentation:
  logseq_graph: ~/logseq
  create_index: true
  
tickets:
  enabled: true
  auto_prioritize: true
  create_epics: true

privacy:
  anonymize_for_llm: true
  keep_structure: true
```

## How It Works

1. **Parse**: Analyzes Python code using AST and static analysis
2. **Identify**: Finds critical sections, entry points, and dependencies
3. **Detect**: Discovers bugs, security issues, and code smells
4. **Document**: Generates comprehensive Logseq documentation
5. **Track**: Creates prioritized tickets for issues in repo-tickets
6. **Report**: Produces detailed analysis reports

All analysis data is stored in `.code-analyzer/` directory, never modifying source code.

## Extensibility

### Plugin System

Create custom analyzers to enforce team-specific rules:

```python
from code_analyzer.plugins import CustomRulePlugin
from code_analyzer.models import IssueSeverity

class MyTeamRules(CustomRulePlugin):
    @property
    def name(self) -> str:
        return "my-team-rules"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.add_rule(
            name="no-print-statements",
            check=lambda obj: 'print(' in str(obj.source_code),
            severity=IssueSeverity.LOW,
            message="Use logging instead of print",
            recommendation="Import logging and use logger.info()"
        )
```

See [docs/PLUGINS.md](docs/PLUGINS.md) for complete guide.

### Code Library

Build a library of code patterns classified by quality:

```yaml
examples:
  - id: "eval-bad-001"
    classification: bad
    pattern_type: security
    language: python
    reason: "Arbitrary code execution vulnerability"
    code: |
      result = eval(user_input)
    alternative: "Use ast.literal_eval() for safe evaluation"
```

The analyzer will match your code against the library and flag bad/smelly patterns.

## Performance

Benchmarked on 4 real-world Python projects (176 files, 62,814 lines):

- **Throughput**: 28.5 files/sec, 10,182 lines/sec
- **Memory**: 7.6 MB average, < 20 MB peak
- **Speed**: 0.5-3.5s for typical projects
- **Scaling**: Linear growth, handles 70+ files easily

Suitable for:
- ✅ Interactive CLI usage
- ✅ Pre-commit hooks (< 5s)
- ✅ CI/CD pipelines
- ✅ IDE integration

See [docs/PERFORMANCE.md](docs/PERFORMANCE.md) for detailed benchmarks.

## Integration

- **logseq-python**: Documentation generation in Logseq format
- **repo-tickets**: Epic and ticket management for discovered issues
- **Plugins**: Custom analyzers and rules
- **Code Library**: Pattern matching against classified examples
- **Local Analysis**: Most analysis runs locally for privacy
- **LLM Support**: Optional anonymized code analysis for complex patterns

## License

MIT License
