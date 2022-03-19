from urllib import response
from flask_testing import TestCase
from flask import current_app, url_for
import app

from main import create_app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLE'] = False
        app.config['DEBUG'] = True

        return app

