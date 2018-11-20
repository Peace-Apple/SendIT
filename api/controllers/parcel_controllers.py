"""
Module to handle any logic
"""
from flask import request, jsonify
from flask.views import MethodView
from api.models.parcel_models import Orders
from api.handlers.response_errors import ResponseErrors
from api.utils.validations import DataValidation
from api.models.database import DatabaseConnection
from flask_jwt_extended import jwt_required, get_jwt_identity


class ParcelController(MethodView):
    """
    Class with  methods to handle get, post and put methods
    """
    receivers_name = None
    pickup_location = None
    destination = None
    weight = None
    val = DataValidation()
    order_data = Orders()
    data = DatabaseConnection()

    @jwt_required
    def post(self):
        """
        post method to handle posting an order
        :return:
        """
        user = get_jwt_identity()
        user_type = user[4]
        user_id = user[0]

        if user_id and user_type == "FALSE":

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
            elif self.weight < 0:
                return ResponseErrors.negative_number()

            new_order = self.order_data.make_delivery_order(self.receivers_name, self.pickup_location, self.destination,
                                                            self.weight, str(user_id))
            response_object = {
                'message': 'Successfully posted a parcel delivery order',
                'data': new_order
            }
            return jsonify(response_object), 201
        return ResponseErrors.permission_denied()

    @jwt_required
    def get(self, parcel_id=None):
        """
        get method to return a list of parcel delivery orders
        :param parcel_id:
        :return:
        """
        user = get_jwt_identity()
        user_id = user[0]
        user_type = user[4]

        if user_type == "TRUE" and user_id:

            if parcel_id:
                return self.get_single_order(parcel_id)

            all_orders = self.data.get_all_parcel_orders()

            if isinstance(all_orders, object):

                response_object = {
                    "msg": "Successfully got all parcel delivery orders",
                    "data": all_orders
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
        user_type = user[4]
        user_id = user[0]

        if user_id and user_type == "TRUE":

            single_order = self.data.get_one_parcel_order(parcel_id)

            if isinstance(single_order, object):
                response_object = {
                    'msg': 'Successfully got one parcel delivery order',
                    'data': single_order
                }
                return jsonify(response_object), 200

            else:
                return ResponseErrors.parcel_order_absent()

        return ResponseErrors.denied_permission()




