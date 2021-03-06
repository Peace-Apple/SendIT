"""
Module to handle any logic
"""
from flask import request, jsonify
from flask.views import MethodView
from api.models.parcel_models import ParcelModel
from api.handlers.response_errors import ResponseErrors
from api.utils.validations import DataValidation
from api.models.database import DatabaseConnection
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from


class ParcelController(MethodView):
    """
    Class with  methods to handle get, post and put methods
    """
    receivers_name = None
    pickup_location = None
    destination = None
    weight = None
    val = DataValidation()
    order_data = ParcelModel()
    data = DatabaseConnection()

    @jwt_required
    @swag_from('../docs/post_parcel.yml')
    def post(self):
        """
        post method to handle posting an order
        :return:
        """
        user = get_jwt_identity()
        admin = user[4]
        user_id = user[0]

        if user_id and admin == "FALSE":

            post_data = request.get_json()
            keys = ("receivers_name", "pickup_location", "destination", "weight")

            if not set(keys).issubset(set(post_data)):
                return ResponseErrors.missing_fields(keys)

            try:
                self.receivers_name = post_data['receivers_name'].strip()
                self.pickup_location = post_data['pickup_location'].strip()
                self.destination = post_data['destination'].strip()
                self.weight = post_data['weight']

            except AttributeError:
                return ResponseErrors.invalid_data_format()

            if not self.receivers_name or not self.pickup_location or not self.destination or not self.weight:
                return ResponseErrors.empty_data_fields()
            elif DataValidation.check_string_of_numbers(self.receivers_name) or \
                    DataValidation.check_string_of_numbers(self.pickup_location) or \
                    DataValidation.check_string_of_numbers(self.destination):
                return ResponseErrors.invalid_data_format()
            # elif self.weight < 0:
            #     return ResponseErrors.negative_number()

            new_order = self.order_data.make_delivery_order(self.receivers_name, self.pickup_location, self.destination,
                                                            self.weight, str(user_id))
            response_object = {
                'message': 'Successfully posted a parcel delivery order',
                'data': new_order
            }
            return jsonify(response_object), 201
        return ResponseErrors.permission_denied()

    @jwt_required
    @swag_from('../docs/get_all_parcels.yml')
    def get(self, parcel_id=None):
        """
        get method to return a list of parcel delivery orders
        :param parcel_id:
        :return:
        """
        user = get_jwt_identity()
        user_id = user[0]
        admin = user[4]

        if admin and user_id:

            if parcel_id:
                return self.get_single_order(parcel_id)

            all_orders = self.data.get_all_parcel_orders()

            if isinstance(all_orders, object):
                orders = []
                for order in all_orders:

                    user = self.data.find_user_by_id(order['user_id'])
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
                    "message": "Successfully got all parcel delivery orders",
                    "data": orders
                    }
                return jsonify(response_object), 200
            else:
                return ResponseErrors.no_items('order')

        return ResponseErrors.denied_permission()

    @jwt_required
    def get_single_order(self, parcel_id):
        """
        Method to return a single parcel delivery order
        :param parcel_id:
        :return:
        """
        user = get_jwt_identity()
        admin = user[4]
        user_id = user[0]

        if user_id and admin:

            single_order = self.data.get_one_parcel_order(parcel_id)
            if isinstance(single_order, object):
                user = self.data.find_user_by_id(single_order['user_id'])
                res_data = {
                    "user_name": user[1],
                    "phone_number": user[3],
                    "email": user[2],
                    "parcel_id": single_order['parcel_id'],
                    "receivers_name": single_order['receivers_name'],
                    "pickup_location": single_order['pickup_location'],
                    "destination": single_order['destination'],
                    "weight": single_order['weight'],
                    "delivery_status": single_order['delivery_status'],
                    "present_location": single_order['present_location'],
                    "order_date": single_order['order_date']
                }

                response_object = {
                    'message': 'Successfully got one parcel delivery order',
                    'data': res_data
                }
                return jsonify(response_object), 200

            else:
                return ResponseErrors.parcel_order_absent()

        return ResponseErrors.denied_permission()

    @jwt_required
    @swag_from('../docs/admin_updates.yml')
    def put(self, parcel_id):
        """
        Method to update the parcel delivery status
        :param parcel_id:
        :return:
        """
        user = get_jwt_identity()
        admin = user[4]
        user_id = user[0]

        if admin == "TRUE" and user_id:

            post_data = request.get_json()

            key = "delivery_status"
            key_1 = "present_location"

            status = ['inTransit', 'completed']
            if key_1 in post_data:
                try:
                    present_location = post_data['present_location'].strip()
                except AttributeError:
                    return ResponseErrors.invalid_data_format()
                if not present_location:
                    return ResponseErrors.empty_data_fields()
                if not self.val.validate_string_input(present_location):
                    return ResponseErrors.invalid_input()
                if DataValidation.check_string_of_numbers(present_location):
                    return ResponseErrors.invalid_data_format()
                return self.update_present_location(present_location, parcel_id)
            elif key in post_data:
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
                    return ResponseErrors.delivery_status_not_accepted(delivery_status)
                deliver = self.data.check_parcel_delivery_status(parcel_id)
                if deliver[0] == 'completed' or deliver[0] == 'cancelled':
                    return ResponseErrors.parcel_cancelled_or_completed()
                parcel = self.data.get_one_parcel_order(parcel_id)
                if not parcel['destination'] == parcel['present_location'] and delivery_status == 'completed':
                    return ResponseErrors.parcel_not_reached_destination()
                updated_status = self.data.update_delivery_status(delivery_status, parcel_id)
                if isinstance(updated_status, object):
                    response_object = {
                        'message': 'Status has been updated successfully'
                    }
                    return jsonify(response_object), 202

        return ResponseErrors.denied_permission()

    def update_present_location(self, present_location, parcel_id):
        """
        Method to update the destination of a parcel delivery order
        :param present_location:
        :param parcel_id:
        :return:
        """
        if self.data.get_one_parcel_order(parcel_id):
            deliver = self.data.check_parcel_delivery_status(parcel_id)
            if deliver[0] == 'completed' or deliver[0] == 'cancelled':
                return ResponseErrors.parcel_cancelled_or_completed()
            updated_location = self.data.update_present_location(present_location, parcel_id)
            if isinstance(updated_location, object):
                response_object = {
                    'message': 'Present location has been updated successfully'

                }
                return jsonify(response_object), 202

        return ResponseErrors.no_items('order')
