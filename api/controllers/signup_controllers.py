"""
module to handle signup of the user
"""
from flask import request, jsonify
from flask.views import MethodView
from api.handlers.response_errors import ResponseErrors
from api.models.user_model import UserModel
from api.utils.validations import DataValidation
from api.auth.authenticate import Authenticate
from flasgger import swag_from


class SignupController(MethodView):
    """
    Registering a new user
    """
    myUser = UserModel()
    val = DataValidation()

    @swag_from('../docs/signup.yml')
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
        elif not self.val.validate_email(email):
            return ResponseErrors.invalid_email()
        elif not self.val.validate_name(user_name):
            return ResponseErrors.invalid_name()
        elif not self.val.check_if_email_exists(email):
            return ResponseErrors.email_already_exists()
        elif not self.val.validate_phone(phone_number):
            return ResponseErrors.invalid_phone_number()
        elif not self.val.check_if_user_name_exists(user_name):
            return ResponseErrors.username_already_exists()

        user = self.myUser.register_user(user_name, email, phone_number,
                                         Authenticate.hash_password(password))

        del user.password

        response_object = {
            'status': 'success',
            'message': 'Your account has been created successfully'
            }
        return jsonify(response_object), 201
