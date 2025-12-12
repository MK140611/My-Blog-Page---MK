from flask import Flask, render_template, request, redirect, url_for, flash, session, g

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for sessions and flash messages

# In-memory user storage (for demo purposes)
users = []

# Make the current user available globally in templates
@app.before_request
def load_current_user():
    g.current_user = session.get('user')


# Home route
@app.route('/')
def index():
    return render_template('index.html')


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        passwordConf = request.form.get('passwordConf', '')

        # Validation
        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if password != passwordConf:
            errors.append("Passwords do not match")

        # Check if username already exists
        if any(user['username'] == username for user in users):
            errors.append("Username already taken")

        if not errors:
            users.append({'username': username, 'email': email, 'password': password})
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))

    return render_template('register.html', errors=errors)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Find user
        user = next((u for u in users if u['username'] == username), None)
        if not user:
            errors.append("Username not found")
        elif user['password'] != password:
            errors.append("Incorrect password")

        if not errors:
            session['user'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))

    return render_template('login.html', errors=errors)


# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
