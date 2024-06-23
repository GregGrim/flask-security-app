from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

from models import user_datastore, db

app = Blueprint('auth', __name__)


@app.route('/after_login/')
@login_required
def after_login_redirect():
    if current_user.has_role('admin'):
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('index.index_page'))


@app.route('/after_register/')
@login_required
def after_register_redirect():
    default_role = user_datastore.find_role("user")
    user_datastore.add_role_to_user(current_user, default_role)
    db.session.commit()
    return redirect(url_for('index.index_page'))


@app.route('/after_logout/')
def after_logout_redirect():
    return redirect(url_for('security.login'))
