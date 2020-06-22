#!/usr/bin/python
"""
This is pytest file to perform unit tests associated with utilities library.
For each function in utitlies library we have a test with all possible input/output combinations
"""
from datetime import datetime
import pytest
from tmobile.utilities.template import get_email_template
from tmobile.utilities.utils import parse_months, parse_to_float, parse_to_num


@pytest.mark.parametrize(
    ("user", "month", "new_month", "year"),
    [
        ("Rob", "Apr", "May", 2020),
        ("Mark", "Sep", "Oct", 2021),
        ("John", "Dec", "Jan", 2019),
    ],
)
def test_get_email_template(user, month, new_month, year):
    """
    Test function get_email_template
    """
    template = get_email_template(user, month, new_month, year)
    assert "Hello {}".format(user) in template
    assert "{} {}".format(month, year) in template
    assert "{} 19".format(month) in template
    assert "{} 18".format(new_month) in template
    assert "before {}".format(new_month) in template


@pytest.mark.parametrize(
    ("string_val", "output_val"),
    [("$123.45", 123.45), ("34.5455", 34.5455), ("$5", 5.0), ("$0", 0), ("-$34", -34)],
)
def test_parse_to_num(string_val, output_val):
    """
    Test function parse_to_num
    """
    assert parse_to_num(string_val) == output_val


@pytest.mark.parametrize(("string_val"), [("$123SSS"), ("-")])
def test_parse_to_num_fail(string_val):
    """
    Test function parse_to_num failure
    """
    with pytest.raises(ValueError):
        parse_to_num(string_val)


@pytest.mark.parametrize(
    ("input_value", "expected_val"),
    [(5, 5), (123.4455, 123.45), (34.5455, 34.55), (-34.4443, -34.44)],
)
def test_parse_to_float(input_value, expected_val):
    """
    Test parse_to_float function
    """
    assert parse_to_float(input_value) == expected_val


@pytest.mark.parametrize(
    ("input_string", "expected_val"),
    [
        ("SummaryBillApr", {"current_month": "Apr", "next_month": "May"}),
        ("SummaryBillDec", {"current_month": "Dec", "next_month": "Jan"}),
    ],
)
def test_parse_months(input_string, expected_val):
    """
    Test parse_months function
    """
    input_string += str(datetime.today().year)
    parsed_months = parse_months(input_string)
    for key in ["current_month", "next_month"]:
        assert parsed_months[key] == expected_val[key]
