from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms import validators


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', [
                           validators.DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', [validators.DataRequired()])
    secret_key = StringField('Secret_key', [validators.DataRequired()])

    submit = SubmitField('Ingresar')


class SignupForm(FlaskForm):
    username = StringField('Nombre de usuario', [
                           validators.DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', [validators.DataRequired()])

    submit = SubmitField('Registrarse')

class UserForm(FlaskForm):
    username = StringField('username', [validators.DataRequired()])
    password_reference = PasswordField(id='user-password', validators=[validators.DataRequired()])
    new_password = PasswordField(id='new-password', validators=[validators.DataRequired()])

    submit = SubmitField(id='submit-user')

class VaultForm(FlaskForm):
    vaultname = StringField(
        'Nombre', [validators.DataRequired()], render_kw={'autofocus': True})
    description = TextAreaField('Descripcion', name='Descripcion_vault')

    submit = SubmitField()


class AccountForm(FlaskForm):
    name = StringField('Nombre', [validators.DataRequired()], render_kw={
                       'autofocus': True})
    id_vault = StringField('id_vault')
    username = StringField('Username', [validators.DataRequired()])
    password = StringField('Password', [validators.DataRequired()])
    page = StringField('Página', [validators.DataRequired()])
    description = TextAreaField('Descripcion', name='Descripcion')

    submit = SubmitField(id='submit-form')
