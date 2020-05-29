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
)


class Line:
    """
    Main class to perform operations each line on T-Mobile account with
    class variable corresponding to full path to user details.json file
    """

    __user_info__ = "configs/users.json"

    def __init__(self, prop):
        if os.path.exists(Line.__user_info__):
            err = "file={} is missing. Kindly review --help menu".format(
                Line.__user_info__
            )
            raise FileNotFoundError(err)
        self.prop = prop
        self.line = self.prop["Line"]
        self.type = self.prop["Type"]
        self.one_time_charge = self._get_onetime_charge()
        self.equipment = self._get_equipment()
        self.services = self._get_services()
        self.tax = self._get_tax()
        self.user = parse_json_data(Line.__user_info__)[self.line]
        self._validate_user_info()

    def _validate_user_info(self):
        """Private function to validate the user information provided in the json file

        :raises UserNotFound: If user or email details are not valid
        """
        if "user" not in self.user or not self.user.name:
            raise UserNotFound(
                '"user" details are incorrect in file={}'.format(Line.__user_info__)
            )
        if "email" not in self.user:
            raise UserNotFound(
                '"email" details are incorrect in file={} for user={}'.format(
                    Line.__user_info__, self.user.name
                )
            )

    def _get_equipment(self):
        """Private function to get equipment charges on a line

        :return: Equipment charges on a line
        :rtype: (int)
        """
        if self.prop["Equipment"] == "-":
            return 0
        return parse_to_num(self.prop["Equipment"])

    def _get_services(self):
        """Private function to get service charges on a line

        :return: Service charges on a line
        :rtype: (int)
        """
        if self.prop["Services"] == "-":
            return 0
        return parse_to_num(self.prop["Services"])

    def _get_tax(self):
        """Private function to calculate and get tax on a line

        :return: Tax amount on a line
        :rtype: (float)
        """
        tax = parse_to_num(self.prop["Plans"])
        if tax > 20:
            tax = tax - 20
        return parse_to_float(tax)

    def _get_onetime_charge(self):
        """Private function to get one-time charges on a line

        :return: One-time charges on a line
        :rtype: (int)
        """
        if (
            self.prop.get("One-time charges") is None
            or self.prop.get("One-time charges") == "-"
        ):
            return 0
        return parse_to_num(self.prop["One-time charges"])
