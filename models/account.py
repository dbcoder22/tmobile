#!/usr/bin/python

import sys
sys.path.append("./")
from utilities.utils import parse_to_float, parse_to_num

class Account(object):

    def __init__(self, all_lines, account_total):
        self.lines = all_lines
        self.account_total = account_total
        self.tax_total = self._get_tax_total()
    
    @property
    def no_of_lines(self):
        return len(self.lines)
    
    def _get_tax_total(self):
        total_tax = 0
        for line in self.lines:
            total_tax += line.tax
        return parse_to_float(total_tax)
    
    def get_basic_charge(self):
        extra_charge_on_line = (self.no_of_lines - 4) * 20
        total_charges = self.account_total + extra_charge_on_line
        return parse_to_float(total_charges/self.no_of_lines)
    
    def get_tax_charge(self):
        return parse_to_float(self.tax_total/self.no_of_lines) 
    

