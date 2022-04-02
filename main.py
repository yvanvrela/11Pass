from ast import Return
import unittest
from flask import(
    flash, make_response, redirect, render_template, url_for
)
from app import create_app
from flask_login import login_required, current_user

from app.forms import VaultForm
from app.sql_services import add_vault, get_vaults

app = create_app()


""" Comandos de testing """


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    vault_form = VaultForm()
    username = current_user.username

    context = {
        'vaults': get_vaults(),
        'vault_form': vault_form,
        'username': username,
    }

    return render_template('home.html', **context)


@app.route('/vault', methods=['GET', 'POST'])
@login_required
def vault():

    vault_form = VaultForm()

    if vault_form.validate_on_submit():
        add_vault(name=vault_form.vaultname.data,
                  description=vault_form.description.data)
        flash('Bóveda creada', 'info')

        return redirect(url_for('home'))

    return redirect(url_for('home'))
