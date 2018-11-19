"""
Module to handle data storage
"""
import datetime
from flask import jsonify
from api.models.database import DatabaseConnection


class ParcelModel:

    """
    This class uses the database to store data persistently
    """

    def __init__(self, receivers_name=None, pickup_location=None, destination=None, weight=None, user_id=None):
        self.parcel_id = None
        self.user_id = user_id
        self.receivers_name = receivers_name
        self.pickup_location = pickup_location
        self.destination = destination
        self.weight = weight
        self.order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.delivery_status = 'New'
        self.present_location = 'Office'


class Orders:
    data = DatabaseConnection()

    def make_delivery_order(self, receivers_name=None, pickup_location=None, destination=None, weight=None,
                            user_id=None):
        """
        Make new parcel delivery order
        :param receivers_name:
        :param pickup_location:
        :param destination:
        :param weight:
        :param user_id:
        :return:
        """
        current_order = self.data.insert_parcel(receivers_name, pickup_location, destination, weight, user_id)

        return current_order

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

