from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

@app.route('/search')
def search():
    # SQL Injection vulnerability
    query = request.args.get('q')
    db = sqlite3.connect('data.db')
    result = db.execute("SELECT * FROM products WHERE name = '" + query + "'")
    return str(result.fetchall())

@app.route('/ping')
def ping():
    # Command Injection vulnerability  
    host = request.args.get('host')
    os.system('ping ' + host)
    return 'Pinging...'

@app.route('/admin')
def admin():
    # Hardcoded credentials
    username = 'admin'
    password = 'password123'
    
    if request.args.get('user') == username and request.args.get('pass') == password:
        return 'Admin access granted'
    return 'Access denied'

@app.route('/file')
def read_file():
    # Path traversal vulnerability
    filename = request.args.get('name')
    with open('/var/data/' + filename, 'r') as f:
        return f.read()

@app.route('/redirect')
def redirect_user():
    # Open redirect vulnerability
    url = request.args.get('url')
    return f'<meta http-equiv="refresh" content="0;url={url}">'

if __name__ == '__main__':
    app.run(debug=True)
