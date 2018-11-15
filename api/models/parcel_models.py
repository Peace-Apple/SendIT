"""
Module to handle data storage
"""
import datetime
from flask import jsonify


class ParcelModel:

    """
    This class uses data structures to store data non-persistently
    """

    increment = 0

    def __init__(self, pickup_location=None, destination=None, weight=None, user_id=None):
        self.parcel_id = None
        self.user_id = user_id
        self.pickup_location = pickup_location
        self.destination = destination
        self.weight = weight
        self.order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.delivery_status = 'pending'

    def make_delivery_order(self, pickup_location, destination, weight, user_id):
        self.increment += 1
        current_order = ParcelModel(pickup_location, destination, weight, user_id)
        current_order.parcel_id = self.increment

        new_order = {
            'parcel_id': current_order.parcel_id,
            'user_id': current_order.user_id,
            'pickup_location': current_order.pickup_location,
            'destination': current_order.destination,
            'weight': current_order.weight,
            'order_date': current_order.order_date,
            'delivery_status': current_order.delivery_status
        }
        self.orders.append(new_order)
        return new_order

    def get_all_orders(self):
        return self.orders

    def get_one_order(self, parcel_id):
        for order in self.orders:
            if parcel_id == order['parcel_id']:
                return order
            return None

    def update_delivery_status(self, parcel_id, delivery_status=None):
        order = self.get_one_order(parcel_id)
        if not order:
            return False
        order['delivery_status'] = delivery_status
        response_object = {
            'message': 'Parcel delivery order has been canceled successfully'
        }
        return jsonify(response_object), 202

    orders = []

