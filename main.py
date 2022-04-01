from ast import Return
import unittest
from flask import(
    flash, make_response, redirect, render_template, url_for
)
from app import create_app
from flask_login import login_required, current_user

from app.forms import VaultForm

app = create_app()


""" Comandos de testing """


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.signup'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template('home.html')


@app.route('/vault', methods=['GET', 'POST'])
@login_required
def vault():

    vault_form = VaultForm()
    context = {
        'vault_form': vault_form,
    }

    if vault_form.validate_on_submit():

        flash('Bóveda creada', 'info')
        return url_for('home')

    return url_for('home')
