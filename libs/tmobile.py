#!/usr/bin/python

import sys
sys.path.append("./")
from utils import _parse_to_num

class TMobile(object):
    
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.positions = self._get_start_end_positions()
        self.data = self._get_data()
        self.account_total = self._get_account_total()
        self.titles = self._get_titles()

    def _get_data(self):
        return self.raw_data[self.positions['start'] + 1:self.positions['end']]
    
    def _get_start_end_positions(self):
        start_pos = end_pos = 0
        for _, detail in enumerate(self.raw_data):
            if "SUMMARY" in detail:
                start_pos = _
            if "DETAILED" in detail:
                end_pos = _
            if start_pos > 0 and end_pos > 0:
                break
        return {'start' : start_pos, 'end' : end_pos}

    def _get_account_total(self):
        content = self.data[4].split()
        return _parse_to_num(content[-1])
    
    def _get_titles(self):
        return self.data[0].split()

    def get_account_data_mapping(self):
        account_to_data = []
        real_data = self.data[5:]
        for chunk in real_data:
            if len(chunk) > 0: 
                data_ = chunk.split(" ")
                data_obj = {}
                for d, t in zip(data_, self.titles):
                    data_obj[t] = d.replace(u'\xa0', u'')
                account_to_data.append(data_obj)
        return account_to_data