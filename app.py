from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy data for demonstration purposes
users = [
    {"id": 1, "username": "admin", "password": "admin123"},
    {"id": 2, "username": "user1", "password": "user123"},
    {"id": 3, "username": "user2", "password": "user456"},
]

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/admin')
def admin():
    return render_template('admin.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
