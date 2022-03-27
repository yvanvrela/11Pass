from . import views
from flask import Blueprint

# Ingresa la url /auth a todos los auth.
auth = Blueprint('auth', __name__, url_prefix='/auth')
