"""
Module for the user
"""

from api.models.database import DatabaseConnection


class UserModel:
    """
    Model to hold user data by storing it in the database
    """

    def __init__(self, user_name=None, email=None, phone_number=None, password=None):

        """
        User model template
        :param user_name:
        :param email:
        :param phone_number:
        :param password:
        """
        self.user_name = user_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.user_type = None
        self.user_id = None


class Users:
    """
    Define user module attributes accessed by callers
    """
    data = DatabaseConnection()

    def register_user(self, user_name=None, email=None, phone_number=None, password=None):
        """
        Register new user
        :param user_name:
        :param email:
        :param phone_number:
        :param password:
        :return:
        """
        user = UserModel(user_name, email, phone_number, password)
        self.data.insert_user(user_name, email, phone_number, password)

        del user.user_id

        return user
