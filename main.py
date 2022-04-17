import unittest
from flask import(
    flash, make_response, redirect, render_template, url_for, request
)
from app import create_app
from flask_login import login_required, current_user

from app.forms import AccountForm, VaultForm
from app.lib.security_fuctions import decrypt_data, encrypt_data
from app.sql_services import account_items, add_vault,  delete_account, delete_vault, get_account_by_id, get_account_by_name, get_accounts, get_vault_by_name, get_vault_name, get_vaults, put_account, update_account, update_vault

app = create_app()

LOGIN_MESSAGE = 'Inicia sesión, para acceder a la página'

""" Comandos de testing """


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


""" Manejos de errores"""


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def not_found(error):
    # se debe usar una variable abort o que nada funcione
    return render_template('500.html', error=error)


"""Rutas"""


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.login'))


@app.route('/vaults', methods=['GET', 'POST'])
@login_required
def home():
    vault_form = VaultForm()
    username = current_user.username
    id_user = current_user.id
    context = {
        'vaults': get_vaults(id_user=id_user),
        'vault_form': vault_form,
        'username': username,
        'items': account_items(id_user=id_user),
    }

    return render_template('home.html', **context)


@app.route('/vault/add', methods=['GET', 'POST'])
@login_required
def vault():

    vault_form = VaultForm()
    id_user = current_user.id

    if vault_form.validate_on_submit():

        vault_reference = get_vault_by_name(
            name=vault_form.vaultname.data, id_user=id_user)

        if vault_reference is None:

            add_vault(
                name=vault_form.vaultname.data,
                id_user=id_user,
                description=vault_form.description.data
            )

            flash('Bóveda creada', 'info')

            return redirect(url_for('home'))

        flash('La bóveda ya existe.')

    return redirect(url_for('home'))


@app.route('/vault/edit/<id_vault>', methods=['GET', 'POST'])
@login_required
def edit_vault(id_vault):

    vault_form = VaultForm()
    id_user = current_user.id

    if vault_form.validate_on_submit():

        update_vault(
            name=vault_form.vaultname.data,
            id_user=id_user,
            description=vault_form.description.data,
            id_vault=id_vault
        )

        flash('Bóveda editada', 'info')

        return redirect(url_for('account', id_vault=id_vault))


@app.route('/vault/delete/<id_vault>', methods=['GET', 'POST'])
@login_required
def del_vault(id_vault):

    delete_vault(id_vault=id_vault)

    flash('Bóveda eliminada.')

    return redirect(url_for('home'))


@app.route('/vaults/<id_vault>', methods=['GET', 'POST'])
@login_required
def account(id_vault):

    account_form = AccountForm()
    vault_form = VaultForm()
    id_user = current_user.id

    context = {
        'username': current_user.username,
        'items': account_items(id_user=id_user),
        'accounts': get_accounts(id_vault=id_vault),
        'vaults': get_vaults(id_user=id_user),
        'id_vault': id_vault,
        'vaultname': get_vault_name(id_vault=id_vault),
        'account_form': account_form,
        'vault_form': vault_form,
    }

    return render_template('account.html', **context)


@app.route('/account/add', methods=['POST', 'GET'])
@login_required
def add_account():

    account_form = AccountForm()
    id_user = current_user.id
    secret_key_reference = current_user.secret_key

    id_vault_reference = account_form.id_vault.data

    if account_form.validate_on_submit():

        account_reference = get_account_by_name(
            account_form.name.data, id_user=id_user, id_vault=id_vault_reference)

        if account_reference is None:

            password = account_form.password.data

            # encriptar la contraseña
            password_encrypt = encrypt_data(
                secret_key=password, passkey=secret_key_reference)

            put_account(
                name=account_form.name.data,
                id_user=id_user,
                id_vault=id_vault_reference,
                username=account_form.username.data,
                password=password_encrypt,
                page=account_form.page.data,
                description=account_form.description.data
            )

            flash('Cuenta agregada', 'info')

            return redirect(url_for('account', id_vault=id_vault_reference))

        flash('El nombre de la cuenta ya existe.')

        return redirect(url_for('account', id_vault=id_vault_reference))


@app.route('/account/edit/<id_account>', methods=['GET', 'POST'])
@login_required
def edit_account(id_account):
    account_form = AccountForm()
    id_user = current_user.id
    secret_key_reference = current_user.secret_key

    id_vault = account_form.id_vault.data

    if account_form.validate_on_submit():

        password_encrypt = encrypt_data(
            secret_key=account_form.password.data, passkey=secret_key_reference)

        update_account(
            account_id=id_account,
            id_user=id_user,
            id_vault=account_form.id_vault.data,
            name=account_form.name.data,
            username=account_form.username.data,
            password=password_encrypt,
            page=account_form.page.data,
            description=account_form.description.data
        )

        flash('Cuenta editada')
        return redirect(url_for('details_account', id_vault=id_vault, id_account=id_account))


@app.route('/account/delete/<id_vault>/<id_account>', methods=['GET', 'POST'])
@login_required
def del_account(id_account, id_vault):
    id_vault_reference = id_vault

    delete_account(account_id=id_account)
    flash('Cuenta eliminada')

    return redirect(url_for('account', id_vault=id_vault_reference))


@app.route('/vaults/<id_vault>/<id_account>', methods=['POST', 'GET'])
@login_required
def details_account(id_vault, id_account):

    secret_key_reference = current_user.secret_key
    id_vault_reference = id_vault

    # Desencripta la contraseña para mostrarla
    details_account = get_account_by_id(id_account=id_account)
    details_account.update({'password': decrypt_data(
        str_encoded=details_account['password'], passkey_reference=secret_key_reference)})

    id_user = current_user.id

    vault_form = VaultForm()
    account_form = AccountForm()

    context = {
        'username': current_user.username,
        'items': account_items(id_user=id_user),
        'accounts': get_accounts(id_vault=id_vault),
        'details_account': details_account,
        'vaults': get_vaults(id_user=id_user),
        'id_vault': id_vault_reference,
        'vaultname': get_vault_name(id_vault=id_vault),
        'vault_form': vault_form,
        'account_form': account_form,
    }

    return render_template('account_detail.html', **context)
