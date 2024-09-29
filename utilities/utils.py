#!/usr/bin/python3
"""
This module provides all unique independent utility functions that can be
imported into other programs to perform string operations as defined
"""
import calendar
import json
from datetime import datetime


class UserNotFound(Exception):
    """Raise this error when user is not found

    :param Exception: Base Exception Class object
    :type Exception: (Exception)
    """


def parse_to_num(string_val):
    """Convert given value to a numeric value
       e.g. parse_to_num($25.9345) -> 25.94

    :param string_val: Value to be converted to numerical value
    :type string_val: (str)
    :return: Converted float value to string and remove '$' from the string val
    :rtype: (float)
    """
    return float(string_val.replace("$", ""))


def parse_to_float(val):
    """Convert given numeric value to float number and round it off
       e.g. parse_to_float(25.9345) -> 25.94

    :param val: Numeric value to be converted to float and round it off
    :type val: (int/float)
    :return: Rounded float value for a given numeric value
    :rtype: (float)
    """
    return round(float(val), 2)


def parse_months(file_name):
    """Function to get current and new month by parsing a given file name without extension
       e.g. parse_months("SummaryBillApr2020") -> {"prev_month": "Mar", current_month": "Apr", "next_month": "May"}

    :param file_name: Name of the file to parse
    :type file_name: (str)
    :return: Abbrevation of current month and new month
    :rtype: (dict)
    """
    current_year = str(datetime.today().year)
    month_abbr = file_name.replace(current_year, "")[-3:]
    month_num = list(calendar.month_abbr).index(month_abbr)
    if month_num == 12:
        new_month = 1
    else:
        new_month = month_num + 1
    if month_num == 1:
        prev_month = 12
    else:
        prev_month = month_num - 1
    new_month_abbr = calendar.month_abbr[new_month]
    prev_month_abbr = calendar.month_abbr[prev_month]
    return {
        "prev_month": prev_month_abbr,
        "current_month": month_abbr,
        "next_month": new_month_abbr,
    }


def validate_email(email_address):
    """Function to check if provide email is valid

    :param email_address: Email address to be validated
    :type email_address: (str)
    """
    if "@" not in email_address:
        return False
    if ".com" not in email_address and ".edu" not in email_address:
        return False
    if len(email_address) < 5:
        return False
    if email_address.split("@")[0] == "":
        return False
    return True


def parse_json_data(file_path):
    """Function to parse json data from a given json file

    :param file_name: Path to json file
    :type file_name: (str)
    :return: data parsed from json file
    :rtype: (json)
    """
    with open(file_path) as file_name:
        data = json.load(file_name)
    return data


def clean_chunk(data_chunk):
    """Function to clear addtional variables from data chunk

    :param data_chunk: Data chunk before identifying all charges
    :type data_chunk: (str)
    :return: filtered data chunk
    :rtype: (str)
    """
    filters = [" - New", "\xa0", " - Transferred to T-Mobile", " - Old number"]
    for filter_ in filters:
        data_chunk = data_chunk.replace(filter_, "")
    return data_chunk


def get_year(months):
    """Function to get exact year based on current and next month

    :param months: Dict containing current and next month
    :type months: (dict)
    :return: Year calculated based on current and next month
    :rtype: (int)
    """
    if months["next_month"] == "Jan":
        year_ = datetime.today().year + 1
    else:
        year_ = datetime.today().year
    return year_
