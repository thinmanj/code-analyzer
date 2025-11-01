# Quick Start Guide

Get started with Code Analyzer in 5 minutes!

## Installation

```bash
cd /Volumes/Projects/code-analyzer
pip install -e .
```

## Basic Usage

### 1. Analyze a Project

```bash
# Basic analysis
code-analyzer analyze /path/to/your/project

# Deep analysis with all features
code-analyzer analyze /path/to/your/project --deep --generate-docs --create-tickets
```

### 2. View Results

Analysis results are saved in `.code-analyzer/` directory:
- `analysis.json` - Complete analysis data in JSON format
- View in terminal or use the report command

```bash
code-analyzer report /path/to/project/.code-analyzer/analysis.json
```

### 3. Logseq Documentation (Optional)

Generate documentation in your Logseq graph:

```bash
code-analyzer analyze /path/to/project \
  --generate-docs \
  --logseq-graph ~/logseq
```

This creates structured documentation pages:
- Project Overview with metrics
- Issues categorized by severity and type  
- Critical sections analysis
- Module documentation
- Dependency graphs

### 4. Create Tickets (Optional)

If you have repo-tickets initialized:

```bash
# First, initialize repo-tickets in your project
cd /path/to/project
tickets init

# Then analyze with ticket creation
code-analyzer analyze . --create-tickets
```

This creates:
- An epic for code quality improvements
- Individual tickets for critical/high issues
- A summary ticket with action plan

### 5. Code Anonymization

For privacy-preserving external analysis:

```bash
code-analyzer anonymize /path/to/project --output /tmp/anonymized

# The output includes:
# - Anonymized Python files
# - ANONYMIZATION_MAP.txt (keep this secure!)
# - STRUCTURE_SUMMARY.md (safe to share)
```

## Configuration

Create `.code-analyzer.yaml` in your project root:

```yaml
analysis:
  depth: deep
  ignore_patterns:
    - "*/migrations/*"
    - "*/tests/*"

documentation:
  logseq_graph: ~/logseq
  
tickets:
  enabled: true
  auto_prioritize: true
```

## Example Workflow

```bash
# 1. Install
cd /Volumes/Projects/code-analyzer
pip install -e .

# 2. Initialize repo-tickets in your project
cd /path/to/your/project
tickets init

# 3. Run complete analysis
code-analyzer analyze . \
  --depth deep \
  --generate-docs \
  --logseq-graph ~/logseq \
  --create-tickets

# 4. Review results
# - Check Logseq for documentation
# - Run: tickets epic list
# - View: .code-analyzer/analysis.json
```

## What Gets Analyzed?

- ✅ **Code Structure**: Classes, functions, methods
- ✅ **Complexity**: Cyclomatic complexity per function
- ✅ **Dependencies**: Import analysis and call graphs
- ✅ **Issues**: Bugs, security, performance, code smells
- ✅ **Critical Sections**: High-risk areas needing attention
- ✅ **Documentation**: Missing docstrings
- ✅ **Code Quality**: Long parameter lists, god classes, etc.

## Understanding Results

### Issue Severities

- 🔴 **CRITICAL**: Immediate attention required
- 🟠 **HIGH**: Should be addressed soon
- 🟡 **MEDIUM**: Important but not urgent
- 🔵 **LOW**: Nice to fix
- ⚪ **INFO**: Informational only

### Issue Types

- **bug**: Potential bugs or errors
- **security**: Security vulnerabilities
- **performance**: Performance issues
- **complexity**: High cyclomatic complexity
- **code_smell**: Anti-patterns
- **unused_code**: Unused functions/classes
- **conceptual**: Architectural issues
- **documentation**: Missing docs

## Tips

1. **Start shallow**: Use `--depth shallow` for quick overview
2. **Filter results**: Use filters in the report command
3. **Iterate**: Fix critical issues first, then re-analyze
4. **Document findings**: Logseq integration helps track progress
5. **Team collaboration**: Use tickets for distributed work

## Next Steps

- Read `README.md` for complete documentation
- Check `.code-analyzer.yaml.example` for all options
- Explore your Logseq graph for detailed findings
- Review created tickets: `tickets list --labels code-analysis`

## Help

```bash
code-analyzer --help
code-analyzer analyze --help
code-analyzer anonymize --help
code-analyzer report --help
```

## Self-Analysis

Want to see it in action? Analyze the code-analyzer itself:

```bash
code-analyzer analyze /Volumes/Projects/code-analyzer --deep
```
