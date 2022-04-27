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
                "name"  TEXT,
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
                "name_element"	TEXT,
                "username_element" TEXT,
                "password_element"	TEXT,
                "page_element"	TEXT,
                "description_element"	TEXT,
                "favorite_element" INTEGER,
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
    if user is not None:
        user = {
            'user_id': user[0],
            'username': user[1],
            'password': user[2],
            'secret_key': user[3],
        }
        conn.commit()

        return user
    else:
        return None


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


def update_user(id_user: int, username: str, password: str) -> None:
    """ Actualizar datos del usuario """

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f"UPDATE users SET user_name='{username}', user_password='{password}' WHERE id_user={id_user}"
    cursor.execute(sql)

    conn.commit()
    conn.close()


def delete_user(id_user: int) -> None:
    """Elimina el usuario, todas sus bovedas y cuentas de la bd"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    exists_account = all_account(id_user=id_user)
    exists_vault = get_vaults(id_user=id_user)

    if exists_account:
        sql = f"DELETE FROM accounts WHERE id_user= {id_user}"
        cursor.execute(sql)

    if exists_vault:
        sql = f"DELETE FROM vaults WHERE id_user= {id_user}"
        cursor.execute(sql)

    sql = f"DELETE FROM users WHERE id_user= {id_user}"
    cursor.execute(sql)

    conn.commit()
    conn.close()


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


def update_vault(id_vault: int, name: str, id_user: int, description: str) -> None:
    """ Edita la bóveda en la base de datos """

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = "UPDATE vaults SET  id_user = ?, name = ?, description = ? WHERE id_vault = ?"
    values = id_user, name, description, id_vault
    cursor.execute(sql, values)

    conn.commit()
    conn.close()


def delete_vault(id_vault: int) -> None:
    """Elimina la bovéda y todas sus cuentas de la bd"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f"DELETE FROM accounts WHERE id_vault= {id_vault}"
    cursor.execute(sql)

    sql = f"DELETE FROM vaults WHERE id_vault= {id_vault}"
    cursor.execute(sql)

    conn.commit()
    conn.close()


def get_vaults(id_user: int) -> tuple:
    """ Busca todos los baules de la base de datos,
        que tenga el usuario.
        retorna una lista con sus nombres.
    """
    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = (
        f'SELECT id_vault, name FROM vaults WHERE id_user = {id_user} ORDER BY name')
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

    sql = (f'SELECT name, description FROM vaults WHERE id_vault ={id_vault}')
    vaultname = cursor.execute(sql).fetchone()

    conn.commit()
    conn.close()

    return vaultname


def all_account(id_user: int) -> list:
    """Trae todas la cuentas de la tabla, segun el usuario"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f'SELECT * FROM accounts WHERE id_user={id_user} ORDER BY name_element'
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
    """ Retorna el id, nombre, el username o email y la pagina de todas las cuentas
        que esten dentro de la bóveda, ordenados alfabeticamente.
        :param id_vault: Id de la boveda.
        :return Nombre y página
    """
    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f'SELECT id_account, name_element, username_element FROM accounts WHERE id_vault = {id_vault} ORDER BY name_element'
    names = cursor.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return names


def get_account_by_id(id_account):

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f'SELECT name_element, username_element, page_element, password_element, description_element,  \
            id_vault, id_account, favorite_element FROM accounts WHERE id_account = {id_account}'
    details = cursor.execute(sql).fetchone()

    details = {
        'name': details[0],
        'username': details[1],
        'page': details[2],
        'password': details[3],
        'description': details[4],
        'id_vault': details[5],
        'id_account': details[6],
        'favorite': details[7],
    }

    conn.commit()
    conn.close()

    return details


def get_favorite_by_id(id_account):

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f'SELECT name_element, username_element, page_element, password_element, description_element,  \
            id_vault, id_account, favorite_element FROM accounts WHERE id_account = {id_account} and favorite_element = 1'
    details = cursor.execute(sql).fetchone()

    if details == None:
        conn.commit()
        conn.close()

        return False
    else:
        details = {
            'name': details[0],
            'username': details[1],
            'page': details[2],
            'password': details[3],
            'description': details[4],
            'id_vault': details[5],
            'id_account': details[6],
            'favorite': details[7],
        }

        conn.commit()
        conn.close()

        return details


def get_account_by_name(name: str, id_user: int, id_vault: int):

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f"SELECT name_element FROM accounts WHERE name_element = '{name}' AND id_user = {id_user} AND id_vault = {id_vault}"
    data = cursor.execute(sql).fetchone()

    conn.commit()
    conn.close()

    return data


def get_favorite_accounts(id_user: int) -> list:
    """ Retorna todas las cuentas favoritas del usuario.
        :param id_account id_user
        :return Lista de favoritos 
    """

    conn = conection_db('database.db')
    cursor = conn.cursor()

    sql = f'SELECT id_account, id_vault, name_element, username_element FROM accounts WHERE favorite_element = 1 AND id_user = {id_user} ORDER BY name_element'

    favorites = cursor.execute(sql).fetchall()

    favorites_list = []

    for account in favorites:
        favorites_list.append(
            {
                'name': account[2],
                'detail': {
                    'id_account': account[0],
                    'id_vault': account[1],
                    'id_user': id_user,
                    'username': account[3],
                },
            }
        )

    conn.commit()
    conn.close()

    return favorites_list


def update_favorite(data: int, id_account: int) -> None:

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = "UPDATE accounts SET favorite_element = ? WHERE id_account = ?"
    value = data, id_account

    cursor.execute(sql, value)
    conn.commit()


def end_element_account(id_user: int) -> list:
    """Datos del ultimo elemento"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f"SELECT * FROM accounts ORDER BY accounts.id_account DESC LIMIT 1 WHERE id_user = {id_user}"
    end_element = cursor.execute(sql).fetchone()
    conn.commit()

    return end_element


def put_account(name: str, id_user: int, id_vault: int, username: str, password: str, page: str, description: str, favorite: int) -> None:
    """ Agrega los datos de la cuenta a la base de datos """

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = "INSERT INTO accounts \
            (name_element, id_user, id_vault, username_element, password_element, page_element, description_element, favorite_element) \
            VALUES (?,?,?,?,?,?,?,?)"
    values = name, id_user, id_vault, username, password, page, description, favorite

    cursor.execute(sql, values)
    conn.commit()


def update_account(account_id: int, id_user: int, id_vault: int, name: str, username: str, password: str, page: str, description: str) -> None:
    """Actualiza los datos de la cuenta"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = "UPDATE accounts  \
        SET  name_element = ?, id_user = ?, id_vault = ?, username_element = ?, password_element = ?, \
        page_element = ?, description_element = ? \
        WHERE id_account = ?"
    values = name, id_user, id_vault, username, password, page, description, account_id

    cursor.execute(sql, values)
    conn.commit()


def delete_account(account_id: int) -> None:
    """Eliminar la cuenta, de la bd"""

    conn = conection_db(db_file='database.db')
    cursor = conn.cursor()

    sql = f"DELETE FROM accounts WHERE id_account= {account_id}"

    cursor.execute(sql)
    conn.commit()
