
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
    # data is list of dicts
    data = inputs.csv_input_hardwork()
    print('all available data:', data, '\n')
    # calculated data is dict like data with added unit price 
    calculated_data = calculation.calculate_unit_price(data)
    print('calculated data is data with added unit price: ', calculated_data, '\n')
    print('dict formated to top_row, middle_row and bottom_row: ', calculation.prepare_output_dic(calculated_data[0]),'\n')
    print('prepare_output_list() returns list of formated dicts: ', calculation.prepare_output_list(calculated_data),'\n')
    print('list splitted to formated pages: ', calculation.split_to_pages(calculation.prepare_output_list(calculated_data)), '\n')
    #outputs.to_console(calculated_data)

    listSplittedToPages = calculation.split_to_pages(calculation.prepare_output_list(calculated_data))
    #print(listSplittedToPages)

    # testdata is list of dicts
    testdata = calculation.prepare_output_list(calculated_data)
    print('testdata: ', testdata, '\n')

    outputdata = []
    #print(calculation.enumerate_keys(testdata))
    for i in listSplittedToPages:

        outputdata.append(calculation.enumerate_keys(i))

    

    print('ocislovany list', outputdata)


    #print(outputdata)
if __name__ == '__main__':
    main()
