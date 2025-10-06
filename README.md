# CodeQL Security Demo

This repository demonstrates CodeQL's automated security vulnerability detection capabilities using a deliberately vulnerable Flask application.

## 🎯 What This Demo Shows

CodeQL automatically detects:
- **SQL Injection** - Unsanitized user input in database queries
- **Command Injection** - User input flowing to system commands
- **Hardcoded Credentials** - Sensitive credentials in source code
- **Path Traversal** - Unvalidated file path access
- **Open Redirect** - Unvalidated URL redirects

## 🚀 Quick Setup (5 Minutes)

### Option 1: GitHub Web Interface (RECOMMENDED)

1. **Create a new GitHub repository**
   - Go to https://github.com/new
   - Name it `codeql-security-demo`
   - Make it **public** (required for free CodeQL scanning)
   - Click "Create repository"

2. **Upload these files to your repo**
   - Click "uploading an existing file"
   - Upload: `app.py`, `requirements.txt`, and the `.github/workflows/codeql.yml` file
   - Commit the files

3. **Enable CodeQL Scanning**
   - Go to "Settings" → "Code security and analysis"
   - Under "Code scanning", click "Set up" → "Default"
   - GitHub will automatically use the workflow file you uploaded

4. **Wait 2-3 minutes for the scan to complete**
   - Go to "Actions" tab to watch the scan progress
   - Once complete, go to "Security" tab → "Code scanning"

5. **View the vulnerabilities**
   - You should see 5+ security alerts
   - Click on each to see the data flow visualization

### Option 2: Local Setup (Advanced)

If you want to run CodeQL locally:

```bash
# Install CodeQL CLI
# Mac:
brew install codeql

# Linux/Windows: Download from
# https://github.com/github/codeql-cli-binaries/releases/latest

# Clone CodeQL standard libraries
git clone https://github.com/github/codeql.git ~/codeql-home/codeql-repo

# Create CodeQL database
cd /home/partoa/work/CodeQL
codeql database create python-db --language=python --source-root=.

# Run analysis
codeql database analyze python-db \
  ~/codeql-home/codeql-repo/python/ql/src/Security/ \
  --format=sarif-latest \
  --output=results.sarif

# View results
codeql bqrs interpret python-db/results/*.bqrs
```

## 📁 Repository Structure

```
CodeQL/
├── app.py                          # Vulnerable Flask application
├── requirements.txt                # Python dependencies
├── sql-injection.ql               # Example CodeQL query for SQL injection
├── command-injection.ql           # Example CodeQL query for command injection
├── .github/
│   └── workflows/
│       └── codeql.yml             # GitHub Actions workflow for CodeQL
└── README.md                      # This file
```

## 🎬 Demo Script (5-Minute Presentation)

### [0:00-0:45] Hook

"How do you find security vulnerabilities in a million lines of code?

I'm going to show you CodeQL - GitHub's semantic code analysis engine that treats code like a database and automatically finds vulnerabilities that would take weeks of manual review.

Let me show you a real example."

### [0:45-1:30] What is CodeQL

*[Screen: Show your GitHub repo with app.py open]*

"I created this Flask application with intentional security flaws. Here's what makes CodeQL different:

**First: Semantic Analysis**
CodeQL parses your code into a database and understands what it does - not just pattern matching.

**Second: Data Flow Tracking**  
Look at line 10: User input from `request.args.get` flows into a SQL query. CodeQL automatically traces this dangerous data flow.

**Third: Continuous Scanning**
Every commit triggers CodeQL automatically."

### [1:30-2:45] Show Results

*[Navigate to Security → Code scanning alerts]*

"CodeQL found 5+ critical vulnerabilities in about 2 minutes:

*[Click on SQL Injection alert]*

**Alert 1: SQL Injection**

See this visualization? It shows the complete attack path:
- **Source**: Line 10 - user input from URL parameter
- **Flow**: Concatenated into SQL string
- **Sink**: Line 11 - executed without sanitization

*[Click 'Show paths']*

CodeQL traced the data through variables and string operations. This is taint tracking.

*[Click on Command Injection alert]*

**Alert 2: Command Injection**

Same pattern: User input flows to `os.system()`. CodeQL understands this is a shell command execution sink."

### [2:45-3:45] Advanced Features

"Here's where CodeQL becomes enterprise-grade:

*[Show the .github/workflows/codeql.yml file]*

**GitHub Actions Integration**

This workflow runs CodeQL on every push and pull request. That's it - automatic security scanning.

**Multi-Language Support**

CodeQL works for Python, JavaScript, Java, C++, C#, Go, Ruby.

**Custom Queries**

*[Show sql-injection.ql file]*

This is the query that found our SQL injection. It's written in QL - a declarative language:

- Define **sources**: where dangerous data comes from (user input)
- Define **sinks**: where it can cause harm (SQL execution)
- Find all **paths** between them

You can write custom queries for your specific security policies."

### [3:45-4:45] Real-World Impact

"Let me show you the ROI:

**Traditional Security Audit:**
- Cost: $50,000
- Time: 2 weeks
- Output: Static PDF report
- Coverage: Snapshot in time

**CodeQL:**
- Cost: Free (public repos), included with GitHub Enterprise
- Time: Runs continuously, results in minutes
- Output: Actionable alerts with remediation
- Coverage: Every commit, every pull request

**Real-world usage:**
- Find authentication vulnerabilities in legacy code
- Audit multiple microservices in one day
- Block vulnerable code before it reaches production

When developers open a PR, CodeQL runs automatically. If it finds vulnerabilities, the PR gets flagged. No vulnerable code reaches main branch."

### [4:45-5:00] Closing

"So here's what we covered:
- Semantic analysis and data flow tracking
- Real vulnerabilities detected automatically  
- Integration with GitHub's development workflow
- Custom query capabilities

CodeQL transforms security from quarterly audits to continuous, automated vulnerability detection.

Thanks for watching - now go secure your code."

## 🔍 Understanding the Vulnerabilities

### 1. SQL Injection (Line 10-11)
```python
query = request.args.get('q')
result = db.execute("SELECT * FROM products WHERE name = '" + query + "'")
```
**Attack**: `?q=' OR '1'='1`  
**Impact**: Attacker can read/modify entire database

### 2. Command Injection (Line 17-18)
```python
host = request.args.get('host')
os.system('ping ' + host)
```
**Attack**: `?host=google.com; rm -rf /`  
**Impact**: Arbitrary command execution on server

### 3. Hardcoded Credentials (Line 24-25)
```python
username = 'admin'
password = 'password123'
```
**Impact**: Anyone reading the code has admin credentials

### 4. Path Traversal (Line 34-36)
```python
filename = request.args.get('name')
with open('/var/data/' + filename, 'r') as f:
    return f.read()
```
**Attack**: `?name=../../../etc/passwd`  
**Impact**: Read arbitrary files on the system

### 5. Open Redirect (Line 41-42)
```python
url = request.args.get('url')
return f'<meta http-equiv="refresh" content="0;url={url}">'
```
**Attack**: `?url=https://evil.com`  
**Impact**: Phishing attacks using trusted domain

## 📚 CodeQL Query Breakdown

The `sql-injection.ql` file demonstrates how CodeQL queries work:

```ql
from SqlInjectionConfiguration config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "SQL injection vulnerability: user input $@ flows to SQL execution",
  source.getNode(), "from here"
```

**Key concepts:**
- **Source**: Entry points for untrusted data (HTTP requests, file reads, etc.)
- **Sink**: Dangerous operations (SQL execution, command execution, etc.)
- **Path**: CodeQL traces data flow from source to sink through all intermediate steps
- **Taint tracking**: Follows data transformations (concatenation, formatting, etc.)

## 🎓 Learning Resources

- **Official CodeQL Documentation**: https://codeql.github.com/docs/
- **CodeQL for Security Researchers**: https://securitylab.github.com/
- **CodeQL Query Examples**: https://github.com/github/codeql/tree/main/python/ql/src/Security
- **Interactive CodeQL Tutorial**: https://codeql.github.com/docs/writing-codeql-queries/

## ⚠️ Important Notes

- **DO NOT deploy this application** - it contains intentional vulnerabilities
- This is for educational purposes only
- CodeQL scanning is free for public repositories
- Private repos require GitHub Advanced Security license
- First scan may take 3-5 minutes; subsequent scans are faster

## 🔧 Troubleshooting

**CodeQL scan not running?**
- Ensure repository is public
- Check Actions tab for workflow status
- Verify `.github/workflows/codeql.yml` is in the correct location

**No alerts showing?**
- Wait 2-3 minutes after first commit
- Check Security tab → Code scanning
- Ensure workflow completed successfully in Actions tab

**Want to test locally?**
- Install CodeQL CLI (see Option 2 above)
- Requires ~2GB disk space for CodeQL libraries
- Works on Mac, Linux, and Windows

## 📞 Next Steps

1. **Push this code to GitHub** (follow setup instructions above)
2. **Wait for CodeQL scan** to complete
3. **Explore the alerts** in the Security tab
4. **Practice your demo** using the script above
5. **Record your presentation** (5 minutes)

Good luck with your demo! 🚀
