from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required

app = Blueprint('index', __name__)


@app.route('/')
@login_required
def index_page():
    return render_template('index.html')


@app.route('/after_logout/')
def after_logout_redirect():
    return redirect(url_for('security.login'))
