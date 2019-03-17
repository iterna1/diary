from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Open my diary')
    title = 'Open your personal diary'
    link = ('/init/register', 'Create')


class RegistrationForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Create my diary')
    title = 'Create your personal diary'
    link = ('/init/login', 'Open')
