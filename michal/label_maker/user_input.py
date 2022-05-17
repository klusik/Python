'''Inputs.py

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
def user_input():
    '''Take input from user'''
    name = input('Zadejte jmeno: ')
    form = input('Zadejte formu: ')
    unit = input('Zadejte jednotky: ')
    qty = input('zadejte pocet: ')
    total_price = input('zadejte celkovou cenu: ')

    return name, form, unit, qty, total_price

def create_d():
    name, form, unit, qty, total_price = user_input()
    mydict = {
        'name'          : name,
        'form'          : form,
        'units'         : unit,
        'qty'           : qty,
        'total_price'   : total_price 
    }

    list_of_dicts = []

    while True:
        cont = input('prejete si zadavat? a/n')

        if cont == 'a':
            list_of_dicts.append(mydict)
        elif cont == 'n':
            break
        else:
            print('Neplatne zadani, konec')
            break

create_d()