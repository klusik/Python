import user_input
import calculation

def main():
    data = user_input.user_input()
    # print(data)
    calculated_data = calculation.calculate_unit_price(data)
    print(calculated_data)
if __name__ == '__main__':
    main()
