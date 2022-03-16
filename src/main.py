import unittest
from .app import create_app

app = create_app()


@app.cli.command()
def test() -> None:
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(test=tests)
