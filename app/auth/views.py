from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.lib.security_fuctions import check_decrypt_data, decrypt_data, encrypt_data, secret_key_generator
from app.models import UserData, UserModel
from . import auth
from app.forms import LoginForm, SignupForm
from app.sql_services import get_user_by_name, add_user


@auth.route('login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        secret_key = login_form.secret_key.data

        user_from_db = get_user_by_name(username=username)

        if user_from_db is not None:
            user_id_from_db = user_from_db['user_id']
            password_from_db = user_from_db['password']
            secret_key_from_db = user_from_db['secret_key']

            if check_password_hash(password_from_db, password):

                if check_decrypt_data(secret_key, secret_key_from_db, password):
                    user_data = UserData(
                        user_id=user_id_from_db,
                        username=username,
                        password=password,
                        secret_key=secret_key,
                    )
                    user = UserModel(user_data=user_data)

                    login_user(user)
                    flash('Bienvenido')

                    return redirect(url_for('home'))
                else:
                    flash('Secret key incorrecto', 'error')
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash(message='El usuario no existe', category='info')

    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth.login'))


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user_by_name(username)

        if user_doc is None:
            # Genera un id aleatorio
            #user_id = str(uuid.uuid4())
            password_hash = generate_password_hash(password)

            secret_key = secret_key_generator()
            secret_key_encrypt = encrypt_data(
                secret_key=secret_key, passkey=password)

            # user_data = UserData(
            #    user_id=user_id, username=username, password=password_hash)
            add_user(username=username, password=password_hash,
                     secret_key=secret_key_encrypt)

            user_from_db = get_user_by_name(username=username)

            user_data = UserData(
                user_id=user_from_db['user_id'],
                username=user_from_db['username'],
                password=user_from_db['password'],
                secret_key=secret_key,
            )

            user = UserModel(user_data)

            login_user(user)

            flash('Bienvenido!')

            context = {
                'secret_key': secret_key
            }

            # return redirect(url_for('home'))
            return render_template('secret.html', **context)
        else:
            flash('El usuario ya existe')

    return render_template('signup.html', **context)
