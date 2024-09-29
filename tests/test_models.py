#!/usr/bin/python3
"""
This is pytest file to perform unit tests associated with models library.
For each function in models library we have a test with all possible input/output combinations
"""
import json
import pytest
from mock import patch, Mock
from tmobile.models.account import Account
from tmobile.models.line import Line
from tmobile.utilities.utils import UserNotFound


__all_line_props__ = [
    {
        "prop": {
            "Line": "123456789",
            "Type": "Voice",
            "Equipment": "$10",
            "Services": "$15",
            "Plans": "$24.43",
            "One-time charges": "$0",
        },
        "test_info_file": "/tmp/test_info_line.json",
    },
    {
        "prop": {
            "Line": "234567891",
            "Type": "Voice",
            "Equipment": "$0",
            "Services": "$0",
            "Plans": "$24.43",
            "One-time charges": "$22",
        },
        "test_info_file": "/tmp/test_info_line.json",
    },
]

__test_data__ = dict()

__test_data__["123456789"] = {"name": "Abcd", "email": "abcd@gmail.com"}

__test_data__["234567891"] = {"name": "Efgh", "email": "efgh@gmail.com"}

__test_info_file__ = "/tmp/test_info_line.json"

with open(__test_info_file__, "w") as test_file:
    json.dump(__test_data__, test_file, indent=4)


def test_create_line_object_error_case():
    """
    Test FileNotFoundError
    """
    with pytest.raises(FileNotFoundError):
        Line(prop=__all_line_props__[0], user_info_file="non_existant_file.json")


@patch("tmobile.models.line.Line.get_user")
def test_create_line_object_missing_user_name(user):
    """
    Test UserNotFound for missing user_name
    """
    mock_data = Mock()
    mock_data = {"email": "abcd@gmail.com"}
    user.return_value = mock_data
    with pytest.raises(UserNotFound):
        Line(prop=__all_line_props__[0]["prop"], user_info_file=__test_info_file__)


@patch("tmobile.models.line.Line.get_user")
def test_create_line_object_missing_user_email(_user):
    """
    Test UserNotFound for missing email
    """
    mock_data = Mock()
    mock_data = {"user": "abcd"}
    _user.return_value = mock_data
    with pytest.raises(UserNotFound):
        Line(prop=__all_line_props__[0]["prop"], user_info_file=__test_info_file__)


@patch("tmobile.models.line.Line.get_user")
def test_create_line_object_incorrect_user_email(user):
    """
    Test UserNotFound for incorrect user_email
    """
    mock_data = Mock()
    mock_data = {"user": "abcd", "email": "abcd@"}
    user.return_value = mock_data
    with pytest.raises(UserNotFound):
        Line(prop=__all_line_props__[0]["prop"], user_info_file=__test_info_file__)

    user.side_effect = {"user": "abcd", "email": "@gmail.com"}

    with pytest.raises(UserNotFound):
        Line(prop=__all_line_props__[0]["prop"], user_info_file=__test_info_file__)


@pytest.mark.parametrize(("prop_"), [x["prop"] for x in __all_line_props__])
def test_all_functions(prop_):
    """
    Test all class Line functions
    """
    line_ = Line(prop=prop_, user_info_file=__test_info_file__)
    assert line_.line == prop_["Line"]
    assert line_.equipment in [0, 10]
    assert line_.services in [0, 15]
    assert line_.one_time_charge in [0, 22]
    assert line_.tax == 4.43
    assert line_.user["name"] in ["Abcd", "Efgh"]
    assert line_.user["email"] in ["abcd@gmail.com", "efgh@gmail.com"]


def test_all_account():
    """
    Test all class Accoount functions
    """
    lines_ = [
        Line(prop=x["prop"], user_info_file=x["test_info_file"])
        for x in __all_line_props__
    ]
    account_ = Account(all_lines=lines_, account_total=50)
    assert account_.get_basic_charge() == 25
    assert account_.get_tax_charge() == 4.43
    assert account_.no_of_lines == 2
    assert account_.tax_total == 8.86
