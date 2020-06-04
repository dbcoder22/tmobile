#!/usr/bin/python
"""
Module that represents each line on the T-Mobile account with operations pertaining to each line
    - Relies on configs/users.json with appropriate line:{name, email} definition for each user
"""
import os
from tmobile.utilities.utils import (
    parse_to_num,
    parse_to_float,
    parse_json_data,
    UserNotFound,
    validate_email,
)


class Line:
    """
    Main class to perform operations each line on T-Mobile account with
    class variable corresponding to full path to user details.json file
    """

    def __init__(self, prop, user_info_file="configs/users.json"):
        self.user_info_file = user_info_file
        self.prop = prop
        self.__check_file()
        self.user = self.__user()
        self.__validate_user_info()

    def __validate_user_info(self):
        """Private function to validate the user information provided in the json file

        :raises UserNotFound: If user or email details are not valid
        """
        if "name" not in self.user or not self.user["name"]:
            raise UserNotFound(
                '"name" details are missing in file={}'.format(self.user_info_file)
            )
        if "email" not in self.user:
            raise UserNotFound(
                '"email" details are missing in file={} for user={}'.format(
                    self.user_info_file, self.user["name"]
                )
            )
        if not validate_email(self.user["email"]):
            raise ValueError(
                "Incorrect email={} address provided for user={}".format(
                    self.user["email"], self.user["name"]
                )
            )

    def __check_file(self):
        """Function to check if file exists

        :raises FileNotFoundError: If file is not found
        """
        if not os.path.exists(self.user_info_file):
            err = "file={} is missing. Kindly review --help menu".format(
                self.user_info_file
            )
            raise FileNotFoundError(err)

    def __user(self):
        """Property defining user details on a line

        :return: User details defined in users.json file
        :rtype: (dict)
        """
        return parse_json_data(self.user_info_file)[self.line]

    @property
    def line(self):
        """Property defining number associated with line

        :return: Number associated with line
        :rtype: (str)
        """
        return self.prop["Line"]

    @property
    def linetype(self):
        """Property defining type of line

        :return: Type of line
        :rtype: (str)
        """
        return self.prop["Type"]

    @property
    def equipment(self):
        """Property defining equipment charges on a line

        :return: Equipment charges on a line
        :rtype: (int)
        """
        if self.prop["Equipment"] == "-":
            return 0
        return parse_to_num(self.prop["Equipment"])

    @property
    def services(self):
        """Property defining service charges on a line

        :return: Service charges on a line
        :rtype: (int)
        """
        if self.prop["Services"] == "-":
            return 0
        return parse_to_num(self.prop["Services"])

    @property
    def tax(self):
        """Property defining tax on a line

        :return: Tax amount on a line
        :rtype: (float)
        """
        tax = parse_to_num(self.prop["Plans"])
        if tax > 20:
            tax = tax - 20
        return parse_to_float(tax)

    @property
    def one_time_charge(self):
        """Property defining one-time charges on a line

        :return: One-time charges on a line
        :rtype: (int)
        """
        if (
            self.prop.get("One-time charges") is None
            or self.prop.get("One-time charges") == "-"
        ):
            return 0
        return parse_to_num(self.prop["One-time charges"])
