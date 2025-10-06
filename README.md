# Semgrep Security Demo

**Platform-independent static analysis tool for finding security vulnerabilities instantly.**

This repository demonstrates Semgrep's capabilities using a deliberately vulnerable Flask application with custom security rules.

## 🎯 Why Semgrep?

✅ **Runs locally** - no cloud service or GitHub required  
✅ **Lightning fast** - scan results in seconds  
✅ **Easy custom rules** - write security patterns in YAML  
✅ **Beautiful visualizations** - colored terminal output + web playground  
✅ **Multi-language** - Python, JavaScript, Java, Go, TypeScript, Ruby, C++  
✅ **Open source** - used by Snowflake, GitLab, Dropbox  

### Semgrep vs CodeQL

| Feature | CodeQL | Semgrep |
|---------|--------|---------|
| Setup time | 30+ minutes | 30 seconds |
| Runs locally | Yes (complex) | Yes (simple) |
| Visual editor | No | Yes (Playground) |
| Custom rules | QL language (hard) | YAML (easy) |
| Speed | Minutes | Seconds |
| Platform | GitHub-centric | Truly independent |

---

## 🚀 Quick Start (5 Minutes)

### 1. Clone & Setup

```bash
git clone https://github.com/partoa/codeql-security-demo-.git
cd codeql-security-demo-

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Semgrep

```bash
# Scan with custom rules
semgrep --config=semgrep-rules.yaml vulnerable_app.py

# Or use Semgrep's community rules
semgrep --config=auto vulnerable_app.py

# Beautiful output with verbose mode
semgrep --config=semgrep-rules.yaml vulnerable_app.py --verbose
```

### 3. See Results

You'll get beautiful colored output showing:
- **11 security vulnerabilities found**
- Line numbers with code snippets
- Detailed explanations and remediation guidance
- CWE and OWASP classifications

---

## 📊 Vulnerabilities Demonstrated

### Critical (9 findings)

| ID | Vulnerability | Line | CWE |
|----|---------------|------|-----|
| 1 | SQL Injection (f-string) | 20 | CWE-89 |
| 2 | Command Injection (os.system) | 27 | CWE-78 |
| 3 | Code Injection (eval) | 35 | CWE-94 |
| 4 | Shell Injection (subprocess) | 43 | CWE-78 |
| 5 | Server-Side Template Injection | 51 | CWE-94 |
| 6 | Path Traversal | 59 | CWE-22 |
| 7 | Unsafe Deserialization | 74 | CWE-502 |
| 8 | Hardcoded Password | 9 | CWE-798 |
| 9 | Hardcoded API Keys (3x) | 10-11 | CWE-798 |

### High (1 finding)

| ID | Vulnerability | Line | CWE |
|----|---------------|------|-----|
| 10 | Flask Debug Mode | 79 | CWE-215 |

---

## 📁 Repository Structure

```
CodeQL/
├── vulnerable_app.py          # Deliberately vulnerable Flask application
├── semgrep-rules.yaml        # Custom security rules
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── venv/                     # Virtual environment (excluded from git)
└── .gitignore               # Git ignore patterns
```

---

## 🎓 Understanding Semgrep Rules

### Example Rule Breakdown

```yaml
rules:
  - id: sql-injection-f-string
    pattern: db.execute(f"... {$VAR} ...")
    message: |
      SQL injection vulnerability detected!
      User input '$VAR' is directly interpolated into SQL.
    severity: ERROR
    languages: [python]
```

**Key concepts:**
- `pattern`: Code pattern to match (looks like the actual code!)
- `$VAR`: Metavariable that matches any expression
- `...`: Ellipsis that matches any code
- `severity`: ERROR (blocking), WARNING, or INFO
- `message`: Detailed explanation with remediation

### Advanced Pattern Features

#### Pattern Combinators

```yaml
patterns:
  - pattern: os.system($CMD)
  - pattern-not: os.system("safe-command")  # Exclude false positives
```

#### Pattern Either (OR logic)

```yaml
pattern-either:
  - pattern: API_KEY = "..."
  - pattern: SECRET_TOKEN = "..."
  - pattern: $VAR = "sk-..."  # OpenAI keys
  - pattern: $VAR = "ghp_..."  # GitHub tokens
```

#### Taint Tracking (Advanced)

```yaml
mode: taint
pattern-sources:
  - pattern: request.args.get(...)
pattern-sinks:
  - pattern: db.execute(...)
```

This traces user input through your application automatically, just like CodeQL!

---

## 🎬 5-Minute Demo Script

### [0:00-0:45] Hook

"How do you find security vulnerabilities instantly, without waiting for CI/CD or cloud services?

I'm going to show you Semgrep - an open-source static analysis tool that scans code for vulnerabilities in seconds, right from your terminal.

It's like CodeQL but runs locally, has better visualizations, and is easier to customize. Let me show you."

---

### [0:45-1:30] What is Semgrep

*[Show terminal with vulnerable_app.py open]*

"Here's a Flask app with intentional security flaws. Semgrep finds them in seconds.

What makes Semgrep different:

**1. Pattern-based matching** - Rules look like the code you're searching for  
**2. Metavariables** - Abstract patterns that match any expression  
**3. Instant local execution** - No cloud service needed

Watch this:"

```bash
semgrep --config=semgrep-rules.yaml vulnerable_app.py
```

*[Beautiful colored output appears]*

"11 vulnerabilities found in 2 seconds:
- SQL injection on line 20
- Command injection on line 27  
- Code injection on line 35
- Hardcoded secrets on lines 9-11
- And more..."

---

### [1:30-2:45] Custom Rule Writing

*[Open https://semgrep.dev/playground in browser]*

"Now here's where Semgrep becomes powerful - writing custom rules is EASY.

I'm in the Semgrep Playground. Left panel is my rule, middle is the code, right shows matches in real-time."

*[Type rule in left panel]*

```yaml
rules:
  - id: sql-injection
    pattern: db.execute(f"... {$INPUT} ...")
    message: User input in SQL query
    severity: ERROR
    languages: [python]
```

*[Type code in middle panel]*

```python
query = request.args.get('q')
db.execute(f"SELECT * FROM users WHERE name = '{query}'")
```

*[Right panel highlights the match]*

"See? The pattern uses:
- `f"..."` to match f-strings
- `{$INPUT}` as a metavariable matching any expression
- `...` to match any SQL before/after

This isn't regex - it understands Python's syntax tree.

Let me write another - detecting hardcoded secrets:"

*[Type new rule]*

```yaml
pattern-either:
  - pattern: API_KEY = "..."
  - pattern: SECRET_TOKEN = "..."
  - pattern: $VAR = "sk-..."  # OpenAI keys
```

*[Show it catching all hardcoded credentials]*

"The `pattern-either` is like an OR - matches any of these patterns."

---

### [2:45-3:45] Advanced Features

"Semgrep has enterprise-grade features:

**1. Taint tracking** - Follow data flow like CodeQL:

```yaml
mode: taint
pattern-sources:
  - pattern: request.args.get(...)
pattern-sinks:
  - pattern: db.execute(...)
```

This traces user input through your application automatically.

**2. Auto-fix** - Semgrep can fix vulnerabilities:

```yaml
fix: db.execute("SELECT * FROM users WHERE name = ?", [$INPUT])
```

Run with `--autofix` and it rewrites your code safely.

**3. CI Integration** - Works with any CI system:

```yaml
- run: semgrep --config=auto --error
```

But unlike CodeQL, it also runs locally instantly."

---

### [3:45-4:45] Real-World Usage

*[Show terminal]*

"In real workflows, I use Semgrep to:

**Pre-commit hooks** - Catch vulnerabilities before they're committed:

```bash
semgrep --config=auto --error .
```

**IDE integration** - VS Code extension shows issues in real-time

**CI/CD** - Block vulnerable code in pull requests

**Code audits** - Scan third-party code before integration

The ROI: Traditional SAST tools cost $500/month per developer. Semgrep is free and runs 10x faster.

Let me run it on our vulnerable app one more time:"

```bash
semgrep --config=semgrep-rules.yaml vulnerable_app.py --json | jq '.results | length'
# Output: 11
```

"11 vulnerabilities. Each with:
- The vulnerable code pattern
- Why it's dangerous
- How to fix it
- CWE classification
- OWASP mapping"

---

### [4:45-5:00] Closing

"So here's what we covered:
- How Semgrep does pattern-based static analysis locally
- Writing custom rules with metavariables in the Playground
- Advanced features like taint tracking and auto-fix
- Real-world usage in development workflows

I learned Semgrep because I needed instant security feedback - not waiting for CI/CD. After 6 months, I've caught dozens of vulnerabilities before code review.

If you're serious about security, Semgrep is the fastest, most customizable tool available.

Thanks for watching - now go scan your code."

---

## 🎨 Visual Demo Options

### Option 1: Terminal (Fastest)

Beautiful colored output built-in:

```bash
semgrep --config=semgrep-rules.yaml vulnerable_app.py
```

### Option 2: Semgrep Playground (Most Impressive)

Go to: **https://semgrep.dev/playground**

- **Left panel**: Write your rule in YAML
- **Middle panel**: Paste your code
- **Right panel**: See matches highlighted in real-time

This is your visual graph equivalent - interactive and impressive!

### Option 3: VS Code Extension

Install "Semgrep" extension from marketplace:
- Real-time vulnerability detection
- Inline code highlighting
- Jump to rule definitions
- Run custom rule files

---

## 🔒 Vulnerability Details

### 1. SQL Injection (Line 20)

```python
result = db.execute(f"SELECT * FROM users WHERE name = '{query}'")
```

**Attack**: `?q=' OR '1'='1`  
**Impact**: Read/modify entire database  
**Fix**: Use parameterized queries

```python
result = db.execute("SELECT * FROM users WHERE name = ?", (query,))
```

### 2. Command Injection (Line 27)

```python
os.system(cmd)
```

**Attack**: `?cmd=rm -rf /`  
**Impact**: Arbitrary command execution  
**Fix**: Use subprocess with list arguments

```python
subprocess.run(['ping', '-c', '1', host], capture_output=True)
```

### 3. Code Injection (Line 35)

```python
result = eval(code)
```

**Attack**: `?code=__import__('os').system('rm -rf /')`  
**Impact**: Arbitrary Python code execution  
**Fix**: Never use eval() on user input

```python
import ast
result = ast.literal_eval(code)  # Only for safe literals
```

### 4. Hardcoded Secrets (Lines 9-11)

```python
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
```

**Impact**: Exposed credentials in git history  
**Fix**: Use environment variables

```python
DB_PASSWORD = os.getenv('DB_PASSWORD')
API_KEY = os.getenv('API_KEY')
```

---

## 📚 Learning Resources

- **Official Docs**: https://semgrep.dev/docs/
- **Playground**: https://semgrep.dev/playground
- **Rule Examples**: https://semgrep.dev/r
- **Community Rules**: https://github.com/returntocorp/semgrep-rules
- **VS Code Extension**: Search "Semgrep" in Extensions

---

## ⚙️ Advanced Usage

### Custom Rule File

```bash
# Run specific rule file
semgrep --config=semgrep-rules.yaml .

# Run multiple configs
semgrep --config=auto --config=semgrep-rules.yaml .

# JSON output for CI/CD
semgrep --config=auto --json > results.json
```

### Pre-commit Hook

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/returntocorp/semgrep
    rev: v1.139.0
    hooks:
      - id: semgrep
        args: ['--config=semgrep-rules.yaml', '--error']
```

### GitHub Actions

Create `.github/workflows/semgrep.yml`:

```yaml
name: Semgrep Security Scan

on: [push, pull_request]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: semgrep-rules.yaml
```

---

## 🐛 Troubleshooting

**Issue**: `semgrep: command not found`  
**Solution**: Activate virtual environment: `source venv/bin/activate`

**Issue**: No findings shown  
**Solution**: Make sure you're in the correct directory with `vulnerable_app.py`

**Issue**: Rule parse errors  
**Solution**: Check YAML indentation (use 2 spaces, not tabs)

**Issue**: Pattern not matching  
**Solution**: Test in Semgrep Playground first to debug the pattern

---

## 🤝 Contributing

Found a bug or have a suggestion? Open an issue or PR!

Want to add more vulnerable code examples? Please do!

---

## ⚠️ Security Notice

**DO NOT deploy or run `vulnerable_app.py` in production!**

This application contains intentional security vulnerabilities for educational purposes only.

---

## 📝 License

MIT License - Free to use for learning and demonstration purposes.

---

**Happy scanning! 🔍**