# New Features: Plugin System & Code Library

## Overview

Two major extensibility features have been added to code-analyzer:

1. **Plugin System** - Create custom analyzers to add your own rules and checks
2. **Code Library** - Build a library of classified code examples for pattern matching

---

## 1. Plugin System

### What It Does

Allows you to extend the analyzer with custom logic without modifying the core codebase.

### Key Features

- **Easy to Create**: Simple base classes (`AnalyzerPlugin`, `CustomRulePlugin`)
- **Hooks**: Run code at different analysis stages (pre/post analysis)
- **Auto-Loading**: Drop Python files in a directory, they're automatically loaded
- **Custom Findings**: Generate your own metrics and reports
- **Built-in Examples**: Includes naming conventions and logging best practices plugins

### Files Added

- `code_analyzer/plugins.py` (315 lines) - Plugin system implementation
- `examples/example_plugin.py` (233 lines) - Example plugins for users
- `docs/PLUGINS.md` (503 lines) - Complete plugin documentation

### Usage

```bash
# Command line
code-analyzer analyze ./project --plugins ./my-plugins

# Configuration
plugins:
  directory: "./my-plugins"
```

### Example Plugin

```python
from code_analyzer.plugins import CustomRulePlugin
from code_analyzer.models import IssueSeverity

class MyRules(CustomRulePlugin):
    @property
    def name(self): return "my-rules"
    
    @property
    def version(self): return "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.add_rule(
            name="no-todos",
            check=lambda obj: 'TODO' in str(obj.source_code),
            severity=IssueSeverity.LOW,
            message="TODO comment found",
            recommendation="Track as ticket"
        )
```

---

## 2. Code Library System

### What It Does

Allows you to classify code examples as excellent/good/smelly/bad and automatically match them against analyzed code.

### Key Features

- **4 Quality Levels**: excellent, good, smelly, bad
- **Pattern Types**: security, error_handling, structure, design patterns, etc.
- **Smart Matching**: Uses AST structure + text + token similarity
- **Issue Generation**: Automatically creates issues for bad/smelly pattern matches
- **Quality Scoring**: Generates quality metrics based on matches
- **Default Library**: Includes 5 built-in examples to start with

### Files Added

- `code_analyzer/code_library.py` (449 lines) - Code library implementation
- `examples/example_code_library.yaml` (321 lines) - Example library with 15+ patterns

### Usage

```bash
# Command line - custom library
code-analyzer analyze ./project --code-library ./team-library.yaml

# Command line - use defaults
code-analyzer analyze ./project --use-default-library

# Configuration
code_library:
  path: "./team-library.yaml"
  # OR
  use_default: true
```

### Example Library Entry

```yaml
- id: "eval-bad-001"
  classification: bad
  pattern_type: security
  language: python
  description: "Using eval() on user input"
  reason: "Arbitrary code execution vulnerability"
  code: |
    result = eval(user_input)
  alternative: "Use ast.literal_eval() for safe evaluation"
  tags: [security, injection]
```

When the analyzer finds code similar to this, it automatically creates a HIGH severity issue.

---

## Integration with Existing Features

### Analyzer Changes

The main `CodeAnalyzer` class now:
- Accepts `plugin_dir` and `code_library_path` parameters
- Loads plugins on initialization
- Runs plugin hooks at key stages
- Runs pattern matching against code library
- Includes plugin issues and library issues in final results

### CLI Changes

New options added to `analyze` command:
- `--plugins PATH` - Directory containing plugins
- `--code-library PATH` - Path to code library YAML
- `--use-default-library` - Use built-in default library

### Configuration Changes

New sections in `.code-analyzer.yaml`:
```yaml
plugins:
  directory: "./code-analyzer-plugins"

code_library:
  path: "./team-code-library.yaml"
  use_default: true
```

---

## Default Library

Includes 5 examples:

### Excellent
1. Thread-safe singleton with double-checked locking
2. Proper error handling with specific exceptions and logging

### Bad
1. Using `eval()` on user input (security)
2. Bare except clause swallowing all exceptions
3. God class with too many responsibilities (smelly)

---

## Use Cases

### Plugin System Use Cases

1. **Team Standards**: Enforce coding standards specific to your team
2. **Security Rules**: Add custom security checks (hardcoded secrets, SQL injection)
3. **Naming Conventions**: Enforce naming standards for your project
4. **Documentation**: Check for required docstrings/comments
5. **Custom Metrics**: Track team-specific metrics

### Code Library Use Cases

1. **Learning Tool**: Show developers examples of good vs bad code
2. **Pattern Detection**: Find anti-patterns in existing code
3. **Code Review**: Automatically catch common mistakes
4. **Team Standards**: Document team's preferred patterns
5. **Refactoring Guide**: Provide alternatives for problematic code

---

## Documentation

- **PLUGINS_QUICKSTART.md** - 5-minute getting started guide
- **docs/PLUGINS.md** - Complete plugin and code library guide (503 lines)
- **examples/example_plugin.py** - 3 example plugins with different approaches
- **examples/example_code_library.yaml** - 15+ example patterns

---

## Extensibility Benefits

1. **No Core Changes Needed**: Add features without modifying analyzer
2. **Team-Specific**: Customize for your team's needs
3. **Shareable**: Share plugins/libraries across projects
4. **Version Control**: Keep plugins and libraries in Git
5. **Iterative**: Start small, grow over time

---

## Performance Considerations

- Plugins run sequentially for each module
- Pattern matching compares against all library examples
- Default similarity threshold: 70% (prevents excessive false positives)
- Errors in plugins don't stop analysis (graceful degradation)

---

## Future Enhancements

Potential future additions:
- Plugin marketplace/registry
- Configurable similarity thresholds
- Visual code library browser
- AI-powered pattern suggestions
- Team collaboration features for libraries
- Plugin testing framework

---

## Example Workflow

1. **Start with defaults**:
   ```bash
   code-analyzer analyze ./project --use-default-library
   ```

2. **Add custom plugin**:
   Create `my-plugins/security.py` with team security rules

3. **Build team library**:
   Create `team-library.yaml` with team standards

4. **Configure project**:
   Add to `.code-analyzer.yaml`:
   ```yaml
   plugins:
     directory: "./my-plugins"
   code_library:
     path: "./team-library.yaml"
   ```

5. **Run analysis**:
   ```bash
   code-analyzer analyze ./project
   ```

6. **Iterate**:
   Add more rules and examples as issues are discovered

---

## Summary

These features make code-analyzer truly extensible:
- **Plugins**: Add custom analysis logic
- **Code Library**: Learn from classified examples
- **Easy to Use**: Simple APIs and configuration
- **Well Documented**: Complete guides and examples
- **Production Ready**: Error handling and performance considered

The analyzer is now a platform that teams can customize to their specific needs while maintaining the powerful core analysis capabilities.
