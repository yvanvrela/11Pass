from flask_login import UserMixin

from app.lib.security_fuctions import decrypt_data
from .sql_services import get_user_by_name, get_user_by_id


class UserData:
    def __init__(self, user_id, username, password, secret_key):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.secret_key = secret_key


class UserModel(UserMixin):
    def __init__(self, user_data):
        """UserData"""
        self.id = user_data.user_id
        self.username = user_data.username
        self.password = user_data.password
        self.secret_key = user_data.secret_key

    # @staticmethod  # no recibe self
    # def query(user_name):
    #     user_doc = get_user_by_name(user_name)  # Trae el usuario, si existe

    #     # Nueva instancia de UserData, busca en la bd si existe el usuario
    #     user_data = UserData(
    #         user_id=user_doc['user_id'],
    #         username=user_doc['username'],
    #         password=user_doc['password'],
    #         secret_key= self.secret),
    #     )

    #     return UserModel(user_data)

    @staticmethod  # no recibe self
    def queryId(user_id):
        user_doc = get_user_by_id(user_id)  # Trae el usuario, si existe

        # Nueva instancia de UserData, busca en la bd si existe el usuario
        user_data = UserData(
            user_id=user_doc['user_id'],
            username=user_doc['username'],
            password=user_doc['password'],
            secret_key= user_doc['secret_key'],
        )

        return UserModel(user_data)
