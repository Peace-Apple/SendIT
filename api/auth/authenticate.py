from api.models.user_model import Users
from werkzeug.security import generate_password_hash


class Authenticate:

    myUser = Users()

    @staticmethod
    def hash_password(password):
        """
        method to hash password
        :param password:
        :return:
        """
        try:
            return generate_password_hash(password, method="sha256")

        except ValueError:
            return False
