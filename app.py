from flask import Flask, request
import sqlite3
from cryptography.fernet import Fernet

app = Flask(__name__)

# Encryption setup
key = Fernet.generate_key()
cipher = Fernet(key)

# Database setup
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')

# Capability code
CAPABILITY_CODE = "SECURE123"

@app.route('/')
def home():
    return "Server Running Successfully!"

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    code = request.form.get('code')

    if code != CAPABILITY_CODE:
        return "Access Denied"

    encrypted_password = cipher.encrypt(password.encode())

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, encrypted_password))
    conn.commit()

    return "User Registered Securely"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']

    # SQL Injection Safe
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        return "User Exists (Safe Login Check)"
    else:
        return "User Not Found"

if __name__ == '__main__':
    app.run(debug=True)