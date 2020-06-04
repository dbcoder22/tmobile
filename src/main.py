#!/usr/bin/python
"""
Contains the workflow of T-Mobile application with following roles:
    - Read pdf
    - String parsing
    - Perform calculation pertaining to each line on the plan
    - Generates an individual report for each line user
    - Sends email with details to each user
    - Creates a Venmo request to each user
Configuration needed:
    - credentials.json: Json file containing the key configuration for google imap email api
    - input.json: Json file containing inputs to be provided to the application
    - users.json:  Json file containing user details (line, name, email etc.)
    - venmo.json: Json file containing venmo related details for all users
    - SummaryBillMMMYYYY.pdf : File obtained from family head's T-Mobile account each month
"""
from datetime import datetime
import json
import os
import sys
from tika import parser
from tabulate import tabulate
from tmobile.models.line import Line
from tmobile.models.account import Account
from tmobile.utilities.template import get_email_template, get_help
from tmobile.utilities.utils import (
    parse_to_float,
    parse_months,
    validate_email,
    UserNotFound,
)
from tmobile.libs.lib_email import EmailClient, create_message
from tmobile.libs.lib_tmobile import TMobile
from tmobile.libs.lib_venmo import Venmo


def update_and_validate_inputs(_data):
    """Function to validate all input variables and update boolean values

    :param _data: Data obtained from configs/input.json
    :type _data: (dict)
    :raises ValueError: For any invalid inputs provided
    :return: Updated/Validated input values
    :rtype: (dict)
    """
    if len(_data.keys()) < 5:
        raise ValueError("Not enough parameters found")
    for k, val in _data.items():
        if k in ["venmo", "email"]:
            if val.lower() not in ["true", "false"]:
                raise ValueError('Incorrect value provided for boolean "{}"'.format(k))
        if k == "sender" and not validate_email(val):
            raise ValueError("Incorrect email address provided")
        if val == "":
            raise ValueError("Values not provided as expected")
        if val.lower() == "true":
            _data[k] = True
        elif val.lower() == "false":
            _data[k] = False
    return _data


def get_args():
    """Function to get arguments passed to application by the user

    :return: Arguments passed to appliaction by the user
    :rtype: (dict)
    """
    input_file = "configs/input.json"
    print("\nWelcome to T-Mobile bill generator application\n")
    if not os.path.exists(input_file):
        get_help(input_file)
        raise FileNotFoundError("\nPlease create file={}".format(input_file))
    with open(input_file) as user_input_file:
        input_data = json.load(user_input_file)
        try:
            update_and_validate_inputs(input_data)
            return input_data
        except ValueError as gen_error:
            get_help(input_file)
            print(
                "\nPlease update {} with correct configuration. ERROR: {}".format(
                    input_file, gen_error
                )
            )
            sys.exit(1)


if __name__ == "__main__":

    args = get_args()
    base_name, ext = os.path.splitext(os.path.basename(args["path"]))
    raw = parser.from_file(args["path"])
    data = raw["content"].split("\n")

    email_cli = EmailClient()
    tmobile = TMobile(raw_data=data)
    account_to_data = tmobile.get_account_data_mapping()
    lines = [Line(account) for account in account_to_data]
    account = Account(all_lines=lines, account_total=tmobile.account_total)

    tax_on_each_line = account.get_tax_charge()
    basic_on_each_line = account.get_basic_charge()

    months = parse_months(file_name=base_name)
    curr_year = datetime.today().year
    SUBJECT = "T-Mobile({} {})".format(months["current_month"], curr_year)
    GRAND_TOTAL = 0
    headers = [
        "User",
        "Line",
        "Type",
        "Equipment",
        "Services",
        "One-time",
        "Basic",
        "Tax",
        "Total",
    ]
    table_data = []
    for _acc_ in lines:
        total_charges = parse_to_float(
            _acc_.equipment + _acc_.services + tax_on_each_line + basic_on_each_line
        )
        chunk = (
            _acc_.user["name"],
            _acc_.line,
            _acc_.linetype,
            _acc_.equipment,
            _acc_.services,
            _acc_.one_time_charge,
            basic_on_each_line,
            tax_on_each_line,
            "${}".format(total_charges),
        )
        tabular_data = tabulate([chunk], headers=headers, tablefmt="grid")
        print(tabular_data)
        GRAND_TOTAL += total_charges

        if args["test"]:
            continue
        if args["email"]:
            EMAIL_TEMPLATE = get_email_template(
                user=_acc_.user["name"],
                month=months["current_month"],
                old_month=months["old_month"],
                year=curr_year,
            )

            message = create_message(
                sender_email=args["sender"],
                to_email=_acc_.user["email"],
                subject=SUBJECT,
                message_text="{}\n{}".format(EMAIL_TEMPLATE, tabular_data),
            )
            if email_cli.send_message(message=message):
                print(
                    "Email to user={} for line={}\t\t\t\tSUCCESS".format(
                        _acc_.user["name"], _acc_.line
                    )
                )
            else:
                print(
                    "Email to user={} for line={}\t\t\t\tFAILED".format(
                        _acc_.user["name"], _acc_.line
                    )
                )
        if args["venmo"] and args["user"].lower() != _acc_.user["name"].lower():
            print("Sending Venmo request ...")
            venmo_ = Venmo()
            try:
                v_name = venmo_.users[_acc_.line]
                user_details = venmo_.get_user(user_name=v_name["venmo_username"])
                venmo_.request(
                    note=SUBJECT + v_name["additional_note"],
                    user_id=user_details.id,
                    amount=total_charges,
                    addtional_amount=v_name["additonal_amount"],
                )
                print(
                    "Request to user={} for line={}\t\t\t\tSUCCESS".format(
                        user_details.id, _acc_.line
                    )
                )
            except UserNotFound as err:
                print(err)
                print(
                    "Request to user={} for line={}\t\t\t\tFAILED".format(
                        _acc_.user["name"], _acc_.line
                    )
                )
    print("TOTAL AMOUNT: {}".format(GRAND_TOTAL))
