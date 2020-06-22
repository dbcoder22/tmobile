#!/usr/bin/python
"""
This module provides all unique dependent functions binded by the
sole purpose of helping business logic in main. All functions are
pre-defined string templates
"""


def get_email_template(user, month, next_month, year):
    """Function to generate email template that would include
       the given user, month, next month and year

    :param user: Name of the user whom email is addressed
    :type user: (str)
    :param month: Abbr of current month
    :type month: (str)
    :param next_month: Abbr of next month
    :type next_month: (str)
    :param year: Current year
    :type year: (int)
    :return: Email template that includes user, month, next month and year
    :rtype: (str)
    """
    boiler_plate = "**********   THIS IS AN AUTO-GENERATED EMAIL **********\
       \nHello {user},\n\
       \nFollowing is the bill details for month of {month} {year} (This cover billing cycle from {month} 19 - {next_month} 18)\n\
       \nAuto-pay is enabled. If you need any copy of the bill for reimbursement please make sure you get it before {next_month} 11th\n\
       \nYou may have recieved an auto-generated Venmo request on my behalf for this {next_month}\n"
    return boiler_plate.format(user=user, month=month, year=year, next_month=next_month)


def get_help(input_file):
    """Function to get the help menu for this application

    :param input_file: Path to the input file that stores input variables
    :type input_file: (str)
    """
    print(
        '\nIncorrect inputs provided. Please configure file={} as an example below:\
         \n\t-"path": (Full path) Path to summary bill .pdf file\
         \n\t-"email": (True | False) Toggle for sending email to users\
         \n\t-"sender": Email of the sender\
         \n\t-"venmo": (True | False) for to generate venmo requests(venmo.json required)\
         \n\t-"user": User from (configs/users.json) who the venmo requests will be sent'.format(
            input_file
        )
    )
