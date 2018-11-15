"""
Module to handle any logic
"""
from flask import request, jsonify
from flask.views import MethodView
from api.models.user_model import UserModel
from api.handlers.response_errors import ResponseErrors


class LoginController(MethodView):
    """
    User login class
    """
    user_name = None
    password = None
    user_id = None
    data = UserModel()

    def post(self):
        # to get post data
        post_data = request.get_json()

        keys = ('user_name', 'password', 'user_id')
        if not set(keys).issubset(set(post_data)):
            return ResponseErrors.missing_fields(keys)

        try:
            self.user_name = post_data.get('user_name').strip()
            self.password = post_data.get('password').strip()
            self.user_id = post_data.get('user_id')
        except AttributeError:
            return ResponseErrors.invalid_data_format()

        if not self.user_name or not self.password or not self.user_id:
            return ResponseErrors.empty_data_fields()

        users = self.data.get_all_users()
        print(self.data.get_all_users())

        for single_user in users:
            if self.user_id == single_user['user_id']:

                response_object = {
                    'status': 'success',
                    'message': 'You are logged in',
                    'logged_in_as': single_user
                }

                return jsonify(response_object), 200

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return jsonify(response_object), 404


