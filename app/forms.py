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


class VaultForm(FlaskForm):
    vaultname = StringField(
        'Nombre', [validators.DataRequired()], render_kw={'autofocus': True})
    description = TextAreaField('Descripcion', name='Descripcion_vault')

    submit = SubmitField('Agregar')


class AccountForm(FlaskForm):
    name = StringField('Nombre', [validators.DataRequired()], render_kw={
                       'autofocus': True})
    id_vault = StringField('id_vault')
    password = StringField('Password', [validators.DataRequired()])
    page = StringField('Página', [validators.DataRequired()])
    description = TextAreaField('Descripcion', name='Descripcion') 

    submit = SubmitField()
