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
                "secret_key" TEXT,
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
                "id_user"   INTEGER,
                "name"  TEXT UNIQUE,
                "description"	TEXT,
                FOREIGN KEY("id_user") REFERENCES "users"("id_user"),
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
                "id_user"       INTEGER,
                "id_vault"      INTEGER,
                "name_element"	TEXT UNIQUE,
                "password_element"	TEXT,
                "page_element"	TEXT,
                "description_element"	TEXT,
                FOREIGN KEY("id_user") REFERENCES "users"("id_user"),
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
        'secret_key': user[3],
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
                'secret_key': user[3],
            }
            return user


def add_user(username: str, password: str, secret_key: str) -> None:
    """Agregar un usuario a la bd, recibe username and password and secret_key"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f'INSERT INTO users (user_name, user_password, secret_key) VALUES (?,?,?)'
    values = username, password, secret_key
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


def add_vault(name: str, id_user: int, description: str) -> None:
    """ Agrega una Bóveda nueva a la base de datos """

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = ('INSERT INTO vaults (id_user, name, description) VALUES (?,?,?)')
    values = id_user, name, description
    cursor.execute(sql, values)

    conn.commit()
    conn.close()


def get_vaults(id_user: int) -> tuple:
    """ Busca todos los baules de la base de datos,
        que tenga el usuario.
        retorna una lista con sus nombres.
    """
    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = (f'SELECT id_vault, name FROM vaults WHERE id_user = {id_user}')
    vaults = cursor.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return vaults


def get_vault_by_name(name: str, id_user: int):

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f"SELECT name FROM vaults WHERE name = '{name}' AND id_user = {id_user}"
    data = cursor.execute(sql).fetchone()

    conn.commit()
    conn.close()

    return data


def get_vault_name(id_vault):

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = (f'SELECT name FROM vaults WHERE id_vault ={id_vault}')
    vaultname = cursor.execute(sql).fetchone()

    conn.commit()
    conn.close()

    return vaultname


def all_account(id_user: int) -> list:
    """Trae todas la cuentas de la tabla, segun el usuario"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f'SELECT * FROM accounts WHERE id_user={id_user}'
    list_accounts = cursor.execute(sql).fetchall()
    conn.commit()
    conn.close()

    return list_accounts


def account_items(id_user: int):
    """Trae la cantidad de cuentas del usuario en la base de datos"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f'SELECT COUNT(id_account) FROM accounts WHERE id_user={id_user}'
    cant = cursor.execute(sql).fetchone()
    conn.commit()
    conn.close()

    return cant


def get_accounts(id_vault):
    """ Retorna el id, nombre y la pagina de todas las cuentas
        que esten dentro de la bóveda.
        :param id_vault: Id de la boveda.
        :return Nombre y página
    """
    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f'SELECT id_account, name_element, page_element FROM accounts WHERE id_vault = {id_vault}'
    names = cursor.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return names


def get_account_by_id(id_account):

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f'SELECT name_element, page_element, password_element, description_element \
            FROM accounts WHERE id_account = {id_account}'
    details = cursor.execute(sql).fetchone()

    conn.commit()
    conn.close()

    return details


def get_account_by_name(name: str):

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f"SELECT name_element FROM accounts WHERE name_element = '{name}'"
    data = cursor.execute(sql).fetchone()

    conn.commit()
    conn.close()

    return data


def end_element_account() -> list:
    """Datos del ultimo elemento"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = "SELECT * FROM accounts ORDER BY accounts.id_account DESC LIMIT 1"
    end_element = cursor.execute(sql).fetchone()
    conn.commit()

    return end_element


def put_account(name: str, id_vault: int, password: str, page: str, description: str) -> None:
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
