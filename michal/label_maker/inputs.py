'''

Take input and return data in format of list of dicts

Example of output:

[
    {
        'name': 'Bromhexin',
        'form': 'gtt',
        'unit': 'ml'
        'quantity': 100
        'total_price': 194.0
    }
]
'''

import csv
import logging

log = logging.getLogger(__name__)

VALID_FORMS = ['gtt', 'sir', 'sol', 'pst', 'tbl', 'cps',
                'ung', 'crm', 'supp', 'spr', 'grg']
VALID_UNITS = ['g', 'ml', 'btc', 'sats',]
def positive_float(string):
    num = float(string)
    if not 0 < num < 10_000:
        raise ValueError('Smi byt jen od 0 do 9999')
    return num

def better_input(question, value_type, valid_options = None):
    '''
    Validate input based on the passed value type
    
    Upon error continously prompt user for correct answer
    '''
    while True:
        try:
            answer = value_type(input(f'{question} {valid_options if valid_options is not None else ""}: '))
            if valid_options and answer not in valid_options:
                raise ValueError('neni z povolenych hodnot')

            if question == 'Celkova cena [CZK]' and 0 < answer < 10_000:
                raise ValueError('Cena smi byt jen od 0 do 9999')

            if not answer:
                raise ValueError('Nepovolujeme prazdne hodnoty a nuly.')
        except:
            # vynadat
            print('nazadali jste spravny datovy typ')
        else:
            # vratit
            return answer
        finally:
            # trolling since 2022
            print('trolling since 2022')

def user_input():
    '''
    Take input from user.
    Example input:
        Nazev: Bromhexin
        Forma: gtt
        Jednotky: ml
    INPUT
    gather_data()

    OUTPUT
    list_of_dicts
    '''
    entries  = []

    while True:
            item = {
                'name'          : better_input('Nazev: ', str),
                'form'          : better_input('Forma: ', str, valid_options=VALID_FORMS),
                'units'         : better_input('Jednotky: ', str, valid_options=VALID_UNITS),
                'qty'           : better_input('Pocet: ', int),
                'total_price'   : better_input('Celkova cena [CZK]: ', positive_float) 
            }
            entries.append(item)

            next_q = input('-- dalsi? a/n: ')
            if next_q == 'n':
                return entries
def csv_input_hardwork():
    log.info('CSV input ACTIVATED')
    entries = []
    # open file readlines()
    with open(r'C:\UserData\git_ws\myOnlyRealPrivateRepo\michal\label_maker\resources\sample_data_csv', 'r') as csv_file:
        content = csv_file.readlines()
        # first line are keys for dict
        first_line = content.pop(0)
        # split first line to list of strings
        first_line = first_line.split(',')
        #print(first_line)
        # create dict with keys created from list of strings
        item = {
            first_line[0].replace('"',''): '', # name
            first_line[1].replace('"',''): '', # form
            first_line[2].replace('"',''): '', # units
            first_line[3].replace('"',''): '', # qty
            first_line[4].replace('\n', '').replace('"',''): '', # total price
        }
        # print(item)

        for line in content:
            line = line.split(',')    
            item['name'] = line[0].replace('"','')
            item['form'] = line[1].replace('"','')
            item['units'] = line[2].replace('"','')
            item['qty'] = int(line[3])
            item['total_price'] = int(line[4])
            entries.append(item)
                
    # last values are int() 
        return entries
#user_input()

def csv_input():
    log.info('CSV input ACTIVATED')
    
    with open(r'C:\UserData\git_ws\myOnlyRealPrivateRepo\michal\label_maker\resources\sample_data_csv', 'r') as file:
        reader = csv.DictReader(file, quoting=csv.QUOTE_NONNUMERIC)
        data = list(reader)
    return data