import sqlite3
from sqlite3 import Error


def conection_db(db_file):
    """
        Crea la conexión a la base de datos con 
        SQLite database, especificamente con db_file.
        :param db_file: database file
        :return Connection object or None
    """

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table_users(db_file: str) -> None:
    """ Crea la tabla usuarios en la base de datos,
        si aún no existe. Indicando la base de datos
        especifica.
        :param db_file: archivo de la base de datos
        :return None
    """
    try:
        conn = conection_db(db_file=db_file)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
                "id_user"	INTEGER UNIQUE,
                "user_name"	TEXT UNIQUE,
                "user_password"	TEXT,
                PRIMARY KEY("id_user" AUTOINCREMENT)
            );""")
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def create_table_vault(db_file) -> None:
    """ Crea la tabla vaults en la base de datos,
        si aún no existe. Indicando la base de datos
        especifica.
        :param db_file: archivo de la base de datos
        :return None
    """
    try:
        conn = conection_db(db_file=db_file)
        cursor = conn.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS "vaults" (
                "id_vault"	INTEGER UNIQUE,
                "name"  TEXT,
                "description"	TEXT,
                PRIMARY KEY("id_vault" AUTOINCREMENT)
            );""")
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def create_table_accounts(db_file) -> None:
    """ Crea la tabla accounts en la base de datos,
        si aún no existe. Indicando la base de datos
        especifica.
        :param db_file: archivo de la base de datos
        :return None
    """
    try:
        conn = conection_db(db_file=db_file)
        cursor = conn.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS "accounts" (
                "id_account"	INTEGER UNIQUE,
                "id_vault"      INTEGER UNIQUE,
                "name_element"	TEXT,
                "password_element"	TEXT,
                "page_element"	TEXT,
                "description_element"	TEXT,
                FOREIGN KEY("id_vault") REFERENCES "vaults"("id_vault"),
                PRIMARY KEY("id_account" AUTOINCREMENT)
            );""")
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def get_user_by_id(user_id: int) -> dict:

    conn = conection_db(db_file='database.db')
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

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f'INSERT INTO users (user_name, user_password) VALUES (?,?)'
    values = username, password
    cursor.execute(sql, values)
    conn.commit()


def all_users() -> list:
    """Trae todos los usuarios de la bd"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = 'SELECT * FROM users'
    list_users = cursor.execute(sql).fetchall()
    conn.commit()

    return list_users


def add_vault(name: str, description: str) -> None:
    """ Agrega una Bóveda nueva a la base de datos """

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = ('INSERT INTO vaults (name, description) VALUES (?,?)')
    values = name, description
    cursor.execute(sql, values)

    conn.commit()
    conn.close()


def get_vaults() -> tuple:
    """ Busca todos los baules de la base de datos, 
        retorna una lista con sus nombres.
    """
    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = ('SELECT id_vault, name FROM vaults')
    vaults = cursor.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return vaults


def all_account() -> list:
    """Trae todas la cuentas de la tabla"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = 'SELECT * FROM accounts'
    list_accounts = cursor.execute(sql).fetchall()
    conn.commit()
    conn.close()

    return list_accounts


def get_accounts(id_vault):
    """ Retorna todas las cuentas que esten dentro de
        la bóveda.
        :param id_vault: Id de la boveda.
    """
    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f'SELECT name_element FROM accounts WHERE id_vault = {id_vault}'
    names = cursor.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return names


def end_element_account() -> list:
    """Datos del ultimo elemento"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = "SELECT * FROM accounts ORDER BY accounts.id_account DESC LIMIT 1"
    end_element = cursor.execute(sql).fetchone()
    conn.commit()

    return end_element


def add_account(name: str, id_vault: int, password: str, page: str, description: str) -> None:
    """ Agrega los datos de la cuenta a la base de datos """

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = "INSERT INTO accounts \
            (name_element, id_vault, password_element, page_element, description_element) \
            VALUES (?,?,?,?,?)"
    values = name, id_vault, password, page, description

    cursor.execute(sql, values)
    conn.commit()


def update_account(account_id: int, id_vault: int, name: str, password: str, page: str, description: str) -> None:
    """Actualiza los datos de la cuenta"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = "UPDATE accounts  \
        SET  name_element = ?, id_vault = ?,password_element = ?, \
        page_element = ?, description_element = ? \
        WHERE id_account = ?"
    values = name, id_vault, password, page, description, account_id

    cursor.execute(sql, values)
    conn.commit()


def delete_account(account_id: int) -> None:
    """Eliminar la cuenta, de la bd"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f"DELETE FROM accounts WHERE id_account= {account_id}"

    cursor.execute(sql)
    conn.commit()
