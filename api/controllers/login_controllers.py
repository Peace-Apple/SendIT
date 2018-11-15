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
    data = UserModel()

    def post(self):
        # to get post data
        post_data = request.get_json()

        keys = ('user_name', 'password', 'user_id')
        if not set(keys).issubset(set(post_data)):
            return ResponseErrors.missing_fields(keys)

        try:
            user_name = post_data.get("user_name").strip()
            password = post_data.get("password").strip()
            user_id = post_data("user_id")
        except AttributeError:
            return ResponseErrors.invalid_data_format()

        if not user_name or not password or not user_id:
            return ResponseErrors.empty_data_fields()

        user = self.data.get_all_users()

        if self.user_name == user['user_name'] and self.user_id == user['user_id']:

            response_object = {
                'status': 'success',
                'message': 'You are logged in',
                'logged_in_as': user_name
            }

            return jsonify(response_object), 200

        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 404


