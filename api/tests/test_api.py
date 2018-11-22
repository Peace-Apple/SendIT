"""
Tests module
"""
from flask import json

import unittest

from run import app


class TestSendIT(unittest.TestCase):
    """
    Tests run for the api endpoints
    """

    def setUp(self):
        self.app = app
        self.client = self.app.test_client

    def register_user(self, user_name=None, email=None, phone_number=None, password=None):
        return self.client().post(
            '/api/v2/auth/signup/',
            data=json.dumps(dict(
                user_name=user_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )),
            content_type="application/json"
        )

    def login_user(self, user_name=None, password=None):
        return self.client().post(
            '/api/v2/auth/login/',
            data=json.dumps(dict(
                user_name=user_name,
                password=password,
            )),
            content_type='application/json'
        )

    # ....................Testing user authentication, signup and login.............................................. #

    # def test_user_registration(self):
    #     """
    #     Test successful user signup
    #     :return:
    #     """
    #     register = self.register_user('Omech', 'om@gmail.com', '0704194672', 'acireba')
    #     received_data = json.loads(register.data.decode())
    #     print(json.loads(register.data.decode()))
    #     self.assertTrue(received_data['status'], 'success')
    #     self.assertTrue(received_data['message'], 'Your account has been created successfully')
    #     self.assertTrue(received_data['data'])
    #     self.assertTrue(register.content_type, 'application/json')
    #     self.assertEqual(register.status_code, 201)

    def test_missing_fields_during_signup(self):
        """
        Test for missing fields when registering a new user
        :return:
        """
        register = self.client().post(
            '/api/v2/auth/signup/',
            data=json.dumps(dict(
                user_name='Apple',
                email='apple@gmail.com',
                phone_number='0704194672',
            )),
            content_type="application/json"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'some fields are missing')
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_invalid_data_type(self):
        """
        Test user registration with invalid data-type
        :return:
        """
        register = self.register_user(10000, 'apple@gmail.com', '0704194672', 'acireba')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'], 'fail')
        self.assertTrue(received_data['error_message'], 'Please use character strings')
        self.assertFalse(received_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_empty_fields_during_signup(self):
        """
        Test for empty fields during user registration
        :return:
        """
        register = self.register_user(' ', 'apple@gmail.com', '0704194672', 'acireba')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Some fields have no data')
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_invalid_password(self):
        """
        Test for password less than 5 characters
        :return:
        """
        register = self.register_user('Apple', 'apple@gmail.com', '0704194672', 'mat')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'],
                        'Password is wrong. It should be at-least 5 characters long, and alphanumeric.')
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_invalid_email_registration(self):
        """
        Test for registration with invalid email
        :return:
        """
        register = self.register_user('Apple', 'apple@gmail', '0704194672', 'acireba')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'User email {0} is wrong,'
                                                        'It should be in the format (xxxxx@xxxx.xxx)')
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_phone_number(self):
        """
        testing invalid phone_number
        :return:
        """
        register = self.register_user('Apple', 'app0@gmail.com', '070419', 'acireba')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['error_message'], 'Contact {0} is wrong. should be in the form, (070*******)'
                                                        'and between 10 and 13 digits')
        self.assertTrue(received_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_invalid_user_name(self):
        """
        testing invalid username
        :return:
        """
        register = self.register_user('Apple56', 'apple@gmail.com', '0704194672', 'acireba')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'], 'fail')
        self.assertTrue(received_data['error_message'], 'A name should consist of only alphabetic characters')
        self.assertTrue(received_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_user_name_exists(self):
        """
        Test when the user name already exists
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com', '0704194672', 'acireba')
        register = self.register_user('Apple', 'app@gmail.com', '0704194672', 'acireba')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Username already taken')
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 409)

    # def test_registered_user_login(self):
    #     """
    #     Test for proper registered user login
    #     :return:
    #     """
    #     self.register_user('Apple', 'apple@gmail.com', '0704194672', 'acireba')
    #     login_user = self.login_user('Apple', 'acireba')
    #
    #     response_data = json.loads(login_user.data.decode())
    #
    #     self.assertTrue(response_data['status'], 'success')
    #     self.assertTrue(response_data['message'], 'You are logged in')
    #     self.assertTrue(response_data['access_token'])
    #     self.assertTrue(response_data['logged_in_as'], 'Apple')
    #     self.assertTrue(login_user.content_type, 'application/json')
    #     self.assertEqual(login_user.status_code, 200)

    def test_non_registered_user_login(self):
        """
        Test for login of a non registered user
        :return:
        """
        login_user = self.login_user('Anna', 'acireba')
        data = json.loads(login_user.data.decode())
        self.assertTrue(data['status'], 'fail')
        self.assertTrue(data['message'], 'User does not exist.')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 404)

    def test_login_with_missing_fields(self):
        """
        Test for login with missing fields
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com', '0704194672', 'acireba')
        login_user = self.client().post(
            '/api/v2/auth/login/',
            data=json.dumps(dict(
                user_name="Apple"
            )),
            content_type='application/json'
        )

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'some fields are missing')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 400)

    def test_login_with_invalid_data_type(self):
        """
        Test for login with invalid data types
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com', '0704194672', 'acireba')
        login_user = self.login_user('Apple', 100100)

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Please use character strings')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 400)

    def test_login_with_empty_fields(self):
        """
        Test for login with empty fields
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com', '0704194672', 'pesay')
        login_user = self.login_user('Apple', '')

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Some fields have no data')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 400)
