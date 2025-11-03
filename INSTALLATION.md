# Installation Guide

Complete guide to installing and setting up code-analyzer on your system.

## Quick Install (Recommended)

```bash
pip install code-analyzer
```

**Note**: Once published to PyPI, this will be the simplest installation method.

## Install from Source

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/thinmanj/code-analyzer.git
cd code-analyzer
```

### Step 2: Install in Development Mode

```bash
# Basic installation
pip install -e .

# With all optional dependencies
pip install -e ".[full,dev]"
```

### Installation Options

**Basic** (Core features only):
```bash
pip install -e .
```
Includes: AST parsing, basic analysis, reporting

**Full** (All features):
```bash
pip install -e ".[full]"
```
Includes: bandit, pylint, jedi for enhanced analysis

**Development** (For contributors):
```bash
pip install -e ".[dev]"
```
Includes: pytest, pytest-cov, black, mypy

**Everything**:
```bash
pip install -e ".[full,dev]"
```

## Platform-Specific Instructions

### macOS

1. **Install Python** (if not already installed):
   ```bash
   brew install python@3.11
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install code-analyzer**:
   ```bash
   pip install code-analyzer
   ```

### Linux (Ubuntu/Debian)

1. **Install Python**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install code-analyzer**:
   ```bash
   pip install code-analyzer
   ```

### Windows

1. **Install Python** from [python.org](https://python.org/downloads)
   - Make sure to check "Add Python to PATH" during installation

2. **Open PowerShell or Command Prompt**

3. **Create virtual environment**:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install code-analyzer**:
   ```powershell
   pip install code-analyzer
   ```

## Verify Installation

After installation, verify it works:

```bash
code-analyzer --version

# Test with self-analysis
code-analyzer analyze . --depth shallow
```

You should see the analyzer version and analysis output.

## Optional Dependencies

### For LLM Features

Set environment variables for AI-powered analysis:

```bash
# For OpenAI (GPT-4)
export OPENAI_API_KEY="your-api-key"

# For Anthropic (Claude)
export ANTHROPIC_API_KEY="your-api-key"
```

### For Git History Analysis

Code-analyzer automatically uses git if available:

```bash
# macOS
brew install git

# Linux
sudo apt install git

# Windows
# Download from git-scm.com
```

### For Enhanced Security Scanning

```bash
pip install bandit safety pip-audit
```

## Troubleshooting

### Common Issues

#### Issue: "command not found: code-analyzer"

**Solution**: Ensure pip install location is in PATH:
```bash
# Check where pip installs scripts
python -m site --user-base

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$(python -m site --user-base)/bin"
```

#### Issue: "ImportError: No module named 'code_analyzer'"

**Solution**: Install in development mode or use virtual environment:
```bash
pip install -e .
```

#### Issue: "SyntaxError" when running

**Solution**: Check Python version (must be 3.8+):
```bash
python --version
# Should show Python 3.8 or higher
```

#### Issue: "Permission denied" on Linux/macOS

**Solution**: Use virtual environment or user install:
```bash
pip install --user code-analyzer
```

#### Issue: Dependencies conflict

**Solution**: Use fresh virtual environment:
```bash
python -m venv fresh_env
source fresh_env/bin/activate  # or: fresh_env\Scripts\activate on Windows
pip install code-analyzer
```

### Performance Issues

If analysis is slow:

1. **Use shallow depth for large projects**:
   ```bash
   code-analyzer analyze . --depth shallow
   ```

2. **Increase memory** (for very large codebases):
   ```bash
   # Adjust based on available RAM
   ulimit -s 65536
   ```

3. **Exclude unnecessary directories**:
   Create `.code-analyzer.yaml`:
   ```yaml
   analysis:
     ignore_patterns:
       - "*/node_modules/*"
       - "*/venv/*"
       - "*/build/*"
   ```

### Getting Help

If you encounter issues:

1. **Check existing issues**: https://github.com/thinmanj/code-analyzer/issues
2. **Search discussions**: Look for similar problems
3. **Create new issue**: Include:
   - Python version (`python --version`)
   - Operating system
   - Installation method
   - Full error message
   - Steps to reproduce

## Updating

To update to the latest version:

```bash
# From PyPI
pip install --upgrade code-analyzer

# From source
cd code-analyzer
git pull
pip install -e .
```

## Uninstalling

To remove code-analyzer:

```bash
pip uninstall code-analyzer
```

## Next Steps

After installation:

1. **Read the Quick Start**: See [README.md](README.md#quick-start)
2. **Try example projects**: Run analysis on sample codebases
3. **Configure**: Create `.code-analyzer.yaml` for your projects
4. **Explore features**: Try onboarding and intelligence reports

## Development Setup

For contributors who want to work on code-analyzer:

```bash
# Clone repository
git clone https://github.com/thinmanj/code-analyzer.git
cd code-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[full,dev]"

# Run tests
pytest

# Check coverage
pytest --cov=code_analyzer --cov-report=html

# Format code
black code_analyzer/

# Type checking
mypy code_analyzer/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.
