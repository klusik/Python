'''calculations.py

module calculates unit price of the product
'''
# IMPORTS
import inputs

def UnitPrice(product_price, qty_of_units_in_package):
    '''
    Calculate unit price of the product

    INPUTS
    product_price - price of package of the product, float
    qty_of_units_in_package - number of units in product package, integer

    OUTPUT
    
    '''

    unit_price = product_price / qty_of_units_in_package
