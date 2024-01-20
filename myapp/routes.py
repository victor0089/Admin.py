from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from myapp import app, login_manager
from myapp.forms import LoginForm


# Dummy user data for demonstration purposes
users = [
    {"id": 1, "username": "admin", "password": "admin123"},
    {"id": 2, "username": "user1", "password": "user123"},
    {"id": 3, "username": "user2", "password": "user456"},
]

class User:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']

@login_manager.user_loader
def load_user(user_id):
    for user_data in users:
        if user_data['id'] == int(user_id):
            return User(user_data)
# ....
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = next((user_data for user_data in users if user_data['username'] == username and user_data['password'] == password), None)

        if user:
            login_user(User(user))
            flash('Login successful.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html', form=form)
