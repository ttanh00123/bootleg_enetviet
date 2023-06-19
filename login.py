from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# List of users and their credentials
users = [
    {'username': 'user1', 'password': generate_password_hash('password1'), 'is_admin': False},
    {'username': 'user2', 'password': generate_password_hash('password2'), 'is_admin': False},
    {'username': 'admin', 'password': generate_password_hash('adminpassword'), 'is_admin': True}
]

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users if u['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['is_admin'] = user['is_admin']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    else:
        return render_template('login.html')

# Home page
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'], is_admin=session['is_admin'])
    else:
        return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

# Admin page
@app.route('/admin')
def admin():
    if 'username' in session and session['is_admin']:
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)