import os


class Config():
    SECRET_KEY = os.environ['SECRET_KEY']
    WTF_CSRF_ENABLED = False
