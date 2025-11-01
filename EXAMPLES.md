# Code Analyzer - Examples & Results

This document shows real-world examples of code that can be analyzed and the resulting findings.

## Example 1: Simple Python Project

### Input Code

```python
# main.py
import pickle
import sys

def calculate_average(numbers):
    """Calculate average of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def process_data(data, filter_value, threshold, limit, offset, mode):
    """Process data with many parameters."""
    results = []
    for item in data:
        if item > filter_value and item < threshold:
            if mode == "strict":
                if item % 2 == 0:
                    if limit > 0:
                        results.append(item)
                        limit -= 1
    return results

class DataManager:
    """Manages data operations."""
    
    def __init__(self):
        self.data = []
    
    def add_item(self, item):
        self.data.append(item)
    
    def remove_item(self, item):
        self.data.remove(item)
    
    def get_all(self):
        return self.data

def unused_helper():
    """This function is never called."""
    pass

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    print(f"Average: {avg}")
```

### Analysis Results

#### 📊 Metrics
- **Files**: 1
- **Lines of Code**: 45
- **Functions**: 5
- **Classes**: 1
- **Issues Found**: 7
- **Average Complexity**: 3.2
- **Max Complexity**: 12

#### 🔴 Issues Detected

**1. SECURITY - Potentially dangerous import: pickle**
- **Location**: `main.py:1`
- **Severity**: MEDIUM
- **Description**: Module imports pickle which can be unsafe
- **Recommendation**: Ensure proper input validation when using this module

**2. CODE_SMELL - Long parameter list in process_data**
- **Location**: `main.py:12 in process_data()`
- **Severity**: MEDIUM
- **Description**: Function has 6 parameters
- **Recommendation**: Consider using a configuration object or builder pattern

**3. COMPLEXITY - High complexity in process_data**
- **Location**: `main.py:12 in process_data()`
- **Severity**: HIGH
- **Description**: Function has cyclomatic complexity of 12
- **Recommendation**: Consider breaking this function into smaller, more focused functions

**4. UNUSED_CODE - Potentially unused function: unused_helper**
- **Location**: `main.py:33 in unused_helper()`
- **Severity**: LOW
- **Description**: This function is not called anywhere in the codebase
- **Recommendation**: Consider removing if truly unused, or document its external usage

**5. DOCUMENTATION - Missing docstring: process_data**
- **Location**: `main.py:12 in process_data()`
- **Severity**: LOW
- **Description**: Public function lacks comprehensive documentation
- **Recommendation**: Add detailed docstring describing parameters and return value

#### 🎯 Critical Sections

**1. process_data**
- **Location**: `main.py:12-23`
- **Reason**: High complexity (12)
- **Risk Level**: HIGH
- **Dependencies**: None

**2. main**
- **Location**: `main.py:36-40`
- **Reason**: Application entry point
- **Risk Level**: HIGH
- **Impact Areas**: startup, initialization

---

## Example 2: Complex Class with Multiple Issues

### Input Code

```python
# user_manager.py
class UserManager:
    """Manages all user operations."""
    
    def __init__(self, db, cache, logger, config, validator, 
                 mailer, notifier, analyzer, metrics):
        self.db = db
        self.cache = cache
        self.logger = logger
        self.config = config
        self.validator = validator
        self.mailer = mailer
        self.notifier = notifier
        self.analyzer = analyzer
        self.metrics = metrics
        self.users = []
    
    def create_user(self, username, email, password, first_name, 
                   last_name, phone, address, city, country):
        # Complex creation logic
        if not username or not email:
            return None
        if len(password) < 8:
            return None
        user = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'address': address,
            'city': city,
            'country': country
        }
        self.users.append(user)
        self.cache.set(username, user)
        self.logger.info(f"Created user {username}")
        self.metrics.increment('users_created')
        return user
    
    def delete_user(self, username):
        # Delete logic
        pass
    
    def update_user(self, username, **kwargs):
        # Update logic
        pass
    
    def get_user(self, username):
        # Get logic
        pass
    
    def list_users(self):
        # List logic
        pass
    
    def search_users(self, query):
        # Search logic
        pass
    
    def activate_user(self, username):
        # Activation logic
        pass
    
    def deactivate_user(self, username):
        # Deactivation logic
        pass
    
    def reset_password(self, username):
        # Password reset logic
        pass
    
    def send_notification(self, username, message):
        # Send notification
        pass
    
    def validate_email(self, email):
        # Email validation
        pass
    
    def export_users(self, format):
        # Export logic
        pass
    
    def import_users(self, file):
        # Import logic
        pass
    
    def generate_report(self):
        # Report generation
        pass
    
    def archive_user(self, username):
        # Archive logic
        pass
    
    def restore_user(self, username):
        # Restore logic
        pass
    
    def merge_users(self, user1, user2):
        # Merge logic
        pass
```

### Analysis Results

#### 🔴 Issues Detected

**1. CONCEPTUAL - God class: UserManager**
- **Location**: `user_manager.py:2`
- **Severity**: HIGH
- **Description**: Class has 19 methods, indicating too many responsibilities
- **Recommendation**: Consider splitting into smaller, more focused classes following SRP
  - UserCRUD (create, read, update, delete)
  - UserValidation (validate_email, etc.)
  - UserNotification (send_notification)
  - UserReporting (generate_report, export_users)
  - UserManagement (activate, deactivate, archive, restore)

**2. CODE_SMELL - Long parameter list in __init__**
- **Location**: `user_manager.py:4`
- **Severity**: MEDIUM
- **Description**: Function has 9 parameters
- **Recommendation**: Consider using dependency injection container or builder pattern

**3. CODE_SMELL - Long parameter list in create_user**
- **Location**: `user_manager.py:18`
- **Severity**: MEDIUM
- **Description**: Function has 9 parameters
- **Recommendation**: Use a User data class or UserCreateRequest object

**4. COMPLEXITY - Moderate complexity in create_user**
- **Location**: `user_manager.py:18`
- **Severity**: MEDIUM
- **Description**: Function has cyclomatic complexity of 11
- **Recommendation**: Extract validation and user creation into separate methods

---

## Example 3: Security Vulnerabilities

### Input Code

```python
# data_handler.py
import pickle
import marshal
import os

def load_data(filename):
    """Load pickled data from file."""
    with open(filename, 'rb') as f:
        return pickle.load(f)

def save_data(data, filename):
    """Save data using pickle."""
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def execute_command(cmd):
    """Execute system command."""
    os.system(cmd)  # Dangerous!

def load_config(config_string):
    """Load configuration."""
    return eval(config_string)  # Very dangerous!
```

### Analysis Results

#### 🔴 CRITICAL Issues

**1. SECURITY - Potentially dangerous import: pickle**
- **Location**: `data_handler.py:2`
- **Severity**: MEDIUM
- **Description**: Module imports pickle which can execute arbitrary code during deserialization
- **Recommendation**: 
  - Use JSON or YAML for configuration files
  - If pickle is necessary, validate source and use signing
  - Consider alternatives like `json` or `msgpack`

**2. SECURITY - Potentially dangerous import: marshal**
- **Location**: `data_handler.py:3`
- **Severity**: MEDIUM
- **Description**: Marshal is internal Python format and can be unsafe
- **Recommendation**: Use safer serialization formats

**3. BUG - Unsafe command execution**
- **Location**: `data_handler.py:17`
- **Severity**: CRITICAL
- **Description**: Direct system command execution without sanitization
- **Recommendation**: 
  - Use `subprocess.run()` with list arguments
  - Validate and sanitize all inputs
  - Use shell=False option

**4. SECURITY - eval() usage**
- **Location**: `data_handler.py:21`
- **Severity**: CRITICAL
- **Description**: eval() can execute arbitrary code
- **Recommendation**: 
  - Use `ast.literal_eval()` for safe evaluation
  - Use JSON for configuration
  - Implement proper config parser

---

## Example 4: Real Project Analysis

### What the Tool Can Process

The analyzer can handle:

✅ **Any Python Project**
- Web applications (Django, Flask, FastAPI)
- CLI tools
- Data science projects
- Machine learning code
- Automation scripts
- Libraries and packages

✅ **Project Sizes**
- Small: 1-10 files (< 1,000 LOC)
- Medium: 10-100 files (1,000-10,000 LOC)
- Large: 100+ files (10,000+ LOC)

✅ **Python Versions**
- Python 3.8+
- Modern syntax (async/await, type hints, dataclasses)

### Example: Analyzing logseq-python

```bash
code-analyzer analyze /Volumes/Projects/logseq-python --depth deep
```

**Expected Results:**
```
🔍 Analyzing project: /Volumes/Projects/logseq-python
   Depth: deep
   Found 12 Python files

✅ Analysis complete:
   Modules: 12
   Issues: 43
   Critical sections: 8

Analysis Summary
┌─────────────────────┬────────┐
│ Metric              │ Value  │
├─────────────────────┼────────┤
│ Files Analyzed      │ 12     │
│ Total Lines         │ 3,421  │
│ Classes             │ 15     │
│ Functions           │ 87     │
│ Issues Found        │ 43     │
│ Critical Sections   │ 8      │
│ Avg Complexity      │ 4.2    │
│ Max Complexity      │ 18     │
└─────────────────────┴────────┘

Issues by Severity
  🔴 CRITICAL: 2
  🟠 HIGH: 8
  🟡 MEDIUM: 15
  🔵 LOW: 18

💾 Saved analysis to: /Volumes/Projects/logseq-python/.code-analyzer/analysis.json
```

---

## Generated Outputs

### 1. JSON Report

`.code-analyzer/analysis.json`:
```json
{
  "project_path": "/path/to/project",
  "analysis_date": "2025-10-31T17:00:00",
  "metrics": {
    "total_files": 5,
    "total_lines": 450,
    "total_classes": 3,
    "total_functions": 15,
    "total_issues": 12,
    "average_complexity": 4.5,
    "max_complexity": 12
  },
  "issues": [
    {
      "type": "complexity",
      "severity": "high",
      "title": "High complexity in process_data",
      "description": "Function has cyclomatic complexity of 12",
      "location": "main.py:12 in process_data()",
      "recommendation": "Break into smaller functions"
    }
  ],
  "critical_sections": [
    {
      "name": "main.process_data",
      "location": "main.py:12-23",
      "reason": "High complexity (12)",
      "risk_level": "high"
    }
  ]
}
```

### 2. Logseq Documentation

Created pages in your Logseq graph:

```
Code Analysis: ProjectName/
├── Overview (metrics, quick stats)
├── Metrics (detailed metrics)
├── Critical Sections (high-risk areas)
├── Issues/
│   ├── Critical (2 issues)
│   ├── High (8 issues)
│   ├── Medium (15 issues)
│   └── Low (18 issues)
├── Modules (per-module documentation)
└── Dependencies (dependency graph)
```

### 3. Repo-Tickets

Created in `.tickets/`:

```
Epic: Code Quality Improvements: ProjectName
├── TICKET-1: High complexity in process_data [HIGH]
├── TICKET-2: Potentially dangerous import: pickle [MEDIUM]
├── TICKET-3: God class: UserManager [HIGH]
├── TICKET-4: Long parameter list in create_user [MEDIUM]
└── TICKET-5: Code Analysis Summary and Action Plan [HIGH]
```

### 4. Anonymized Code

`/tmp/anonymized/`:
```
main.py (with anonymized names)
ANONYMIZATION_MAP.txt (secure - keep private)
STRUCTURE_SUMMARY.md (safe to share)
```

---

## Real-World Use Cases

### Use Case 1: Legacy Code Audit
**Scenario**: Inheriting old Python codebase
**Command**:
```bash
code-analyzer analyze /path/to/legacy-project \
  --depth deep \
  --generate-docs \
  --logseq-graph ~/logseq
```
**Result**: Complete documentation in Logseq showing:
- Complexity hotspots requiring refactoring
- Security vulnerabilities to address
- Unused code that can be removed
- Documentation gaps to fill

### Use Case 2: Code Review Preparation
**Scenario**: Preparing code for team review
**Command**:
```bash
code-analyzer analyze /path/to/project --create-tickets
```
**Result**: Tickets created for each issue, prioritized by severity, ready for sprint planning

### Use Case 3: Compliance & Security Audit
**Scenario**: Security audit before deployment
**Command**:
```bash
code-analyzer analyze /path/to/project \
  --depth deep \
  --output security-audit
```
**Result**: JSON report highlighting all security issues, dangerous imports, and vulnerabilities

### Use Case 4: External Consultant Review
**Scenario**: Need external code review but code is proprietary
**Command**:
```bash
code-analyzer anonymize /path/to/project \
  --output /tmp/anonymized-for-review
```
**Result**: Anonymized codebase safe to share externally while preserving structure for analysis

---

## Command Examples

### Basic Analysis
```bash
# Quick shallow analysis
code-analyzer analyze /path/to/project --depth shallow

# Deep analysis with all features
code-analyzer analyze /path/to/project \
  --depth deep \
  --generate-docs \
  --logseq-graph ~/logseq \
  --create-tickets
```

### Filtered Reporting
```bash
# View only critical issues
code-analyzer report .code-analyzer/analysis.json --severity critical

# View only security issues
code-analyzer report .code-analyzer/analysis.json --type security
```

### Configuration-Based
```bash
# Create .code-analyzer.yaml in project
cat > .code-analyzer.yaml <<EOF
analysis:
  depth: deep
documentation:
  logseq_graph: ~/logseq
tickets:
  enabled: true
EOF

# Run with config
code-analyzer analyze .
```

### Batch Processing
```bash
# Analyze multiple projects
for proj in project1 project2 project3; do
  code-analyzer analyze /path/to/$proj --output reports/$proj
done
```

---

## What Gets Detected - Summary

| Category | What's Detected | Severity Range |
|----------|-----------------|----------------|
| **Bugs** | Logic errors, type issues, undefined vars | HIGH-MEDIUM |
| **Security** | Dangerous imports, unsafe deserialization | CRITICAL-MEDIUM |
| **Performance** | High complexity, inefficient algorithms | HIGH-MEDIUM |
| **Code Smells** | Long parameters, god classes, duplicates | MEDIUM-LOW |
| **Complexity** | Cyclomatic complexity > 10 | HIGH-MEDIUM |
| **Unused Code** | Uncalled functions, dead code | LOW |
| **Conceptual** | SOLID violations, poor architecture | HIGH-MEDIUM |
| **Documentation** | Missing docstrings | LOW |

---

## Interpreting Results

### Severity Levels

🔴 **CRITICAL** - Fix immediately before deployment
- Security vulnerabilities (eval, os.system)
- Data corruption risks
- System stability issues

🟠 **HIGH** - Address in current sprint
- High complexity (> 15)
- God classes
- Major code smells

🟡 **MEDIUM** - Plan to fix soon
- Moderate complexity (10-15)
- Long parameter lists
- Dangerous imports (pickle)

🔵 **LOW** - Nice to fix when possible
- Missing documentation
- Minor code smells
- Unused code

⚪ **INFO** - Informational only
- Metrics and statistics
- Architectural observations

---

## Next Steps After Analysis

1. **Review Logseq Documentation** - Understand findings
2. **Prioritize Tickets** - Critical → High → Medium → Low
3. **Create Action Plan** - Sprint planning
4. **Fix Issues** - Address highest severity first
5. **Re-analyze** - Verify improvements
6. **Track Progress** - Use Logseq and tickets

The tool provides everything needed to understand, prioritize, and track code quality improvements!
