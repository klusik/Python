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
def gather_data():
    '''Take input from user'''
    name = input('Zadejte jmeno: ')
    form = input('Zadejte formu: ')
    unit = input('Zadejte jednotky: ')
    qty = int(input('zadejte pocet: '))
    total_price = float(input('zadejte celkovou cenu: '))

    return name, form, unit, qty, total_price

def user_input():
    '''Call gather_data and save data in form of list of dicts.
    
    INPUT
    gather_data()

    OUTPUT
    list_of_dicts
    '''
    list_of_dicts = []

    while True:
        cont = input('prejete si zadavat? a/n: ')

        if (cont == 'a') or (cont == 'A'):
            
            name, form, unit, qty, total_price = gather_data()
            mydict = {
                'name'          : name,
                'form'          : form,
                'units'         : unit,
                'qty'           : qty,
                'total_price'   : total_price 
            }
            list_of_dicts.append(mydict)
            continue
        elif (cont == 'n') or (cont == 'N'):
            break
        else:
            print('Neplatne zadani, konec')
            continue
    return list_of_dicts

#print(user_input())
