"""
Module to handle all responses to errors
"""
from flask import jsonify, request


class ResponseErrors:
    """
    Error handler to handle response errors.
    """

    @staticmethod
    def missing_fields(key):
        response_object = {
            "status": "fail",
            "error_message": "some fields are missing",
            "data": key}
        return jsonify(response_object), 400

    @staticmethod
    def invalid_data_format():
        response_object = {
            'status': 'fail',
            'error_message': 'Please use character strings',
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def empty_data_fields():
        response_object = {
            'status': 'fail',
            'error_message': 'Some fields have no data',
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def missing_key(keys):
        response_object = {
            'status': 'fail',
            'error_message': 'Missing key ' + keys,
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def empty_data_storage():
        response_object = {
            'status': 'success',
            'message': 'No parcel delivery orders currently',
            'data': False
        }
        return jsonify(response_object), 404

    @staticmethod
    def parcel_order_absent():
        response_object = {
            'status': 'fail',
            'error_message': 'Parcel order does not exist',
            'data': False
        }
        return jsonify(response_object), 404

    @staticmethod
    def user_absent():
        response_object = {
            'status': 'fail',
            'error_message': 'User does not exist',
            'data': False
        }
        return jsonify(response_object), 404

    @staticmethod
    def order_absent():
        response_object = {
            'status': 'fail',
            'error_message': 'Order does not exist',
            'data': False
        }
        return jsonify(response_object), 404

    @staticmethod
    def negative_number():
        response_object = {
            'status': 'fail',
            'error_message': 'The ID can not be negative',
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def invalid_password():
        response_object = {
            'status': 'fail',
            'error_message': 'Password is wrong. It should be at-least 5 characters long, and alphanumeric.',
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def invalid_email():
        req = request.get_json()
        return jsonify({
            "status": "fail",
            "error_message": "User email {0} is wrong, It should be in the format (xxxxx@xxxx.xxx).format(req['email']",
            "data": req

        }), 400

    @staticmethod
    def invalid_phone_number():
        req = request.get_json()
        return jsonify({"error_message": "Contact {0} is wrong. should be in"
                                         " the form, (070******) and between 10 and 13 "
                                         "digits".format(req['phone_number']),
                        "data": req
                        }), 400

    @staticmethod
    def username_already_exists():
        response_object = {
            'status': 'fail',
            'error_message': 'Username already taken',
            'data': False
        }
        return jsonify(response_object), 409

    @staticmethod
    def email_already_exists():
        response_object = {
            'status': 'fail',
            'error_message': 'email already exists'

                }
        return jsonify(response_object), 409

    @staticmethod
    def invalid_name():
        return jsonify({
            "status": "fail",
            "error_message": "A name should consist of only alphabetic characters",
            "data": request.get_json()
                   }), 400

    @staticmethod
    def invalid_input():
        return jsonify({
            "status": "fail",
            "error_message": "The input here should be a string of characters",
            "data": request.get_json()
                   }), 400

    @staticmethod
    def permission_denied():
        response_object = {
            'status': 'fail',
            'message': 'Permission denied, Please Login as a user'
        }
        return jsonify(response_object), 401

    @staticmethod
    def no_items(item):
        response_object = {
            'status': 'fail',
            'message': 'No {} items currently'.format(item)
        }
        return jsonify(response_object), 404

    @staticmethod
    def denied_permission():
        response_object = {
            'status': 'fail',
            'message': 'Permission denied, Please Login as Admin'
        }
        return jsonify(response_object), 401

    @staticmethod
    def delivery_status_not_found(delivery_status):
        return jsonify({
            "status": "fail",
            "error_message": "Delivery status {} not found, only use cancelled as the value".format(delivery_status),
        }), 404

    @staticmethod
    def parcel_already_cancelled():
        response_object = {
            'status': 'fail',
            'error_message': 'Can not cancel a parcel order twice',
            'data': False
        }
        return jsonify(response_object), 406
