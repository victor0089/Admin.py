from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from myapp import routes
