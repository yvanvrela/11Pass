import unittest
from flask import(
    flash, make_response, redirect, render_template, url_for, request
)
from app import create_app
from flask_login import login_required, current_user

from app.forms import AccountForm, VaultForm
from app.sql_services import add_account, add_vault, all_account, get_accounts, get_vaults

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


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    # account_form = AccountForm()

    # if account_form.validate_on_submit():

    #     add_account(name=account_form.name.data,
    #                 id_vault=account_form.id_vault.data,
    #                 password=account_form.password.data,
    #                 page=account_form.page.data,
    #                 description=account_form.description.data)
    #     flash('Cuenta agregada', 'info')

    #     return redirect(url_for('accounts_page'))

    if request.method == 'GET':
        context = {
            'username': current_user.username,
            'vaults': get_vaults(),
            # 'accounts': get_accounts(),
        }
        return render_template('account.html', **context)
