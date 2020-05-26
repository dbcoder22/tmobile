#!/usr/bin/python
"""
This is pytest file to perform unit tests associated with utilities library.
For each function in utitlies library we have a test  with sall possible input/output combinations
"""
from datetime import datetime
import pytest
from tmobile.utilities.template import get_email_template
from tmobile.utilities.utils import parse_months, parse_to_float, parse_to_num

@pytest.mark.parametrize(("user", "month", "old_month", "year"), [
    ("Rob", "Apr", "Mar", 2020),
    ("Mark", "Sep", "Aug", 2021),
    ("John", "Jan", "Dec", 2019)
])
def test_get_email_template(user, month, old_month, year):
    template = get_email_template(user, month, old_month, year)
    assert "Hello {}".format(user) in template
    assert "{} {}".format(month, year) in template
    assert "{} 19".format(old_month) in template
    assert "{} 18".format(month) in template
    assert "before {}".format(month) in template


@pytest.mark.parametrize(("string_val", "output_val"), [
    ("$123.45", 123.45),
    ("34.5455", 34.5455),
    ("$5", 5.0),
    ("$0", 0),
    ("-$34", -34)
])
def test_parse_to_num(string_val, output_val):
    assert parse_to_num(string_val) == output_val


@pytest.mark.parametrize(("string_val"), [
    ("$123SSS"),
    ("-")
])
def test_parse_to_num_fail(string_val):
    with pytest.raises(ValueError):
        parse_to_num(string_val)


@pytest.mark.parametrize(("input_value", "expected_val"), [
    (5, 5),
    (123.4455, 123.45),
    (34.5455, 34.55),
    (-34.4443, -34.44)
])
def test_parse_to_float(input_value, expected_val):
    assert parse_to_float(input_value) == expected_val


@pytest.mark.parametrize(("input_string", "expected_val"), [
    ("SummaryBillApr", {"current_month": "Apr", "old_month": "Mar"}),
    ("SummaryBillJan", {"current_month": "Jan", "old_month": "Dec"}),
])
def test_parse_months(input_string, expected_val):
    input_string += str(datetime.today().year)
    parsed_months = parse_months(input_string)
    for key in ["current_month", "old_month"]:
        assert parsed_months[key] == expected_val[key]
