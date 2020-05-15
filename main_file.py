from tika import parser
import json

def get_start_end_positions(info):
    start_pos = end_pos = 0
    for _, detail in enumerate(info):
        if "SUMMARY" in detail:
            start_pos = _
        if "DETAILED" in detail:
            end_pos = _
        if start_pos > 0 and end_pos > 0:
            break
    return {'start' : start_pos, 'end' : end_pos}

def _parse_to_num(dollar_val):
    return float(dollar_val.replace("$", ""))

def _parse_to_float(num_val):
    return round(float(num_val), 2)

def get_titles(data):
    return data[0].split()


def get_account_total(data):
    return _parse_to_num(data[4].split()[-1])

def get_account_data_mapping(data, titles):
    account_to_data = []
    real_data = data[5:]
    for chunk in real_data:
        if len(chunk) > 0: 
            data_ = chunk.split(" ")
            data_obj = {}
            for d, t in zip(data_, titles):
                data_obj[t] = d.replace(u'\xa0', u'')
            account_to_data.append(data_obj)
    return account_to_data 


def get_basic_charge(account_total, no_of_lines):
    free_lines = no_of_lines - 4
    extra_charge_on_line = free_lines * 20
    return _parse_to_float((account_total + extra_charge_on_line)/no_of_lines)

def get_tax_charge(data, no_of_lines):
    total_tax = 0
    for _, account in enumerate(data):
        tax = _parse_to_num(account["Plans"])
        if tax > 20:
            tax = tax - 20
        total_tax += tax
    return _parse_to_float(total_tax/no_of_lines)


if __name__ == '__main__':
    path = 'SummaryBillApr2020.pdf'
    raw = parser.from_file(path)
    data = raw['content'].split("\n")
    positions = get_start_end_positions(data)
    needed_data = data[positions['start'] + 1:positions['end']]
    titles = get_titles(needed_data)
    account_total = get_account_total(needed_data)
    titles_mapped_account = get_account_data_mapping(needed_data, titles)
    number_of_lines = len(titles_mapped_account)
    basic_charge_on_each = get_basic_charge(account_total, number_of_lines)
    tax_on_each = get_tax_charge(titles_mapped_account, number_of_lines)
    grand_total = 0
    for _, account in enumerate(titles_mapped_account):
        if account["Equipment"] == "-": 
            equipment = 0 
        else: 
            equipment = _parse_to_num(account["Equipment"])
        if account["Services"] == "-":
            services = 0
        else:
            services = _parse_to_num(account["Services"])
        print("\nAccount {}".format(_))
        print("----------")
        print("Line:{}".format(account["Line"]))
        print("Basic charge:{}".format(basic_charge_on_each))
        print("Taxes:{}".format(tax_on_each))
        print("Equipment:{}".format(equipment))
        print("Services:{}".format(services))
        total_charges = equipment + services + tax_on_each + basic_charge_on_each
        print("----------")
        print("Total:${}".format(_parse_to_float(total_charges)))
        grand_total += total_charges
    print("\nGrand Total:${}".format(_parse_to_float(grand_total)))
    