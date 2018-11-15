"""
Module to handle any logic
"""
from flask import request, jsonify
from flask.views import MethodView
from api.models.user_model import UserModel
from api.handlers.response_errors import ResponseErrors
from api.utils.validations import DataValidation


class UserController(MethodView):
    """
    Class with  methods to handle post and get methods for the user
    """
    user_name = None
    password = None
    user_data = UserModel()

    def post(self):
        """
        post method to handle posting a new user
        :return:
        """
        post_data = request.get_json()
        keys = ("user_name", "password")

        if not set(keys).issubset(set(post_data)):
            return ResponseErrors.missing_fields(keys)

        try:
            self.user_name = post_data['user_name'].strip()
            self.password = post_data['password'].strip()

        except AttributeError:
            return ResponseErrors.invalid_data_format()

        if not self.user_name or not self.password:
            return ResponseErrors.empty_data_fields()
        elif DataValidation.check_string_of_numbers(self.user_name) or \
                DataValidation.check_string_of_numbers(self.password):
            return ResponseErrors.invalid_data_format()

        current_user = self.user_data.register_user(self.user_name, self.password)
        response_object = {
            'message': 'Successfully registered',
            'data': current_user
        }
        return jsonify(response_object), 201




