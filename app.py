from flask import Flask, request, render_template, redirect, url_for, flash, session
from datetime import datetime
import os
import secrets
import logging
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a more secure place for credential logs
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, 'log.txt')


# Dummy credentials for validation
VALID_USERNAME = "user"
VALID_PASSWORD = "pass"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Log login attempt
        user_agent = request.headers.get('User-Agent')
        ip = request.remote_addr
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_path, 'a') as f:
            f.write(f"[{timestamp}] IP: {ip} | User: {username} | Pass: {password} | Agent: {user_agent}\n")
        
        logging.info(f"Login attempt for user: {username} from IP: {ip}")
        
        # Validate credentials
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return redirect(url_for('dashboard'))  # Redirect to dashboard on success
        else:
            return render_template('error.html'), 401 # Return 401 on failure

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found", 404

@app.errorhandler(500)
def server_error(e):
    return "500 Internal Server Error", 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
