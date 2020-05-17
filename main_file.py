#!/usr/bin/python

from tika import parser
from libs.tmobile import TMobile
from models.account import Account
from models.line import Line 
from utils import _parse_to_float
from tabulate import tabulate
from email_cli import EmailClient
from datetime import date
import json

if __name__ == '__main__':
    path = 'SummaryBillApr2020.pdf'
    raw = parser.from_file(path)
    data = raw['content'].split("\n")
    
    email_ = EmailClient()
    tmobile = TMobile(raw_data=data) 
    account_to_data = tmobile.get_account_data_mapping()
    lines = [Line(account) for account in account_to_data]
    account = Account(all_lines=lines, account_total=tmobile.account_total)
    
    tax_on_each_line = account.get_tax_charge()
    basic_on_each_line = account.get_basic_charge()    
    
    # Added automated date and year
    # Add email mapping in Line class
    # Check individual emails
    # Add test cases
    grand_total = 0
    subject = "T-Mobile ({} {})".format(date.month)
    headers = ["Line", "Type", "Equipment", "Services", "One-time", "Basic", "Tax", "Total"]
    table_data = []
    for _acc_ in lines:
        total_charges = _parse_to_float(
                        _acc_.equipment + 
                        _acc_.services + 
                        tax_on_each_line + 
                        basic_on_each_line)
        chunk = (_acc_.line, 
                 _acc_.type, 
                 _acc_.equipment,
                 _acc_.services, 
                 _acc_.one_time_charge,
                 basic_on_each_line,
                 tax_on_each_line,
                 "${}".format(total_charges))
        table_data.append(chunk)
        tabular_data = tabulate(table_data, headers=headers, tablefmt="grid")
        message = email_.create_message(sender="sbagde.projects@gmail.com", 
                                        to=_acc_.email, 
                                        subject=, message_text=body)
    email_.send_message(message=message)
    grand_total += total_charges