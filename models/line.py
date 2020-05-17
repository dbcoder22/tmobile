#!/usr/bin/python

import sys
sys.path.append("./")
from utils import _parse_to_num, _parse_to_float

class Line(object):

    def __init__(self, prop):
        self.prop = prop
        self.line = self.prop["Line"]
        self.type = self.prop["Type"]
        self.one_time_charge = self._get_onetime_charge()
        self.equipment = self._get_equipment()
        self.services = self._get_services()
        self.tax = self._get_tax()
    
    def _get_equipment(self):
        if self.prop["Equipment"] == "-": 
            return 0 
        else: 
            return _parse_to_num(self.prop["Equipment"])
    
    def _get_services(self):
        if self.prop["Services"] == "-":
            return 0
        else:
            return _parse_to_num(self.prop["Services"])

    def _get_tax(self):
        tax = _parse_to_num(self.prop["Plans"])
        if tax > 20:
            tax = tax - 20
        return _parse_to_float(tax)

    def _get_onetime_charge(self):
        if self.prop.get("One-time charges") is None or self.prop.get("One-time charges") == "-":
            return 0
        else:
            return _parse_to_num(self.prop["One-time charges"])