
# order of imports must be as follows due to logging
import logging
import config
config.setup_logging()

import inputs
import calculation

log = logging.getLogger(__name__)

#import outputs

def main():
    
    
    log.info('Start programu')

    #data = inputs.csv_input()
    data = inputs.csv_input_hardwork()
    print(data)
    calculated_data = calculation.calculate_unit_price(data)
    print(calculation.prepare_output_dic(calculated_data[0]))
    print('output list: ', calculation.prepare_output_list(calculated_data))
    #outputs.to_console(calculated_data)

if __name__ == '__main__':
    main()
