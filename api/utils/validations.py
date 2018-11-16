"""
Module to handle validation
"""


class DataValidation:
    """
    Class has methods to handle validation of data
    """

    @staticmethod
    def check_string_of_numbers(test_data):
        try:
            int(test_data)
            return True
        except ValueError:
            return False




