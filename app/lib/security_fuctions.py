from ntpath import join
from random import randint
import random
import string
from cryptocode import encrypt, decrypt
import secrets


def secret_key_generator() -> str:
    """ 
        Retorna una cadena aleatoria con letras y numeros separados por giones.
        Genera un codigo secreto, para todas las cuentas.

        >>> secret_key_generator() #doctest:+SKIP
        'dId40-8c86d-Adfac-3ps'
    """

    # Se genera una lista de 4 elementos hexadecimales aleatorios con list_comprehensions
    list_full = [secrets.token_hex(randint(1, 2)) for i in range(1, 5)]

    list_secret_key = []

    # Cadena con las letras del abecedario más la ñ
    letters_upper = string.ascii_uppercase+'Ñ'+'ñ'

    for position in list_full:

        # Se trata la cadena agregando una letra mayuscula aleatoria al elemento según la posicion
        section = f'{position}{letters_upper[randint(0,27)]}'
        cant = len(section)

        # Se invierte el orden de la seccion segun su tamaño con random sample
        invert_order = random.sample(section, cant)
        section = ''.join(invert_order)

        # se agrega la cadena tratada a la lista de secret_key
        list_secret_key.append(section)

    cant_list_secret_key = len(list_secret_key)

    # Se crea la cadena final para el secret_key
    secret_key = ''

    #  Por cada posicion se agrega un guion para separar los elementos
    for position in range(cant_list_secret_key):

        if position == cant_list_secret_key-1:

            secret_key += f'{list_secret_key[position]}'

        else:

            secret_key += f'{list_secret_key[position]}-'

    return secret_key


def encrypt_data(secret_key: str, passkey: str) -> str:
    str_encoded = encrypt(secret_key, passkey)

    return str_encoded


def decrypt_data(str_encoded: str, passkey_reference: str) -> str:
    str_decoded = decrypt(str_encoded, passkey_reference)

    return str_decoded


def check_decrypt_data(secret_key, str_encode, passkey_reference):
    str_decoded = decrypt(str_encode, passkey_reference)

    if str_decoded == secret_key:
        return True
    else:
        return False
