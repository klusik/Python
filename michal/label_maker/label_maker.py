import inputs
import calculations

def main():
    # gather data from user, data = list of dicts
    data = inputs.user_input()

    # calculate unit price, add to dict
    for product in data:
        product_price = product['total_price']
        qty_of_units = product['qty']
        unit_price = calculations.UnitPrice(product_price, qty_of_units)
        product['unit_price'] = unit_price

    # prepare output data

    # print(data)

if __name__ == '__main__':
    main()