# Plugins & Code Library - Quick Start

Get up and running with custom plugins and code libraries in 5 minutes.

## Quick Start: Plugins

### 1. Create a Plugin Directory

```bash
mkdir my-plugins
cd my-plugins
```

### 2. Create Your First Plugin

Create `my_plugin.py`:

```python
from code_analyzer.plugins import CustomRulePlugin
from code_analyzer.models import IssueSeverity

class MyRules(CustomRulePlugin):
    @property
    def name(self):
        return "my-rules"
    
    @property
    def version(self):
        return "1.0.0"
    
    def __init__(self):
        super().__init__()
        
        # Add your custom rules here
        self.add_rule(
            name="no-todo",
            check=lambda obj: hasattr(obj, 'source_code') and 'TODO' in str(obj.source_code),
            severity=IssueSeverity.LOW,
            message="TODO comment found",
            recommendation="Track TODOs as tickets"
        )
```

### 3. Use Your Plugin

```bash
code-analyzer analyze /path/to/project --plugins ./my-plugins
```

Done! Your plugin will now run during analysis.

---

## Quick Start: Code Library

### 1. Create a Library File

Create `my-library.yaml`:

```yaml
examples:
  # Example of BAD code you want to catch
  - id: "no-eval-001"
    classification: bad
    pattern_type: security
    language: python
    description: "Using eval() is dangerous"
    reason: "Arbitrary code execution vulnerability"
    code: |
      result = eval(user_input)
    alternative: "Use ast.literal_eval() or proper parsing"
    tags: [security, eval]
  
  # Example of EXCELLENT code you want to encourage
  - id: "error-handling-001"
    classification: excellent
    pattern_type: error_handling
    language: python
    description: "Proper error handling"
    code: |
      try:
          risky_operation()
      except ValueError as e:
          logger.error(f"Invalid value: {e}")
          raise
      except Exception as e:
          logger.error(f"Unexpected error: {e}")
          raise
    tags: [error-handling, logging]
```

### 2. Use Your Library

```bash
code-analyzer analyze /path/to/project --code-library ./my-library.yaml
```

The analyzer will:
- Match your code against library examples
- Flag code similar to "bad" patterns
- Generate issues with recommendations

---

## Use Both Together

```bash
code-analyzer analyze /path/to/project \
  --plugins ./my-plugins \
  --code-library ./my-library.yaml \
  --depth deep \
  --generate-docs \
  --logseq-graph ~/logseq
```

---

## Configuration File

Add to `.code-analyzer.yaml`:

```yaml
plugins:
  directory: "./my-plugins"

code_library:
  path: "./my-library.yaml"
```

Then just run:

```bash
code-analyzer analyze /path/to/project
```

---

## Examples

### Security Plugin

```python
from code_analyzer.plugins import CustomRulePlugin
from code_analyzer.models import IssueSeverity

class SecurityPlugin(CustomRulePlugin):
    @property
    def name(self):
        return "security"
    
    @property
    def version(self):
        return "1.0.0"
    
    def __init__(self):
        super().__init__()
        
        self.add_rule(
            name="no-hardcoded-secrets",
            check=lambda obj: (
                hasattr(obj, 'source_code') and
                any(x in str(obj.source_code).lower() 
                    for x in ['password =', 'api_key =', 'secret ='])
            ),
            severity=IssueSeverity.CRITICAL,
            message="Hardcoded credential detected",
            recommendation="Use environment variables"
        )
```

### Team Standards Library

```yaml
examples:
  # What we consider excellent
  - id: "team-logging-001"
    classification: excellent
    pattern_type: general
    language: python
    description: "Our standard logging pattern"
    code: |
      logger = logging.getLogger(__name__)
      logger.info("Processing started")
    tags: [team-standard, logging]
  
  # What we want to avoid
  - id: "team-anti-001"
    classification: bad
    pattern_type: structure
    language: python
    description: "Using globals for state"
    reason: "Hard to test and reason about"
    code: |
      global_state = {}
      
      def update(key, value):
          global global_state
          global_state[key] = value
    alternative: "Pass state as parameters or use a class"
    tags: [team-antipattern, globals]
```

---

## Learn More

- **Full Plugin Guide**: [docs/PLUGINS.md](docs/PLUGINS.md)
- **Example Plugin**: [examples/example_plugin.py](examples/example_plugin.py)
- **Example Library**: [examples/example_code_library.yaml](examples/example_code_library.yaml)

---

## Tips

1. **Start Small**: Begin with 3-5 rules or examples
2. **Be Specific**: Narrow patterns match better than generic ones
3. **Team Input**: Get team consensus on rules and standards
4. **Iterate**: Add more patterns as you encounter issues
5. **Document Why**: Always include reasons for bad patterns

---

## Built-in Defaults

Use the built-in code library to get started:

```bash
code-analyzer analyze /path/to/project --use-default-library
```

Includes examples for:
- Security issues (eval, hardcoded secrets)
- Error handling anti-patterns
- Design patterns (singleton, factory)
- Common Python gotchas
