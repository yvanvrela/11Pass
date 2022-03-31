from multiprocessing import reduction
import sqlite3


def conection_db() -> None:
    """ Conecxion a la base de datos"""
    connection = sqlite3.connect('database.db')

    return connection

# TODO: crear las tablas


def create_users():
    pass


def get_user_by_id(user_id: int) -> dict:

    conn = conection_db()
    cursor = conn.cursor()
    sql = f'SELECT * FROM users WHERE id_user = {user_id}'
    user = cursor.execute(sql).fetchone()
    user = {
        'user_id': user[0],
        'username': user[1],
        'password': user[2],
    }
    conn.commit()

    return user


def get_user_by_name(username: str):
    user_form_db = all_users()

    for user in user_form_db:
        if username in user:
            user = {
                'user_id': user[0],
                'username': user[1],
                'password': user[2],
            }
            return user


def add_user(username: str, password: str) -> None:
    """Agregar un usuario a la bd, recibe username and password"""

    conn = conection_db()
    cursor = conn.cursor()

    sql = f'INSERT INTO users (user_name, user_password) VALUES (?,?)'
    values = username, password
    cursor.execute(sql, values)
    conn.commit()


def all_users() -> list:
    """Trae todos los usuarios de la bd"""

    conn = conection_db()
    cursor = conn.cursor()

    sql = 'SELECT * FROM users'
    list_users = cursor.execute(sql).fetchall()
    conn.commit()

    return list_users


def all_account() -> list:
    """Trae todas la cuentas de la tabla"""

    conn = conection_db()
    cursor = conn.cursor()

    sql = 'SELECT * FROM accounts'
    list_accounts = cursor.execute(sql).fetchall()
    conn.commit()

    return list_accounts


def end_element_account() -> list:
    """Datos del ultimo elemento"""

    conn = conection_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM accounts ORDER BY accounts.id_account DESC LIMIT 1"
    end_element = cursor.execute(sql).fetchone()
    conn.commit()

    return end_element


def add_account(name: str, password: str, page: str, description: str) -> None:
    """ Agrega los datos de la cuenta a la base de datos """

    conn = conection_db()
    cursor = conn.cursor()

    sql = "INSERT INTO accounts \
            (name_element, password_element, page_element, description_element) \
            VALUES (?,?,?,?)"
    values = name, password, page, description
    cursor.execute(sql, values)
    conn.commit()


def update_account(account_id: int, name: str, password: str, page: str, description: str) -> None:
    """Actualiza los datos de la cuenta"""

    conn = conection_db()
    cursor = conn.cursor()

    sql = "UPDATE accounts  \
        SET  name_element = ?, password_element = ?, \
        page_element = ?, description_element = ? \
        WHERE id_account = ?"
    values = name, password, page, description, account_id

    cursor.execute(sql, values)

    conn.commit()


def delete_account(account_id: int) -> None:
    """Eliminar la cuenta, de la bd"""

    conn = conection_db()
    cursor = conn.cursor()

    sql = f"DELETE FROM accounts WHERE id_account= {account_id}"
    cursor.execute(sql)

    conn.commit()
