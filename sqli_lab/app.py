# app.py
from flask import Flask, request, render_template_string, jsonify
import sqlite3
import logging
from datetime import datetime
import html

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attack_logs.log'),
        logging.StreamHandler()
    ]
)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    
    # Insert sample data
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)", 
                  ('admin', 'secret123', 'admin@example.com'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)", 
                  ('alice', 'password123', 'alice@example.com'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)", 
                  ('bob', 'bobpass', 'bob@example.com'))
    
    conn.commit()
    conn.close()

# Vulnerable SQL query function
def vulnerable_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string concatenation - SQL Injection vulnerable
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    log_attack(f"SQL Query executed: {query}", "SQL Injection Attempt")
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        log_attack(f"SQL Error: {str(e)}", "SQL Injection Error")
        conn.close()
        return None

# Safe parameterized query function
def safe_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SAFE: Parameterized query
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# Logging function
def log_attack(message, attack_type="Generic"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {attack_type} - {message} - IP: {request.remote_addr}"
    logging.info(log_entry)

# HTML templates
LOGIN_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Login</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 400px; margin: 0 auto; }
        input, button { width: 100%; padding: 10px; margin: 5px 0; }
        .vuln { background-color: #ffe6e6; padding: 10px; margin: 10px 0; }
        .safe { background-color: #e6ffe6; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Login System</h1>
        
        <div class="vuln">
            <h3>Vulnerable Login (SQL Injection)</h3>
            <form method="POST" action="/login-vulnerable">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login (Vulnerable)</button>
            </form>
        </div>

        <div class="safe">
            <h3>Safe Login (Parameterized)</h3>
            <form method="POST" action="/login-safe">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login (Safe)</button>
            </form>
        </div>

        <div>
            <h3>Search Users (Vulnerable)</h3>
            <form method="GET" action="/search">
                <input type="text" name="query" placeholder="Search users..." required>
                <button type="submit">Search</button>
            </form>
        </div>

        <div>
            <h3>Attack Examples</h3>
            <p>Try these SQL injection payloads:</p>
            <ul>
                <li><code>' OR '1'='1</code> - Basic bypass</li>
                <li><code>' UNION SELECT 1,2,3--</code> - Union attack</li>
                <li><code>admin'--</code> - Comment out password check</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

SEARCH_RESULTS = '''
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Search Results</h1>
    <a href="/">Back to Home</a>
    
    {% if users %}
        <h3>Found {{ users|length }} user(s):</h3>
        <table>
            <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Password</th>
                <th>Email</th>
            </tr>
            {% for user in users %}
            <tr>
                <td>{{ user[0] }}</td>
                <td>{{ user[1] }}</td>
                <td>{{ user[2] }}</td>
                <td>{{ user[3] }}</td>
            </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>No users found.</p>
    {% endif %}
    
    {% if error %}
        <p style="color: red;">Error: {{ error }}</p>
    {% endif %}
</body>
</html>
'''

# Routes
@app.route('/')
def index():
    return render_template_string(LOGIN_FORM)

@app.route('/login-vulnerable', methods=['POST'])
def login_vulnerable():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    log_attack(f"Vulnerable login attempt - Username: {username}, Password: {password}", "Login Attempt")
    
    user = vulnerable_login(username, password)
    
    if user:
        return f"<h1>Login Successful!</h1><p>Welcome {user[1]}!</p><a href='/'>Back</a>"
    else:
        return "<h1>Login Failed</h1><p>Invalid credentials</p><a href='/'>Back</a>"

@app.route('/login-safe', methods=['POST'])
def login_safe():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    log_attack(f"Safe login attempt - Username: {username}", "Safe Login")
    
    user = safe_login(username, password)
    
    if user:
        return f"<h1>Login Successful!</h1><p>Welcome {user[1]}!</p><a href='/'>Back</a>"
    else:
        return "<h1>Login Failed</h1><p>Invalid credentials</p><a href='/'>Back</a>"

@app.route('/search')
def search_users():
    query = request.args.get('query', '')
    
    if not query:
        return render_template_string(SEARCH_RESULTS, users=[])
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string concatenation in search
    search_query = f"SELECT * FROM users WHERE username LIKE '%{query}%' OR email LIKE '%{query}%'"
    
    log_attack(f"Search query: {search_query}", "Search SQL Injection")
    
    try:
        cursor.execute(search_query)
        users = cursor.fetchall()
        conn.close()
        return render_template_string(SEARCH_RESULTS, users=users)
    except Exception as e:
        log_attack(f"Search error: {str(e)}", "Search SQL Error")
        conn.close()
        return render_template_string(SEARCH_RESULTS, error=str(e), users=[])

@app.route('/logs')
def view_logs():
    try:
        with open('attack_logs.log', 'r') as f:
            logs = f.read()
        return f"<pre>{html.escape(logs)}</pre><a href='/'>Back</a>"
    except FileNotFoundError:
        return "<p>No logs found</p><a href='/'>Back</a>"

if __name__ == '__main__':
    init_db()
    print("Database initialized with sample data")
    print("Starting vulnerable server on http://localhost:5000")
    print("Access logs at http://localhost:5000/logs")
    app.run(debug=True, host='0.0.0.0', port=5000)