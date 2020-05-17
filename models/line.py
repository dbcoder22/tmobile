#!/usr/bin/python

import json
import sys
sys.path.append("./")
from utilities.utils import parse_to_num, parse_to_float

class Line(object):

    def __init__(self, prop):
        self.prop = prop
        self.line = self.prop["Line"]
        self.type = self.prop["Type"]
        self.one_time_charge = self._get_onetime_charge()
        self.equipment = self._get_equipment()
        self.services = self._get_services()
        self.tax = self._get_tax()
        self.user = self._get_user_info()

    def _get_user_info(self):
        with open("configs/users.json") as f:
            user_info = json.loads(f.read())
        return user_info[self.line]

    def _get_equipment(self):
        if self.prop["Equipment"] == "-": 
            return 0 
        else: 
            return parse_to_num(self.prop["Equipment"])
    
    def _get_services(self):
        if self.prop["Services"] == "-":
            return 0
        else:
            return parse_to_num(self.prop["Services"])

    def _get_tax(self):
        tax = parse_to_num(self.prop["Plans"])
        if tax > 20:
            tax = tax - 20
        return parse_to_float(tax)

    def _get_onetime_charge(self):
        if self.prop.get("One-time charges") is None or self.prop.get("One-time charges") == "-":
            return 0
        else:
            return parse_to_num(self.prop["One-time charges"])