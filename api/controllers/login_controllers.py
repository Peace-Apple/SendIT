"""
This module looks at the user login
"""
import datetime

from flask import request, jsonify
from flask.views import MethodView
from api.handlers.response_errors import ResponseErrors
from api.auth.authenticate import Authenticate
from api.models.database import DatabaseConnection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


class LoginController(MethodView):
    """
    User login class
    """
    data = DatabaseConnection()
    auth = Authenticate()

    def post(self):
        # to get post data
        post_data = request.get_json()

        keys = ('user_name', 'password')
        if not set(keys).issubset(set(post_data)):
            return ResponseErrors.missing_fields(keys)

        try:
            user_name = post_data.get("user_name").strip()
            password = post_data.get("password").strip()
        except AttributeError:
            return ResponseErrors.invalid_data_format()

        if not user_name or not password:
            return ResponseErrors.empty_data_fields()

        user = self.data.find_user_by_username(user_name)

        if user and Authenticate.verify_password(password, user[5]):

            response_object = {
                'status': 'success',
                'message': 'You are logged in',
                'access_token': create_access_token(identity=user, expires_delta=datetime.timedelta(minutes=3600)),
                'logged_in_as': str(user[1])
                }

            return jsonify(response_object), 200

        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 404

    @jwt_required
    def get(self, user_id):
        """
        Method to return a single users parcel orders
        :return:
        """
        user = get_jwt_identity()
        user_type = user[4]
        user_id = user[0]

        if user_id and user_type == "FALSE":
            my_parcels = self.data.get_specific_user_parcels(user_id)
            if isinstance(my_parcels, object):

                response_object = {
                    "msg": "Successfully got all orders belonging to user",
                    "data": my_parcels
                }
                return jsonify(response_object), 200
            else:
                return ResponseErrors.no_items('order')
        return ResponseErrors.permission_denied()

    @jwt_required
    def put(self, parcel_id):
        """
        Method for user to change the destination of a parcel delivery order
        :param parcel_id:
        :return:
        """
        user = get_jwt_identity()
        user_type = user[4]
        user_id = user[0]

        if user_id and user_type == "FALSE":

            post_data = request.get_json()

            key = "destination"
            print(request.get_json())

            if key not in post_data:
                return ResponseErrors.missing_fields(key)
            try:
                destination = post_data['destination'].strip()
            except AttributeError:
                    return ResponseErrors.invalid_data_format()

            updated_order = self.data.update_destination(destination, parcel_id)
            if isinstance(updated_order, object):
                response_object = {
                    'message': 'Destination has been updated successfully'

                }
                return jsonify(response_object), 202

            return ResponseErrors.no_items('order')

        return ResponseErrors.permission_denied()

    @jwt_required
    def put(self, parcel_id):
        """
        Method for user to change the destination of a parcel delivery order
        :param parcel_id:
        :return:
        """
        user = get_jwt_identity()
        user_type = user[4]
        user_id = user[0]

        if user_id and user_type == "FALSE":

            post_data = request.get_json()

            key = "destination"
            print(request.get_json())

            if key not in post_data:
                return ResponseErrors.missing_fields(key)
            try:
                destination = post_data['destination'].strip()
            except AttributeError:
                return ResponseErrors.invalid_data_format()

            updated_order = self.data.update_destination(destination, parcel_id)
            if isinstance(updated_order, object):
                response_object = {
                    'message': 'Destination has been updated successfully'

                }
                return jsonify(response_object), 202

            return ResponseErrors.no_items('order')

        return ResponseErrors.permission_denied()






