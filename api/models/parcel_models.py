"""
Module to handle data storage
"""
import datetime
from api.models.database import DatabaseConnection


class ParcelModel:

    """
    This class uses the database to store data persistently
    """
    data = DatabaseConnection()

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
