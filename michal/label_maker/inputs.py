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
def gather_data():
    '''Take input from user'''
    
    # name of product
    name = input('Zadejte jmeno: ')
    
    # code of form (btt, etc.)
    form = input('Zadejte formu: ')
    
    # units in which product is measured (ml, piece, etc.)
    unit = input('Zadejte jednotky: ')

    # quantity of product in package
    qty = int(input('zadejte pocet: '))

    # price per package
    total_price = float(input('zadejte celkovou cenu: '))

    return name, form, unit, qty, total_price

def user_input():
    '''Call gather_data and save data in form of list of dicts.
    
    INPUT
    gather_data()

    OUTPUT
    list_of_dicts
    '''

    # output data format
    list_of_dicts = []

    while True:
        # flag for next entry
        cont = input('prejete si zadavat? a/n: ')

        # next entry
        if (cont == 'a') or (cont == 'A'):
            
            name, form, unit, qty, total_price = gather_data()
            mydict = {
                'name'          : name,
                'form'          : form,
                'units'         : unit,
                'qty'           : qty,
                'total_price'   : total_price 
            }

            # add dict with product to output data list
            list_of_dicts.append(mydict)
            continue

        # entry finished
        elif (cont == 'n') or (cont == 'N'):
            break

        # invalid input
        else:
            print('Neplatne zadani, konec')
            continue
    
    return list_of_dicts

# print(user_input())
