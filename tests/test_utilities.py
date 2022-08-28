#!/usr/bin/python3
"""
This is pytest file to perform unit tests associated with utilities library.
For each function in utitlies library we have a test with all possible input/output combinations
"""
from datetime import datetime
import pytest
from tmobile.utilities.template import get_email_template
from tmobile.utilities.utils import (
    parse_months,
    parse_to_float,
    parse_to_num,
    clean_chunk,
    get_year,
)


@pytest.mark.parametrize(
    ("user", "prev_month", "month", "new_month", "year"),
    [
        ("Rob", "Mar", "Apr", "May", 2020),
        ("Mark", "Aug", "Sep", "Oct", 2021),
        ("John", "Nov", "Dec", "Jan", 2019),
        ("Patrick", "Dec", "Jan", "Feb", 2019),
    ],
)
def test_get_email_template(user, prev_month, month, new_month, year):
    """
    Test function get_email_template
    """
    template = get_email_template(user, prev_month, month, new_month, year)
    assert "Hello {}".format(user) in template
    assert "{} {}".format(month, year) in template
    assert "{} 19".format(prev_month) in template
    assert "{} 18".format(month) in template
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
        (
            "SummaryBillApr",
            {"prev_month": "Mar", "current_month": "Apr", "next_month": "May"},
        ),
        (
            "SummaryBillDec",
            {"prev_month": "Nov", "current_month": "Dec", "next_month": "Jan"},
        ),
        (
            "SummaryBillJan",
            {"prev_month": "Dec", "current_month": "Jan", "next_month": "Feb"},
        ),
    ],
)
def test_parse_months(input_string, expected_val):
    """
    Test parse_months function
    """
    input_string += str(datetime.today().year)
    parsed_months = parse_months(input_string)
    for key in ["prev_month", "current_month", "next_month"]:
        assert parsed_months[key] == expected_val[key]


@pytest.mark.parametrize(
    ("data_chunk", "expected_datachunk"),
    [
        ("(123) 1234-342 Voice", "(123) 1234-342 Voice"),
        ("(123) 1234-342 - New Voice", "(123) 1234-342 Voice"),
    ],
)
def test_clean_chunk(data_chunk, expected_datachunk):
    """
    Test clean_chink function
    """
    assert clean_chunk(data_chunk) == expected_datachunk


@pytest.mark.parametrize(
    ("months", "expected_year"),
    [
        ({"current_month": "Apr", "next_month": "May"}, datetime.today().year),
        ({"current_month": "Dec", "next_month": "Jan"}, datetime.today().year + 1),
    ],
)
def test_get_year(months, expected_year):
    """
    Test get_year function
    """
    assert get_year(months=months) == expected_year
