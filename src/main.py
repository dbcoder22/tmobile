#!/usr/bin/python3
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
import json
import logging
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
    get_year,
)
from tmobile.libs.lib_email import EmailClient, create_message, EmailFailure
from tmobile.libs.lib_tmobile import TMobile
from tmobile.libs.lib_venmo import Venmo


def __update_and_validate_inputs__(_data):
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


def __get_args__():
    """Function to get arguments passed to application by the user

    :return: Arguments passed to appliaction by the user
    :rtype: (dict)
    """
    input_file = "configs/input.json"
    logger.info("\nWelcome to T-Mobile bill generator application\n")
    if not os.path.exists(input_file):
        get_help(input_file)
        raise FileNotFoundError("\nPlease create file=%s" % input_file)
    with open(input_file) as user_input_file:
        input_data = json.load(user_input_file)
        try:
            __update_and_validate_inputs__(input_data)
            return input_data
        except ValueError as gen_error:
            get_help(input_file)
            logger.info(
                "\nPlease update %s with correct configuration. ERROR: %s" % input_file,
                gen_error,
            )
            sys.exit(1)


def __get_total_charges_and_tabular_data__(account_details):
    total_charges = parse_to_float(
        account_details.equipment
        + account_details.services
        + account_details.one_time_charge
        + basic_on_each_line
    )
    chunk = [
        ["User", account_details.user["name"]],
        ["Line", account_details.line],
        ["Type", account_details.linetype],
        ["Equipment", account_details.equipment],
        ["Services", account_details.services],
        ["One-time", account_details.one_time_charge],
        ["Basic (incl Tax)", basic_on_each_line],
        ["Total", "${}".format(total_charges)],
    ]
    tabular_data = tabulate(chunk, tablefmt="grid")
    return tabular_data, total_charges


def __send_email__(account_details, account_data):

    email_template = get_email_template(
        user=account_details.user["name"],
        prev_month=months["prev_month"],
        month=months["current_month"],
        next_month=months["next_month"],
        year=curr_year,
    )

    message = create_message(
        sender_email=args["sender"],
        to_email=account_details.user["email"],
        subject=SUBJECT,
        message_text="{}\n{}".format(email_template, account_data),
    )
    email_cli.send_message(message=message)


def __send_venmo_request__(line, total):
    venmo_ = Venmo()
    v_name = venmo_.users[line]
    user_details = venmo_.get_user(user_name=v_name["venmo_username"])
    venmo_.request(
        note=SUBJECT + v_name["additional_note"],
        user_id=user_details.id,
        amount=total,
        addtional_amount=v_name["additional_amount"],
    )


if __name__ == "__main__":
    sys.tracebacklimit = 0
    logging.basicConfig(
        filename="tmobile.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%m-%d-%Y %I:%M:%S %p",
    )
    logger = logging.getLogger(__name__)
    args = __get_args__()
    base_name, ext = os.path.splitext(os.path.basename(args["path"]))
    raw = parser.from_file(args["path"])
    data = raw["content"].split("\n")

    email_cli = EmailClient()
    tmobile = TMobile(raw_data=data)
    account_to_data = tmobile.get_account_data_mapping()
    lines = [Line(account) for account in account_to_data]
    account = Account(all_lines=lines, account_total=tmobile.plan_total)

    basic_on_each_line = account.get_basic_charge()

    months = parse_months(file_name=base_name)
    curr_year = get_year(months=months)
    SUBJECT = "T-Mobile({} {})".format(months["current_month"], curr_year)
    GRAND_TOTAL = 0
    table_data = []
    logger.info(SUBJECT)
    for _acc_ in lines:
        user_name = _acc_.user["name"]
        data_for_account, sub_total = __get_total_charges_and_tabular_data__(
            account_details=_acc_
        )
        logger.info(data_for_account)
        GRAND_TOTAL += sub_total
        if args["test"]:
            continue
        if args["email"]:
            logger.info("Sending Email ...")
            try:
                __send_email__(account_details=_acc_, account_data=data_for_account)
            except EmailFailure as err:
                logger.exception(err)
                logger.error(
                    "Email to user=%s for line=%s : FAILED" % (user_name, _acc_.line)
                )
            else:
                logger.info(
                    "Email to user=%s for line=%s : SUCCESS" % (user_name, _acc_.line)
                )
        if args["venmo"] and args["user"].lower() != user_name.lower():
            logger.info("Sending Venmo request ...")
            try:
                __send_venmo_request__(line=_acc_.line, total=sub_total)
            except UserNotFound as err:
                logger.info(err)
                logger.info(
                    "Request to user=%s for line=%s : FAILED" % (user_name, _acc_.line)
                )
            else:
                logger.info(
                    "Request to user=%s for line=%s : SUCCESS" % (user_name, _acc_.line)
                )
    logger.info("TOTAL AMOUNT: %s" % GRAND_TOTAL)
