from multiprocessing import connection
from time import sleep
from urllib import response
from flask_testing import TestCase
from flask import current_app, url_for
import sqlite3

from main import app
from app.sql_services import all_account, end_element_account,add_account, update_account, delete_account


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLE'] = False
        app.config['DEBUG'] = True

        return app


    def test_app_exists(self):
        self.assertIsNotNone(current_app)


    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])


    def test_sql_add(self): 
        add_account(name='prueba', password='123', page='page', description='description')
        account_reference = f'Cuenta agregada: {end_element_account()}'
        
        return print(account_reference)
        
        
    
    def test_sql_update(self):
        account_id = end_element_account()[0]
        update_account(account_id= account_id, name='editado', password='1235', page='web', description='test')

        return print(f'Cuenta editada: {end_element_account()}')

        
    def test_sql_delete(self):
        account_id = end_element_account()
        account_reference = f'Cuenta eliminada: {account_id}'

        delete_account(account_id= account_id[0])

        return print(account_reference)

        
         

        