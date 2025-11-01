# Code Analyzer

**Deep source code analysis and documentation tool for Python projects**

Code Analyzer is a comprehensive tool that reads source code, understands its structure, identifies critical sections, detects potential issues, and generates detailed documentation. It integrates with Logseq for documentation and repo-tickets for issue tracking.

## Features

### Core Analysis
- 🔍 **Deep Code Analysis**: AST-based parsing to understand code structure and dependencies
- 🎯 **Critical Section Identification**: Automatically identifies important code locations and critical paths
- 🐛 **Bug Detection**: Static analysis to find potential bugs, security issues, and code smells
- 📊 **VCS History Analysis**: Analyzes git history for hotspots, churn, and maintenance patterns
- 📈 **Trends Tracking**: SQLite database for tracking code quality over time
- 🔧 **Auto-Fix Generation**: Automatic fixes for common issues with confidence levels
- 🎫 **CI/CD Integration**: Generate GitHub Actions and GitLab CI workflows

### 🎉 **NEW in v0.5.0: World-Class Engineering Onboarding**

**Transform onboarding from days to hours** with comprehensive, actionable documentation:

1. **📝 Real Code Snippets** - Extract 10-20 line examples from key components
   - Multi-editor deep links (VS Code, IntelliJ, Neovim, Vim, Emacs, Sublime, Atom)
   - Actual implementation with full context and docstrings
   - Jump directly to code in your favorite editor

2. **🔄 Call Graph Visualization** - Understand how functions connect
   - ASCII call trees showing execution flow
   - Hot paths analysis (most-called functions)
   - System flow diagrams with module structure
   - Data transformation pipeline visualization

3. **🎯 "Why This Exists" Documentation** - Learn from git history
   - Mines commit messages for component rationale
   - Shows design decisions and evolution timeline
   - Identifies main contributors per component
   - Extracts "why" patterns from commit history

4. **🎨 Interactive Runnable Examples** - Copy-paste and run immediately
   - Smart parameter inference for realistic examples
   - Expected output shown for each example
   - Multiple use cases (classes, functions, workflows)
   - Copy-paste ready with zero configuration

5. **🔧 Common Developer Workflows** - Step-by-step guides
   - 6 complete workflows with time estimates (20-90 min each)
   - Add analyzers, create plugins, debug issues, contribute
   - Code examples with file locations
   - Pro tips and prerequisites for each workflow

**Result**: Engineers onboard in **<4 hours instead of days**! ✨

### Integration & Extensibility
- 🔌 **Plugin System**: Extensible architecture for custom analyzers and rules
- 📚 **Code Library**: Learn from classified code examples (excellent/good/smelly/bad patterns)
- 🔒 **Privacy-First**: Code anonymization for external LLM analysis while keeping sensitive code local
- 📝 **Logseq Integration**: Automatic documentation generation in your Logseq graph
- 🎫 **Ticket Management**: Auto-creates epics and prioritized tickets for discovered issues
- 🚫 **Non-Invasive**: Never modifies source code, stores all analysis in separate directory
- ⚡ **Fast & Efficient**: 28.5 files/sec, 10k+ lines/sec, < 10 MB memory

## Installation

```bash
cd /Volumes/Projects/code-analyzer
pip install -e .
```

## Quick Start

```bash
# Generate world-class onboarding documentation (NEW in v0.5.0!)
code-analyzer analyze /path/to/project --onboarding --output ./analysis

# Full analysis with all features
code-analyzer analyze /path/to/project \
  --depth deep \
  --onboarding \
  --auto-fix \
  --vcs-analysis \
  --track-trends \
  --generate-cicd github \
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

## Example Onboarding Output

Running onboarding on real projects generates comprehensive documentation:

| Project | Files | Lines | Onboarding Lines | Features |
|---------|-------|-------|-----------------|----------|
| code-analyzer | 31 | 10,147 | 869 | ✅ All 5 |
| python-optimizer | 71 | 23,894 | 1,153 | ✅ All 5 |
| agentscript | 58 | ~15K | 1,099 | ✅ All 5 |
| OrbisTertius | 53 | ~18K | 1,185 | ✅ All 5 |
| logseq-python | 75 | ~25K | 1,274 | ✅ All 5 |

**Each includes**: Real code snippets, call graphs, git history, interactive examples, and step-by-step workflows.

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
