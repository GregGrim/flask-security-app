from flask_security.forms import RegisterForm, EmailField
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(message='Your first name is required.'), Length(max=255)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(message='Your last name is required.'), Length(max=255)])
    phone_number = StringField('Phone Number',
                               validators=[DataRequired(message='Your phone number is required.'), Length(max=50)])


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
