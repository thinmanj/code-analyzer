================================================================================

ENGINEERING ONBOARDING: code-analyzer

================================================================================



**Project Size**: 27 files, 8,592 lines

**Complexity**: Complex



# 🏗️  ARCHITECTURE DEEP DIVE
================================================================================

## Architectural Pattern
**Style**: Command-Line Application




# 🗺️  LEARNING ROADMAP
================================================================================

## Phase 1: Setup & Overview (30-60 minutes)

### Prerequisites
- Python 3.8+ installed
- Familiarity with: Click (CLI framework), pytest (testing)

### Tasks
1. **Clone and setup environment**
   ```bash
   git clone <repository>
   cd code-analyzer
   pip install -r requirements.txt  # or pip install -e .
   ```

2. **Verify installation**
   ```bash
   python -m pytest  # Run tests
   ```

3. **Explore project structure**
   ```bash
   tree -L 2 -I '__pycache__|*.pyc|.git'
   ```

## Phase 2: Entry Points (1-2 hours)

1. **benchmark.py**
   - Has main() function - application entry point
   - Open: `nvim +1 benchmark.py` or click: [VS Code](vscode://file/benchmark.py:1)

2. **code_analyzer/cli.py**
   - Has main() function - application entry point
   - Open: `nvim +1 code_analyzer/cli.py` or click: [VS Code](vscode://file/code_analyzer/cli.py:1)

3. **examples/test_plugins.py**
   - Has main() function - application entry point
   - Open: `nvim +1 examples/test_plugins.py` or click: [VS Code](vscode://file/examples/test_plugins.py:1)

## Phase 3: Core Modules (3-5 hours)

Study these modules in order:

1. **code_analyzer/analyzer.py** - Analysis and processing
   - nvim: `nvim code_analyzer/analyzer.py`
   - Focus on main classes and their public methods

2. **code_analyzer/anonymizer.py** - Analysis and processing
   - nvim: `nvim code_analyzer/anonymizer.py`
   - Focus on main classes and their public methods

3. **code_analyzer/autofix.py** - Analysis and processing
   - nvim: `nvim code_analyzer/autofix.py`
   - Focus on main classes and their public methods

4. **code_analyzer/cli.py** - Analysis and processing
   - nvim: `nvim code_analyzer/cli.py`
   - Focus on main classes and their public methods

5. **code_analyzer/code_library.py** - Analysis and processing
   - nvim: `nvim code_analyzer/code_library.py`
   - Focus on main classes and their public methods

## Phase 4: Testing & Validation (1-2 hours)

- Read test files to understand expected behavior
- Run tests and see what breaks when you change things
- Write a simple test for a new feature

## Phase 5: Making Changes (ongoing)

- Start with small bug fixes or documentation improvements
- Use git blame to see change history: `git blame <file>`
- Ask questions in code reviews




# 💻 CODE EXAMPLES
================================================================================

## Key Classes to Understand

These are the core classes that drive the application:

### Class: `code_analyzer.anonymizer.CodeAnonymizer`
**Purpose**: Anonymizes code for external LLM analysis while preserving structure.

### Class: `code_analyzer.analyzer.CodeAnalyzer`
**Purpose**: Main code analyzer that parses and analyzes Python code.

### Class: `code_analyzer.important_sections.ImportantSectionIdentifier`
**Purpose**: Identifies important sections and patterns in code.

### Class: `code_analyzer.improvement_detector.ImprovementDetector`
**Purpose**: Detects code that needs updates and improvements.

### Class: `code_analyzer.autofix.AutoFixGenerator`
**Purpose**: Generate automatic fixes for common code issues.


## Important Functions

Critical functions you should understand:

### Function: `code_analyzer.onboarding.format_onboarding_report`
**Role**: Format onboarding insights as a human-readable report.

### Function: `code_analyzer.onboarding_formatter.format_architecture_section`
**Role**: Format detailed architecture section.

### Function: `code_analyzer.cli.analyze`
**Role**: Analyze a Python project.




# 🐛 DEBUGGING GUIDE
================================================================================

## Quick Debugging Commands

### Set up debugging in your editor

**VS Code (launch.json):**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

**Neovim (using nvim-dap):**
```lua
require('dap-python').setup('python')
-- Set breakpoint: <leader>db
-- Continue: <leader>dc
-- Step over: <leader>ds
```

### Command-line debugging
```bash
# Add breakpoint in code:
import pdb; pdb.set_trace()

# Or use ipdb for better experience:
import ipdb; ipdb.set_trace()
```

## Common Issues & Solutions

- **Issue**: 21 modules have high complexity - start with simpler ones
  - **Solution**: Review simpler modules first, use debugger to step through

- **Issue**: Many dependencies - make sure you understand the core ones first
  - **Solution**: Review simpler modules first, use debugger to step through




# 📚 QUICK REFERENCE

================================================================================



## Key Dependencies

- `code_analyzer`

- `rich`

- `radon`

- `tracemalloc`

- `tempfile`



## Helpful Commands

```bash

tree -L 2

```

→ View project structure



```bash

find . -name '*.py' | wc -l

```

→ Count Python files



```bash

grep -r 'class ' --include='*.py' | wc -l

```

→ Count classes



```bash

pytest -v

```

→ Run tests with verbose output



```bash

pytest --cov

```

→ Run tests with coverage



```bash

python -m code_analyzer/cli --help

```

→ View CLI help



```bash

pylint *.py

```

→ Check code quality



```bash

radon cc . -a

```

→ Calculate cyclomatic complexity



```bash

pydoc <module>

```

→ View module documentation



================================================================================

**Pro Tips**:

- Use `git log --follow <file>` to see file history

- Use `git blame -L <start>,<end> <file>` to see who wrote what

- Set up editor to jump to definitions (Ctrl+Click or gd in vim)

- Install language server (pyright/pylsp) for better autocomplete

================================================================================