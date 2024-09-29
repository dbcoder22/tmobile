#!/usr/bin/python3
"""
This is pytest file to perform unit tests associated with libs library.
For each function in libs library we have a test with all possible input/output combinations
"""
import pytest
from tmobile.libs.lib_email import create_message
from tmobile.libs.lib_tmobile import TMobile

__test_dummy_data__ = [
    "T-Mobile",
    "",
    "",
    "Bill period",
    "Mar 19, 2020 - Apr 18, 2020",
    "",
    "Account",
    "000123",
    "",
    "Page",
    "1\xa0of\xa06",
    "",
    "TOTAL DUE",
    "DETAILED",
    "$317.53",
    "Your bill is due by May 11, 2020.",
    "",
    "AutoPay is scheduled for May 09, 2020 using Visa",
    "****1234.",
    "",
    "Thanks for paying your last bill of $314.62.",
    "",
    "Hi Mark,",
    "Here's your bill for April.",
    "You're on AutoPay. Thanks for being an awesome T-Mobile customer. With your Simple",
    "Choice plans, you have unlimited talk, text and data with flexible high-speed tiers.",
    "",
    "PLANS",
    "",
    "$259.63",
    "\xa09\xa0VOICE\xa0LINES\xa0=\xa0$259.63\xa0",
    "",
    "This month's charges are $0.12 less",
    "",
    "• Thanks for being a part of the T-Mobile family!",
    "",
    "COMPARE YOUR PLAN MONTH-TO-MONTH",
    "",
    "$259.75",
    "",
    "Jan",
    "",
    "  $259.75",
    "",
    "Feb",
    "",
    "  $259.75",
    "",
    "Mar",
    "",
    "  $259.63",
    "",
    "Apr",
    "",
    " ",
    "",
    "EQUIPMENT",
    "",
    "$22.34",
    "\xa02\xa0HANDSETS\xa0=\xa0$22.34\xa0",
    "",
    "This month's charges are the same as last month's",
    "",
    "SUMMARY",
]

__test_dummy_data_len__ = len(__test_dummy_data__)

__test_actual_data__ = [
    "Previous balance $314.62",
    "",
    "Payment - thank you Mar 28 -$60.00",
    "",
    "Payment - thank you Apr 09 -$254.62",
    "",
    "THIS BILL SUMMARY",
    "Line Type Plans Equipment Services Total",
    "",
    "Totals $259.63 $22.34 $35.56 $317.53",
    "",
    "Account $120.57 - - $120.57",
    "",
    "(123)\xa0456-7890 Voice $4.29 - - $4.29",
    "",
    "(123)\xa0456-7980 Voice $4.29 - $16.37 $20.66",
    "",
    "(123)\xa0456-8970 Voice $4.29 - - $4.29",
    "",
    "DETAILED CHARGES",
    "",
    "PLANS $259.63",
    "",
    "REGULAR CHARGES Apr 19 - May 18 $220.00",
    "",
]


def test_create_email_message():
    """
    Test create email message function
    """
    msg = create_message(
        "abc@gmail.com", "bcd@gmail.com", "Test email", "This is text of a test email"
    )
    assert isinstance(msg["raw"], str)
    assert "abc@gmail.com" not in msg["raw"]
    assert "bcd@gmail.com" not in msg["raw"]
    assert "Test email" not in msg["raw"]
    assert "This is text of a test email" not in msg["raw"]


@pytest.mark.parametrize(
    ("data_"),
    [
        __test_dummy_data__[:__test_dummy_data_len__],
        __test_dummy_data__[__test_dummy_data_len__:],
    ],
)
def test_tmobile_error(data_):
    """
    Test create TMobile object error
    """
    with pytest.raises(OSError):
        TMobile(raw_data=data_)


def test_tmobile_functions():
    """
    Test class TMobile and functions with class TMobile
    """
    tmobile_ = TMobile(raw_data=__test_actual_data__)
    assert "Line" in tmobile_.titles
    assert "Equipment" in tmobile_.titles
    assert tmobile_.account_total == 317.53
    account_data_map = tmobile_.get_account_data_mapping()
    assert len(account_data_map) == 3
    assert account_data_map[0]["Line"] == "(123)456-7890"
    assert account_data_map[1]["Services"] == "$16.37"
    assert account_data_map[1]["Total"] == "$20.66"
    assert account_data_map[2]["Plans"] == "$4.29"
