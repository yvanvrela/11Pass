from multiprocessing import reduction
import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

def all_account() -> list:
    """Trae todas la cuentas de la tabla"""

    sql = "SELECT * FROM accounts"
    list_accounts = cursor.execute(sql).fetchall()
    connection.commit()

    return list_accounts

def end_element_account() -> list():
    """Datos del ultimo elemento"""

    sql = "SELECT * FROM accounts ORDER BY accounts.id_account DESC LIMIT 1"
    end_element = cursor.execute(sql).fetchone()
    connection.commit()

    return end_element

def add_account(name: str, password: str, page: str, description: str) -> None:
    """ Agrega los datos de la cuenta a la base de datos """
    
    sql = "INSERT INTO accounts \
            (name_element, password_element, page_element, description_element) \
            VALUES (?,?,?,?)"
    values = name, password, page, description
    cursor.execute(sql, values)
    connection.commit()


def update_account(account_id:int, name: str, password: str, page: str, description: str) -> None:
    """Actualiza los datos de la cuenta"""

    sql = "UPDATE accounts  \
        SET  name_element = ?, password_element = ?, \
        page_element = ?, description_element = ? \
        WHERE id_account = ?"
    values = name, password, page, description, account_id

    cursor.execute(sql, values)

    connection.commit()


def delete_account(account_id:int) -> None:
    """Eliminar la cuenta, de la bd"""

    sql = f"DELETE FROM accounts WHERE id_account= {account_id}"
    cursor.execute(sql)

    connection.commit()
