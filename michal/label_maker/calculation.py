from functools import total_ordering


def calculate_unit_price(data):
    ''''
    Add key 'unit_price' key to dict, value = total_price / quantity
    '''

    for item in data:
        item['unit_price'] = item['total_price'] / item['qty']

    return data

def prepare_output_dic(input_dict):
    '''
    Link data dict to ouptut dict as follows

    input_dict              output_dict
    form: str               top_row: str  
    name: str               top_row: str
    quantity: int           top_row: str
    total_price: float      price: str -> middle row
    unit: str               bottom_row: str
    unit_price: float       bottom_row: str
    '''

    output_dict = {}

    # alien code
    #total_price = input_dict['total_price']
    #price = f'{total_price},-' # middle row
    #output_dict['price'] = price

    top_row = f'{input_dict["name"]} {input_dict["form"]} {input_dict["qty"]} {input_dict["units"]}'
    bottom_row = f'1{input_dict["units"]} = {input_dict["unit_price"]}CZK'
    middle_row = f'{input_dict["total_price"]}'
    output_dict['top_row'] = top_row
    output_dict['middle_row'] = middle_row
    output_dict['bottom_row'] = bottom_row

    return output_dict

def prepare_output_list(input_data):
    output_list = []

    for data in input_data:
        item = prepare_output_dic(data)
        output_list.append(item)

    return output_list


# home work: zajistete, aby vysledny list mel delku 36 polozek
# kdyz bude list delsi, rozdel to
# kdyz kratsi, dopln ''
# pripravit si CSV file delsi nez 36 polozek