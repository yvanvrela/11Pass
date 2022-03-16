import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()


def add_account(name: str, password: str, page: str, description: str) -> None:
    """ Agrega los datos de la cuenta a la base de datos """
    cursor.execute("""INSERT INTO accounts 
        (name_element, password_element, page_element, description_element)
        VALUES (?,?,?,?)""", (name, password, page, description))
    connection.commit()


# add_account(name='facebook', password='12345',
#             page='face.com', description='dd'
#             )

cur = cursor.execute('SELECT * FROM accounts').fetchall()

print(cur)
