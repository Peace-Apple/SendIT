"""
Module to handle any logic
"""
from flask import request, jsonify
from flask.views import MethodView
from api.models.parcel_models import ParcelModel
from api.handlers.response_errors import ResponseErrors
from api.utils.validations import DataValidation


class ParcelController(MethodView):
    """
    Class with  methods to handle get, post and put methods
    """
    pickup_location = None
    destination = None
    weight = None
    user_id = None
    order_data = ParcelModel()
    delivery_status = None

    def post(self):
        """
        post method to handle post requests
        :return:
        """
        post_data = request.get_json()
        keys = ("pickup_location", "destination", "weight", "user_id")

        if not set(keys).issubset(set(post_data)):
            return ResponseErrors.missing_fields(keys)

        try:
            self.pickup_location = post_data['pickup_location'].strip()
            self.destination = post_data['destination'].strip()
            self.weight = post_data['weight']
            self.user_id = post_data['user_id']

        except AttributeError:
            return ResponseErrors.invalid_data_format()

        if not self.pickup_location or not self.destination or not self.weight or not self.user_id:
            return ResponseErrors.empty_data_fields()
        elif DataValidation.check_string_of_numbers(self.pickup_location) or \
                DataValidation.check_string_of_numbers(self.destination):
            return ResponseErrors.invalid_data_format()
        elif self.user_id < 0 or self.weight < 0:
            return ResponseErrors.negative_number()

        current_order = self.order_data.make_delivery_order(self.pickup_location, self.destination,
                                                            self.weight, self.user_id)
        response_object = {
            'message': 'Successfully posted a parcel delivery order',
            'data': current_order
        }
        return jsonify(response_object), 201

    def get(self, parcel_id=None, user_id=None):
        """
        get method to return a list of parcel delivery orders
        :param parcel_id:
        :param user_id:
        :return:
        """

        all_orders = self.order_data.get_all_orders()
        if not all_orders:
            return ResponseErrors.empty_data_storage()
        elif parcel_id:
            return self.get_single_order(parcel_id)
        elif user_id:
            return self.get_specific_user(user_id)

        response_object = {
            'message': 'Successfully got all parcel delivery orders',
            'data': all_orders
        }
        return jsonify(response_object), 200

    def get_single_order(self, parcel_id):
        """
        Method to return a single parcel delivery order
        :param parcel_id:
        :return:
        """
        orders = self.order_data.get_all_orders()
        for single_order in orders:
            if parcel_id == single_order['parcel_id']:
                response_object = {
                    'message': 'Successfully got one parcel delivery order',
                    'data': single_order
                }
                return jsonify(response_object), 200
        return ResponseErrors.parcel_order_absent()

    def get_specific_user(self, user_id):
        """
        Method to return a single users parcel orders
        :param user_id:
        :return:
        """
        orders = self.order_data.get_all_orders()
        user_orders = []

        for order in orders:
            if user_id == order['user_id']:
                for parcel in orders:
                    if user_id == parcel['user_id']:
                        user_orders.append(parcel)
                response_object = {
                    'message': 'Successfully got all orders belonging to user',
                    'data': user_orders
                }
                return jsonify(response_object), 200
            return ResponseErrors.user_absent()

    def put(self, parcel_id):
        """
        method to make changes to the delivery status and cancel it
        :param parcel_id:
        :return:
        """
        order = self.order_data.get_one_order(parcel_id)

        post_data = request.get_json()
        key = 'delivery_status'
        if key not in post_data:
            return ResponseErrors.missing_key(key)
        try:
            self.delivery_status = post_data['delivery_status'].strip()
        except AttributeError:
            return ResponseErrors.invalid_data_format()

        if not self.delivery_status:
            return ResponseErrors.empty_data_fields()
        elif DataValidation.check_string_of_numbers(self.delivery_status):
            return ResponseErrors.invalid_data_format()

        if not order:
            return ResponseErrors.order_absent()

        return self.order_data.update_delivery_status(parcel_id, self.delivery_status)


