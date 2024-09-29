#!/usr/bin/python3
"""
Module that represents the T-Mobile account with operations pertaining to whole account
    - Relies on SummaryBillMMMYYYY.pdf to perform operations pertaining to the account
"""
from tmobile.utilities.utils import parse_to_float


class Account:
    """
    Main class to perform operations pertaining to T-Mobile account
    """

    def __init__(self, all_lines, account_total=0):
        self.lines = all_lines
        self.account_total = account_total
        self.tax_total = self._get_tax_total()

    @property
    def no_of_lines(self):
        """Property that define the number of lines on the account

        :return: No. of lines on the account
        :rtype: (int)
        """
        return len(self.lines)

    def _get_tax_total(self):
        """Function to get total tax on the account

        :return: Total calculated tax on the account
        :rtype: (float)
        """
        total_tax = 0
        for line in self.lines:
            total_tax += line.tax
        return parse_to_float(total_tax)

    def get_basic_charge(self):
        """Function to get basic charge for each line on the account

        :return: Basic charges for each line
        :rtype: (float)
        """
        return parse_to_float(self.account_total / self.no_of_lines)
