def calculate_unit_price(data):
    ''''
    Add key 'unit_price' key to dict, value = total_price / quantity
    '''

    for item in data:
        item['unit_price'] = item['total_price'] / item['qty']

    return data