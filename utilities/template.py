#!/usr/bin/python

def get_email_template(file_name, user, month, old_month, year):
    
    boiler_plate = """Hello {user},\n
                    \nFollowing is the bill details for month of {month} {year} (This cover billing cycle from {oldmonth} 19 - {month} 18)\n
                    \nAuto-pay is enabled. If you need any copy of the bill for reimbursement please make sure you get it before {month} 11th.\n
                    \nPlease venmo me the payments or send to me on my phone number via Zelle.\n"""
    return boiler_plate.format(user=user, month=month, year=year, oldmonth=old_month)
