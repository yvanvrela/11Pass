from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Ingresar')

class VaultForm(FlaskForm):
    vaultname =  StringField('Nombre', validators=[DataRequired()])
    description = StringField('Descripción')

    submit = SubmitField('Crear')