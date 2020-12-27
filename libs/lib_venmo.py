#!/usr/bin/python
"""
Module pertaining to Venmo account and other functionalities
"""
import os
import logging
from venmo_api import Client
from tmobile.utilities.utils import parse_json_data, UserNotFound

logger = logging.getLogger(__name__)


class Venmo:
    """
    Main class to perform operations via Venmo
    """

    __venmo_file__ = "configs/venmo.json"

    def __init__(self):
        if not os.path.exists(Venmo.__venmo_file__):
            raise FileNotFoundError(
                "Please created venmo.json file containing your access token"
            )
        data = parse_json_data(Venmo.__venmo_file__)
        self.users = data["users"]
        self.client = Client(access_token=data["token"])

    def get_user(self, user_name):
        """Function to get user details by Venmo repository

        :param user_name: User-name of the user whose details need to be fetched
        :type user_name: (str)
        :raises UserNotFound: If given user-name is not found in Venmo repository
        :return: Details of user fetched form the venmo repository
        :rtype: (NamedTuple)
        """
        users = self.client.user.search_for_users(query=user_name, page=1)
        if len(users) < 1:
            err = "User={} does not exits, please check venmo user name in venmo.json file".format(
                user_name
            )
            raise UserNotFound(err)
        return users[0]

    def request(self, note, user_id, amount, addtional_amount=0):
        """Function to perform a venmo request to given user id with given amount and note

        :param note: Note to be added to the venmo request
        :type note: (str)
        :param user_id: Id of the user whom request needs to be sent
        :type user_id: (int)
        :param amount: Amount to be requested
        :type amount: (int)
        :param addtional_amount: Additional amount to added to the request, defaults to 0
        :type addtional_amount:(int), optional
        """
        total_amount = amount + addtional_amount
        if total_amount < 0:
            logger.info("Total amount < 0, request not sent")
        else:
            self.client.payment.request_money(total_amount, note, user_id)
