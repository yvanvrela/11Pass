import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()


def add_account(name: str, password: str, page: str, description: str) -> None:
    """ Agrega los datos de la cuenta a la base de datos """
    
    sql = "INSERT INTO accounts \
            (name_element, password_element, page_element, description_element) \
            VALUES (?,?,?,?)"
    values = (name, password, page, description)

    cursor.execute(sql, values)
    connection.commit()

def update_account(account_id:int, name: str, password: str, page: str, description: str) -> None:
    sql = "UPDATE accounts  \
        SET  name_element = %s, password_element = %s, \
        page_element = %s, description_element = %s \
        WHERE id_account = %d"
    values = (name, password, page, description, account_id)
    cursor.execute(sql,values)
    connection.commit()

# add_account(name='facebook', password='12345',
#             page='face.com', description='dd'
#             )

cur = cursor.execute('SELECT * FROM accounts').fetchall()

print(cur)
