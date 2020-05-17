#!/usr/bin/python
import json
import sys
import os
sys.path.append("./")
from datetime import datetime
from tika import parser
from tabulate import tabulate
from libs.lib_tmobile import TMobile
from libs.lib_email import EmailClient
from models.account import Account
from models.line import Line 
from utilities.utils import parse_to_float, parse_months
from utilities.template import get_email_template

if __name__ == '__main__':
    bill_document_path = 'SummaryBillApr2020.pdf'
    base_name, ext = os.path.splitext(os.path.basename(bill_document_path))
    raw = parser.from_file(bill_document_path)
    data = raw['content'].split("\n")
    
    email_ = EmailClient()
    tmobile = TMobile(raw_data=data) 
    account_to_data = tmobile.get_account_data_mapping()
    lines = [Line(account) for account in account_to_data]
    account = Account(all_lines=lines, account_total=tmobile.account_total)
    
    tax_on_each_line = account.get_tax_charge()
    basic_on_each_line = account.get_basic_charge()    
    
    months = parse_months(file_name=base_name)
    curr_year = datetime.today().year
    grand_total = 0
    headers = ["User", "Line", "Type", "Equipment", "Services", "One-time", "Basic", "Tax", "Total"]
    table_data = []
    for _acc_ in lines:
        total_charges = parse_to_float(
                        _acc_.equipment + 
                        _acc_.services + 
                        tax_on_each_line + 
                        basic_on_each_line)
        chunk = (_acc_.user["name"],
                 _acc_.line, 
                 _acc_.type, 
                 _acc_.equipment,
                 _acc_.services, 
                 _acc_.one_time_charge,
                 basic_on_each_line,
                 tax_on_each_line,
                 "${}".format(total_charges))
        tabular_data = tabulate([chunk], headers=headers, tablefmt="grid")
        emailtemplate = get_email_template(file_name=base_name,
                                            user=_acc_.user["name"],
                                            month=months["current_month"],
                                            old_month=months["old_month"],
                                            year=curr_year)
        
        message = email_.create_message(sender_email="sbagde.projects@gmail.com", 
                                        to_email=_acc_.user["email"], 
                                        subject="T-Mobile({} {})".format(months["current_month"], curr_year), 
                                        message_text="{}\n{}".format(emailtemplate, tabular_data))
        email_.send_message(message=message)