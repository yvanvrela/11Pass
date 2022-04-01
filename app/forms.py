from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
                           DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Ingresar')


class VaultForm(FlaskForm):
    vaultname = StringField('Nombre', validators=[
                            DataRequired()], render_kw={'autofocus': True})
    description = StringField('Descripción', widget=TextArea())

    submit = SubmitField('Crear')
