"""
Module to handle all responses to errors
"""
from flask import jsonify


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

    # @staticmethod
    # def invalid_data_type():
    #     response_object = {
    #         'status': 'fail',
    #         'error_message': 'Wrong data type, please use a number',
    #         'data': False
    #     }
    #     return jsonify(response_object), 400

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
        return jsonify(response_object), 200

    @staticmethod
    def parcel_order_absent():
        response_object = {
            'status': 'fail',
            'error_message': 'Parcel order does not exist',
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def user_absent():
        response_object = {
            'status': 'fail',
            'error_message': 'User does not exist',
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def order_absent():
        response_object = {
            'status': 'fail',
            'error_message': 'Order does not exist',
            'data': False
        }
        return jsonify(response_object), 400

    @staticmethod
    def negative_number():
        response_object = {
            'status': 'fail',
            'error_message': 'The ID can not be negative',
            'data': False
        }
        return jsonify(response_object), 400




