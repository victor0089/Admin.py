from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from myapp import app, login_manager
from myapp.forms import LoginForm

# ... (Your routes go here)
