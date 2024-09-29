#!/usr/bin/python3
"""
Module pertaining to T-Mobile account details that are parsed from PDF provided by the user
"""
from tmobile.utilities.utils import parse_to_num, clean_chunk


class TMobile:
    """
    Main class to perform get details pertaining to T-Mobile account
    """

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.positions = self._get_start_end_positions()
        self.plan_total = self._get_plan_total()
        self.account_total = self._get_account_total()
        self.titles = self.get_titles()

    @property
    def _data(self):
        """Private function to get required chunk of the data from the file

        :return: Required data from the file
        :rtype: (str)
        """
        start = self.positions["start"] + 1
        end = self.positions["end"]
        return self.raw_data[start:end]

    def _get_start_end_positions(self):
        """Function to parse the bill and get start & end
           positions of required chunk of data from the file

        :return: Start and End position of the chunk of data needed on the file
        :rtype: (dict)
        :raises: OSError if required data is not found in given pdf
        """
        start_pos = end_pos = 0
        for _, detail in enumerate(self.raw_data):
            if "SUMMARY" in detail:
                start_pos = _
            if "DETAILED" in detail:
                end_pos = _
            if start_pos > 0 and end_pos > 0:
                break
        if not 0 <= start_pos < end_pos:
            raise OSError(
                "Could not parse given pdf for required data. \
                Please verify or contact developer"
            )
        return {"start": start_pos, "end": end_pos}

    def _get_plan_total(self):
        """Private function to get plan total

        :return: Total plan amount on account
        :rtype: (int)
        """
        content = self._data[2].split()
        return parse_to_num(content[1])

    def _get_account_total(self):
        """Private function to get total amount on the account

        :return: Total amount on the account
        :rtype: (int)
        """
        content = self._data[2].split()
        return parse_to_num(content[-1])

    def get_titles(self):
        """Function to get titles from T-Mobile summary bill PDF

        :return: List of titles parsed from PDF provided by the user
        :rtype: (list)
        """
        titles = self._data[0].split()
        if "charges" in titles:
            titles.pop(titles.index("charges"))
        return titles

    def get_account_data_mapping(self):
        """Function to get an account to data mapping for each line on account

        :return: List of key-value pairs of account mapped to its details
        :rtype: (list)
        """
        account_to_data = []
        real_data = self._data[5:]
        for chunk in real_data:
            if len(chunk) > 0:
                chunk = clean_chunk(data_chunk=chunk)
                if "Removed" in chunk:
                    continue
                data_ = chunk.split(" ")
                data_obj = {}
                for data_value, data_key in zip(data_, self.titles):
                    data_obj[data_key] = data_value
                account_to_data.append(data_obj)
        return account_to_data
