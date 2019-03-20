from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SubmitField
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


class AddDelForm(FlaskForm):
    plus = SubmitField('+')
    sort = SubmitField('s')
    trash = SubmitField()


class NoteEditForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    text = TextAreaField()
    submit = SubmitField('Change')


class NoteCreateForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    text = TextAreaField()
    submit = SubmitField('Add note')