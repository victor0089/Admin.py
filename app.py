from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager(app)
users = [
    {"id": 1, "username": "admin", "password": "admin123"},
    {"id": 2, "username": "user1", "password": "user123"},
    {"id": 3, "username": "user2", "password": "user456"},
]

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user['id'] == int(user_id):
            loaded_user = User()
            loaded_user.id = user['id']
            return loaded_user

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        action = request.form.get('action')

        if action == 'edit':
            return redirect(url_for('edit_user', user_id=user_id))
        elif action == 'delete':
            return delete_user(user_id)
        elif action == 'change_password':
            return redirect(url_for('change_password', user_id=user_id))

    return render_template('admin.html', users=users)

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user_to_edit = next((user for user in users if user['id'] == user_id), None)

    if user_to_edit is None:
        flash('User not found.', 'error')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        user_to_edit['username'] = request.form.get('username')
        flash('User edited successfully.', 'success')
        return redirect(url_for('admin'))

    return render_template('edit_user.html', user=user_to_edit)

@app.route('/admin/change_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    user_to_edit = next((user for user in users if user['id'] == user_id), None)

    if user_to_edit is None:
        flash('User not found.', 'error')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        user_to_edit['password'] = request.form.get('password')
        flash('Password changed successfully.', 'success')
        return redirect(url_for('admin'))

    return render_template('change_password.html', user=user_to_edit)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        new_user = {
            'id': len(users) + 1,
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }
        users.append(new_user)
        flash('User added successfully.', 'success')
        return redirect(url_for('admin'))

    return render_template('add_user.html')

@app.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = next((user for user in users if user['username'] == username and user['password'] == password), None)

        if user:
            login_user(User(), remember=True)
            flash('Login successful.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
