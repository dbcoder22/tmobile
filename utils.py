#!/usr/bin/python

def _parse_to_num(string_val):
    """Convert given value to a numeric value

    :param string_val: Value to be converted to numerical value
    :type string_val: (str)
    :return: Converted float value to string and remove '$' from the string val
    :rtype: (float)
    """
    return float(string_val.replace("$", ""))


def _parse_to_float(val):
    """Convert given numeric value to float number and round it off

    :param val: Numeric value to be converted to float and round it off
    :type val: (int/float)
    :return: Rounded float value for a given numeric value
    :rtype: (float)
    """
    return round(float(val), 2)