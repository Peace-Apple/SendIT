"""
Module for the user
"""


class UserModel:
    """
    Model to hold store users using data structures
    """
    increment = 0

    def __init__(self, user_name=None, password=None):

        """
        User model template
        :param user_name:
        :param password:
        """
        self.user_name = user_name
        self.password = password
        self.user_id = None

    def register_user(self, user_name=None, password=None):
        """
        Register new user
        :param user_name:
        :param password:
        :return:
        """
        self.increment += 1
        current_user = UserModel(user_name, password)
        current_user.user_id = self.increment

        new_user = {
            'user_id': current_user.user_id,
            'user_name': current_user.user_name,
        }
        self.users.append(new_user)
        return new_user

    users = []
