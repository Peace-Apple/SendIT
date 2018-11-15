"""
Tests module
"""
import unittest

from flask import json

from run import app


class TestSendIT(unittest.TestCase):
    """
    Tests for the api endpoints.
    """
    def setUp(self):
        self.app = app
        self.client = self.app.test_client

    def make_delivery_order(self, pickup_location, destination, weight, user_id):
        """
        Method takes these parameters to make a delivery order
        :param pickup_location:
        :param destination:
        :param weight:
        :param user_id:
        :return:
        """
        post_data = self.client().post(
            '/api/v1/parcels/',
            data=json.dumps(dict(
                pickup_location=pickup_location,
                destination=destination,
                weight=weight,
                user_id=user_id
            )),
            content_type='application/json'
        )
        return post_data

    def test_make_delivery_order(self):
        post = self.make_delivery_order('Kampala', 'Entebbe', 3, 1)
        post_response = json.loads(post.data.decode())
        self.assertTrue(post_response['message'], 'Successfully posted a parcel delivery order')
        self.assertTrue(post_response['data'])
        self.assertTrue(post.content_type, 'application/json')
        self.assertEqual(post.status_code, 201)

    def test_make_delivery_order_with_invalid_data_format(self):
        post = self.make_delivery_order('12345', 'Entebbe', 3, 1)
        post_response = json.loads(post.data.decode())
        self.assertTrue(post_response['status'], 'fail')
        self.assertTrue(post_response['error_message'], 'Please use character strings')
        self.assertFalse(post_response['data'])
        self.assertTrue(post.content_type, 'application/json')
        self.assertEqual(post.status_code, 400)

    def test_make_delivery_order_with_empty_data_field(self):
        post = self.make_delivery_order('', 'Entebbe', 3, 1)
        post_response = json.loads(post.data.decode())
        self.assertTrue(post_response['status'], 'fail')
        self.assertTrue(post_response['error_message'], 'Some fields have no data')
        self.assertFalse(post_response['data'])
        self.assertTrue(post.content_type, 'application/json')
        self.assertEqual(post.status_code, 400)

    def test_make_delivery_order_with_negative_weight(self):
        post = self.make_delivery_order('Kampala', 'Entebbe', -3, 1)
        post_response = json.loads(post.data.decode())
        self.assertTrue(post_response['status'], 'fail')
        self.assertTrue(post_response['error_message'], 'The ID can not be negative')
        self.assertFalse(post_response['data'])
        self.assertTrue(post.content_type, 'application/json')
        self.assertEqual(post.status_code, 400)

    def test_make_delivery_order_with_negative_user_id(self):
        post = self.make_delivery_order('Kampala', 'Entebbe', 3, -1)
        post_response = json.loads(post.data.decode())
        self.assertTrue(post_response['status'], 'fail')
        self.assertTrue(post_response['error_message'], 'The ID can not be negative')
        self.assertFalse(post_response['data'])
        self.assertTrue(post.content_type, 'application/json')
        self.assertEqual(post.status_code, 400)

    def test_get_parcel_delivery_orders(self):
        self.make_delivery_order('Kampala', 'Entebbe', 4, 1)
        self.make_delivery_order('Mbuya', 'Bunga', 3, 2)
        self.make_delivery_order('Gaba', 'Luzira', 5, 3)
        self.make_delivery_order('Kampala', 'Entebbe', 2, 4)
        self.make_delivery_order('Entebbe', 'Mukono', 4, 5)

        request_data = self.client().get('/api/v1/parcels/')

        response_data = json.loads(request_data.data.decode())
        self.assertTrue(response_data['message'], 'Successfully got all parcel delivery orders')
        self.assertTrue(response_data['data'])
        self.assertEqual(request_data.status_code, 200)

    def test_get_parcel_order_that_does_not_exist(self):
        self.make_delivery_order('Kampala', 'Entebbe', 4, 1)

        request_data = self.client().get('/api/v1/parcels/100/')

        response_data = json.loads(request_data.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Parcel order does not exist')
        self.assertFalse(response_data['data'])
        self.assertEqual(request_data.status_code, 400)

    def test_get_parcel_order_that_exists(self):
        self.make_delivery_order('Kampala', 'Entebbe', 4, 1)
        self.make_delivery_order('Mbuya', 'Bunga', 3, 2)
        self.make_delivery_order('Gaba', 'Luzira', 5, 3)
        self.make_delivery_order('Kampala', 'Entebbe', 2, 4)
        self.make_delivery_order('Entebbe', 'Mukono', 4, 5)

        request_data = self.client().get('/api/v1/parcels/3/')

        response_data = json.loads(request_data.data.decode())
        self.assertTrue(response_data['message'], 'Successfully got one parcel delivery order')
        self.assertTrue(response_data['data'])
        self.assertEqual(request_data.status_code, 200)

    def test_update_delivery_status(self):
        self.make_delivery_order('Kampala', 'Entebbe', 4, 1)

        request_data = self.client().put(
            '/api/v1/parcels/1/cancel/',
            data=json.dumps(dict(
                delivery_status="cancelled"
            )),
            content_type='application/json'
        )

        response_data = json.loads(request_data.data.decode())
        self.assertTrue(response_data['message'], 'Parcel delivery order has been canceled successfully')
        self.assertTrue(request_data.content_type, 'application/json')
        self.assertEqual(request_data.status_code, 202)

    def test_update_delivery_order_absent(self):
        self.make_delivery_order('Kampala', 'Entebbe', 4, 1)

        request_data = self.client().put(
            '/api/v1/parcels/7/cancel/',
            data=json.dumps(dict(
                delivery_status="cancelled"
            )),
            content_type='application/json'
        )
        response_data = json.loads(request_data.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Parcel order does not exist')
        self.assertFalse(response_data['data'])
        self.assertEqual(request_data.status_code, 400)

    def test_get_a_specific_users_parcel_orders(self):
        self.make_delivery_order('Kampala', 'Entebbe', 4, 1)
        self.make_delivery_order('Kampala', 'Mbuya', 3, 1)

        request_data = self.client().get('/api/v1/users/1/parcels/')

        response_data = json.loads(request_data.data.decode())
        self.assertTrue(response_data['message'], 'Successfully got all orders belonging to user')
        self.assertTrue(response_data['data'])
        self.assertEqual(request_data.status_code, 200)

    def test_get_a_specific_users_parcel_orders_with_user_id_that_does_not_exist(self):
        self.make_delivery_order('Kampala', 'Entebbe', 4, 1)
        self.make_delivery_order('Kampala', 'Mbuya', 3, 1)

        request_data = self.client().get('/api/v1/users/6/parcels/')

        response_data = json.loads(request_data.data.decode())
        self.assertTrue(response_data['error_message'], 'User does not exist')
        self.assertFalse(response_data['data'])
        self.assertEqual(request_data.status_code, 400)


