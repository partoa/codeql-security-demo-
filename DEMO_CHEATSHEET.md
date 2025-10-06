# Semgrep Demo Cheatsheet

**Quick reference for your 5-minute demo presentation.**

---

## 🔧 Setup Commands (Run Before Demo)

```bash
cd /home/partoa/work/CodeQL
source venv/bin/activate
```

---

## 🎬 Demo Commands (In Order)

### 1. Initial Scan (Show 11 Vulnerabilities)

```bash
semgrep --config=semgrep-rules.yaml vulnerable_app.py
```

**Expected output**: 11 findings in beautiful colored format

---

### 2. Show Custom Rules File

```bash
cat semgrep-rules.yaml
```

**Talking points**: 
- YAML format (easy!)
- Pattern looks like actual code
- Metavariables like `$VAR`
- Detailed remediation messages

---

### 3. Show Vulnerable Code

```bash
cat vulnerable_app.py
```

**Point out**:
- Line 20: SQL injection
- Line 27: Command injection
- Line 9-11: Hardcoded secrets

---

### 4. Semgrep Playground Demo

**URL**: https://semgrep.dev/playground

**Left Panel** (paste this rule):
```yaml
rules:
  - id: sql-injection-demo
    pattern: db.execute(f"... {$VAR} ...")
    message: SQL injection found!
    severity: ERROR
    languages: [python]
```

**Middle Panel** (paste this code):
```python
query = request.args.get('q')
db.execute(f"SELECT * FROM users WHERE name = '{query}'")
```

**Right Panel**: Shows match highlighted in real-time! ✨

---

### 5. Advanced Pattern (Optional)

**Show taint tracking capability:**

```yaml
mode: taint
pattern-sources:
  - pattern: request.args.get(...)
pattern-sinks:
  - pattern: db.execute(...)
```

**Talking point**: "This traces user input through the entire application, just like CodeQL!"

---

### 6. JSON Output (Optional - for CI/CD discussion)

```bash
semgrep --config=semgrep-rules.yaml vulnerable_app.py --json | jq '.results | length'
```

**Output**: 11

**Talking point**: "Perfect for CI/CD pipelines and automated security gates"

---

## 🎯 Key Talking Points

### Why Semgrep?

1. **Fast**: 11 findings in 2 seconds
2. **Easy**: Rules in YAML, not complex query language
3. **Local**: No cloud service needed
4. **Visual**: Playground shows matches in real-time
5. **Powerful**: Taint tracking, auto-fix, CI integration

### vs CodeQL

| Feature | CodeQL | Semgrep |
|---------|--------|---------|
| Setup | 30+ min | 30 sec |
| Rules | QL (hard) | YAML (easy) |
| Speed | Minutes | Seconds |
| Platform | GitHub | Independent |

---

## 📊 Vulnerabilities to Highlight

### Critical (emphasize these 3)

1. **SQL Injection** (Line 20)
   - Shows f-string interpolation danger
   - Easy to exploit: `?q=' OR '1'='1`

2. **Command Injection** (Line 27)
   - Direct `os.system()` call
   - Attack: `?cmd=rm -rf /`

3. **Hardcoded Secrets** (Lines 9-11)
   - OpenAI API key: `sk-...`
   - GitHub token: `ghp_...`
   - Shows pattern matching power

---

## 🗣️ Demo Script Outline

**[0:00-0:45]** Hook
- "Find vulnerabilities in seconds, not hours"
- Show Semgrep scan → 11 findings instantly

**[0:45-1:30]** What is Semgrep
- Pattern-based matching
- Metavariables
- Runs locally

**[1:30-2:45]** Custom Rules (IMPRESSIVE PART)
- Open Semgrep Playground
- Live coding a rule
- Show real-time matching

**[2:45-3:45]** Advanced Features
- Taint tracking
- Auto-fix
- CI/CD integration

**[3:45-4:45]** Real-World Usage
- Pre-commit hooks
- VS Code integration
- Cost comparison ($0 vs $500/mo)

**[4:45-5:00]** Closing
- Recap key points
- "Go scan your code!"

---

## 🚨 Common Issues & Fixes

**Terminal colors not showing?**
- Windows: Use Windows Terminal or WSL
- Mac/Linux: Should work by default

**Semgrep command not found?**
```bash
source venv/bin/activate
```

**No findings?**
- Check you're in the right directory
- Verify file name: `vulnerable_app.py`

---

## 📝 Backup Talking Points

If you run out of things to say:

1. **Open Source**: "Used by Snowflake, GitLab, Dropbox"
2. **Community Rules**: "10,000+ rules from security community"
3. **Multi-Language**: "Works with Python, JS, Java, Go, C++..."
4. **Auto-Fix**: "Can automatically fix vulnerabilities"
5. **VS Code**: "Has real-time IDE integration"

---

## 🎤 Opening Lines (Choose One)

1. "How do you find security vulnerabilities in seconds instead of hours?"
2. "What if code scanning didn't require GitHub or cloud services?"
3. "I'm going to show you the fastest way to find security bugs in your code"
4. "Traditional security tools take minutes and cost money. Let me show you something better."

---

## 🎬 Closing Lines (Choose One)

1. "Now go secure your code!"
2. "Thanks for watching - your code just got safer!"
3. "That's Semgrep - instant security at your fingertips!"
4. "Questions? Try it yourself at semgrep.dev/playground!"

---

## 📱 URLs to Bookmark

- **Playground**: https://semgrep.dev/playground
- **Docs**: https://semgrep.dev/docs/
- **Rules**: https://semgrep.dev/r
- **Your Repo**: https://github.com/partoa/codeql-security-demo-

---

**Good luck with your demo! 🎉**
