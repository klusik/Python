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
    # total_price = input_dict['total_price']
    # price = f'{total_price},-' # middle row
    # output_dict['price'] = price

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

def split_to_pages(unchunked_list, chunk_size=36):
    """
    take a list of dicts and separate after selected chunk size
    if last chunk is not having desired size, fill ''
    return list of lists of size 36 (chunk size)
    """

    # list divided to chunk_size
    chunked_list = []

    # data to be filled
    # missing_data = {'top_row':'', 'middle row':'', 'bottom_row':''}
    missing_data = {k: '' for k in unchunked_list[0]}

    # create chunked list
    for chunk in range(0, len(unchunked_list), chunk_size):
        chunked_list.append(unchunked_list[chunk: chunk + chunk_size])

    # empty data solution

    # number of missing entries in last list
    missing_entries = chunk_size - len(chunked_list[-1])

    # adding missing data to fill the last list to standard length
    chunked_list[-1].extend([missing_data] * missing_entries)

    return chunked_list


def enumerate_keys(pagelist):
    """
    take list of dicts and add number to each dict key
    return list of dicts
    """

    new_list = []

    for num, dct in enumerate(pagelist, start=1):
        new_dict = {}
        # for each key and value in dct
        for key, val in dct.items():
            # to key add '_num'
            dctkey = key + f'_{num}'
            # dctval = dctval + f'_{num}'
            # vlozim klic s hodnotou do new_dict
            new_dict[dctkey] = val
        # novej slovnik do new_list
        new_list.append(new_dict)
    return new_list

    # napis funkci, ktera zmerguje vsechny dicty oceilovane do jednoho velkeho dictu bez dodatecne struktury


def merge_dicts(chunk_list: list) -> dict:
    """
    :param list:
    """
    return {'merge': True}
