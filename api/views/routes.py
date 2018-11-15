"""
Module to handle url requests
"""
from api.controllers.parcel_controllers import ParcelController


class Routes:
    """
        Class to generate urls
    """

    @staticmethod
    def generate(app):
        """
        Generate urls
        :param app:
        :return:
        """
        app.add_url_rule('/api/v1/parcels/', view_func=ParcelController.as_view('make_delivery_order'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/parcels/', view_func=ParcelController.as_view('get_all_orders'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/parcels/<int:parcel_id>', view_func=ParcelController.as_view('get_one_order'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/users/<int:user_id>/parcels/', view_func=ParcelController.as_view('get_user_parcels'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/parcels/<int:parcel_id>/cancel/',
                         view_func=ParcelController.as_view('update_delivery_status'),
                         methods=['PUT'], strict_slashes=False)

