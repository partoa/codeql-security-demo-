import sqlite3
import os
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnerability 1: Hardcoded credentials
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
SECRET_TOKEN = "ghp_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"

@app.route('/search')
def search():
    """SQL Injection vulnerability"""
    query = request.args.get('q')
    db = sqlite3.connect('data.db')
    # VULNERABLE: SQL injection via f-string
    result = db.execute(f"SELECT * FROM users WHERE name = '{query}'")
    return str(result.fetchall())

@app.route('/execute')
def execute_command():
    """Command Injection vulnerability"""
    cmd = request.args.get('cmd')
    # VULNERABLE: Command injection
    os.system(cmd)
    return "Executed"

@app.route('/eval')
def eval_code():
    """Code Injection vulnerability"""
    code = request.args.get('code')
    # VULNERABLE: Code injection via eval
    result = eval(code)
    return str(result)

@app.route('/subprocess')
def run_subprocess():
    """Another command injection variant"""
    host = request.args.get('host')
    # VULNERABLE: Shell injection in subprocess
    subprocess.call(f'ping -c 1 {host}', shell=True)
    return "Pinging..."

@app.route('/render')
def render_template():
    """Server-Side Template Injection (SSTI)"""
    template = request.args.get('template')
    # VULNERABLE: SSTI
    return render_template_string(template)

@app.route('/file')
def read_file():
    """Path Traversal vulnerability"""
    filename = request.args.get('name')
    # VULNERABLE: Path traversal
    with open(f'/var/data/{filename}', 'r') as f:
        return f.read()

@app.route('/redirect')
def redirect_user():
    """Open Redirect vulnerability"""
    url = request.args.get('url')
    # VULNERABLE: Open redirect
    return f'<meta http-equiv="refresh" content="0;url={url}">'

@app.route('/deserialize')
def deserialize_data():
    """Unsafe Deserialization"""
    import pickle
    data = request.args.get('data')
    # VULNERABLE: Unsafe deserialization
    obj = pickle.loads(data.encode())
    return str(obj)

if __name__ == '__main__':
    # VULNERABLE: Debug mode enabled in production
    app.run(debug=True, host='0.0.0.0')
