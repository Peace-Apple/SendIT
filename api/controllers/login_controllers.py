"""
This module looks at the user login
"""
import datetime

from flask import request, jsonify
from flask.views import MethodView
from api.handlers.response_errors import ResponseErrors
from api.auth.authenticate import Authenticate
from api.models.database import DatabaseConnection
from api.models.parcel_models import ParcelModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.utils.validations import DataValidation
from flasgger import swag_from


class LoginController(MethodView):
    """
    User login class
    """
    destination = None
    data = DatabaseConnection()
    auth = Authenticate()
    order = ParcelModel()
    val = DataValidation()

    @swag_from('../docs/login.yml')
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
                'access_token': create_access_token(identity=user,
                                                    expires_delta=datetime.timedelta(minutes=3600)),
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
    # @swag_from('..docs/get_user_parcels.yml')
    def get(self, user_id):
        """
        Method to return a single users parcel orders
        :return:
        """
        user = get_jwt_identity()
        admin = user[4]

        if user_id and admin == "FALSE":
            my_parcels = self.data.get_specific_user_parcels(user_id)
            if isinstance(my_parcels, object):
                user = self.data.find_user_by_id(user_id)
                orders = []
                for order in my_parcels:
                    res_data = {
                        "user_name": user[1],
                        "phone_number": user[3],
                        "email": user[2],
                        "parcel_id": order['parcel_id'],
                        "receivers_name": order['receivers_name'],
                        "pickup_location": order['pickup_location'],
                        "destination": order['destination'],
                        "weight": order['weight'],
                        "delivery_status": order['delivery_status'],
                        "present_location": order['present_location'],
                        "order_date": order['order_date']
                    }
                    orders.append(res_data)
                response_object = {
                    "message": "Successfully got all orders belonging to user",
                    "data": orders
                }
                return jsonify(response_object), 200
            else:
                return ResponseErrors.no_items('order')
        return ResponseErrors.permission_denied()

    @jwt_required
    @swag_from('../docs/user_updates.yml')
    def put(self, parcel_id):
        """
        Method for user to cancel a parcel delivery order
        :param parcel_id:
        :return:
        """
        user = get_jwt_identity()
        admin = user[4]
        user_id = user[0]

        if admin == "FALSE" and user_id:

            post_data = request.get_json()

            key = "delivery_status"
            key1 = "destination"
            status = ['cancelled']

            if key1 in post_data:
                if key1 not in post_data:
                    return ResponseErrors.missing_fields(key1)
                if not post_data['destination']:
                    return ResponseErrors.empty_data_fields()
                if DataValidation.check_string_of_numbers(post_data['destination']):
                    return ResponseErrors.invalid_data_format()
                return self.update_parcel_destination(post_data['destination'].strip(), parcel_id)

            elif key:
                if key not in post_data:
                    return ResponseErrors.missing_fields(key)
                try:
                    delivery_status = post_data['delivery_status'].strip()
                except AttributeError:
                    return ResponseErrors.invalid_data_format()
                if not delivery_status:
                    return ResponseErrors.empty_data_fields()
                if not self.val.validate_string_input(delivery_status):
                    return ResponseErrors.invalid_input()
                if DataValidation.check_string_of_numbers(delivery_status):
                    return ResponseErrors.invalid_data_format()
                if delivery_status not in status:
                    return ResponseErrors.delivery_status_not_found(delivery_status)
                deliver = self.data.check_parcel_delivery_status(parcel_id)
                if deliver[0] == 'completed':
                    return ResponseErrors.parcel_already_delivered()
                if deliver[0] == 'cancelled':
                    return ResponseErrors.parcel_already_cancelled()
                updated_status = self.data.cancel_delivery_order(delivery_status, parcel_id)
                if isinstance(updated_status, object):
                    response_object = {
                        'message': 'Parcel delivery order has been cancelled successfully'
                    }
                    return jsonify(response_object), 202

        return ResponseErrors.permission_denied()

    def update_parcel_destination(self, destination, parcel_id):
        """
        Method to update the destination of a parcel delivery order
        :param destination:
        :param parcel_id:
        :return:
        """
        if self.data.get_one_parcel_order(parcel_id):
            deliver = self.data.check_parcel_delivery_status(parcel_id)
            if deliver[0] == 'completed' or deliver[0] == 'cancelled':
                return ResponseErrors.parcel_cancelled_or_completed()
            updated_destination = self.data.update_destination(destination, parcel_id)
            if isinstance(updated_destination, object):
                response_object = {
                    'message': 'Destination has been updated successfully'

                }
                return jsonify(response_object), 202

        return ResponseErrors.no_items('order')
