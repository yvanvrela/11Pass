from random import randint
import string
from cryptocode import encrypt, decrypt
import secrets


def secret_key_generator() -> str:
    """ Genera un codigo secreto, para todas las cuentas.
        Con simbolos, letras y numeros.
    """

    list_full = [secrets.token_hex(randint(2, 5)) for i in range(1, 4)]

    salida = list(
        map(lambda section: f'{section}{secrets.token_bytes(1)}', list_full))

    simbols = list(f'{string.punctuation}{string.ascii_uppercase}')

    simbols_len = len(simbols) - 1

    secret_key_list = []
    for section in range(0, randint(2, 4)):
        secret_key_list.append(
            f'ñ{simbols[randint(1,simbols_len)]}ñ{salida[randint(0,2)]}')

    secret_key = ''
    for key in secret_key_list:
        secret_key += f'{key}'

    return secret_key


def encrypt_data(secret_key: str, passkey: str) -> str:
    str_encoded = encrypt(secret_key, passkey)

    return str_encoded


def decrypt_data(str_encoded: str, passkey_reference: str) -> str:
    str_decoded = decrypt(str_encoded, passkey_reference)

    return str_decoded

