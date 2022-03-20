import unittest
from flask import(
    flash, make_response, redirect, render_template, url_for
)
from app import create_app
from flask_login import login_required, current_user

app = create_app()


""" Comandos de testing """


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
