import os


class Config():
    SECRET_KEY = os.urandom(32)
    WTF_CSRF_ENABLED = False
