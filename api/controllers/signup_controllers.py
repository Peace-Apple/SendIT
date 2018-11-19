"""
module to handle signup of the user
"""
from flask import request, jsonify
from flask.views import MethodView
from api.handlers.response_errors import ResponseErrors
from api.models.user_model import Users
from api.utils.validations import DataValidation
from api.auth.authenticate import Authenticate


class SignupController(MethodView):
    """
    Registering a new user
    """
    myUser = Users()
    val = DataValidation()

    def post(self):

        post_data = request.get_json()

        keys = ("user_name", "email", "phone_number", "password")
        if not set(keys).issubset(set(post_data)):
            return ResponseErrors.missing_fields(keys)
        try:
            user_name = post_data.get('user_name').strip()
            email = post_data.get('email').strip()
            phone_number = post_data.get('phone_number').strip()
            password = post_data.get('password').strip()

        except AttributeError:
            return ResponseErrors.invalid_data_format()

        if not user_name or not email or not phone_number or not password:
            return ResponseErrors.empty_data_fields()

        user = self.myUser.register_user(user_name, email, phone_number,
                                         Authenticate.hash_password(password))

        del user.password

        response_object = {
            'status': 'success',
            'message': 'Your account has been created successfully'
            }
        return jsonify(response_object), 201
