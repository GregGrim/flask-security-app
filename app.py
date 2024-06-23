import json

from flask import Flask
from flask_security import Security, hash_password
from flask_mail import Mail

from models import db
from admin import admin
from forms import ExtendedRegisterForm, LoginForm
from models import user_datastore

from blueprints.auth import app as auth_bp
from blueprints.main import app as main_bp


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config.from_file(filename="config.json", load=json.load)
    app.config.from_pyfile(filename="env.py")

    app.config["SECURITY_LOGIN_USER_FORM"] = LoginForm
    app.config["SECURITY_REGISTER_USER_FORM"] = ExtendedRegisterForm

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    mail = Mail(app)
    security = Security()

    db.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)

    return app


def _init_default_db_records():
    with app.app_context():
        db.create_all()
        user_datastore.find_or_create_role(name='admin')
        user_datastore.find_or_create_role(name='user')
        if not user_datastore.find_user(email=app.config.get('ADMIN_EMAIL')):
            user_datastore.create_user(email=app.config.get('ADMIN_EMAIL'),
                                       first_name='Admin',
                                       last_name='Admin',
                                       password=hash_password(app.config.get('ADMIN_PASSWORD')),
                                       roles=['admin'])
        db.session.commit()


app = create_app()
_init_default_db_records()


if __name__ == '__main__':
    app.run()
