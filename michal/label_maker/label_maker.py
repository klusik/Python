# order of imports must be as follows due to logging
import logging

import config

config.setup_logging()

import inputs
import calculation

log = logging.getLogger(__name__)


# import outputs

def main():
    log.info('Start program')

    # GET DATA FROM CSV FILE
    # data = inputs.csv_input()
    # data is list of dicts
    data = inputs.csv_input_hardwork()
    print('all available data:', data, '\n')

    # FROM DATA CREATE DICT INCLUDING UNIT PRICE
    # calculated data is dict like data with added unit price 
    calculated_data = calculation.calculate_unit_price(data)

    print('calculated data is data with added unit price: ', calculated_data, '\n')

    # REFORMAT CALCULATED_DATA DICT TO OUTPUT DICT CONTAINING KEYS TOP_ROW, MIDDLE_ROW AND BOTTOM_ROW
    print('dict formatted to top-middle-bottom_row: ', calculation.prepare_output_dic(calculated_data[0]),
          '\n')

    # CREATE LIST OF OUTPUT DICTS
    print('prepare_output_list() = list of formatted dicts: ', calculation.prepare_output_list(calculated_data), '\n')

    # SPLIT LIST OF DICTS TO PAGES CONTAINING 36 ITEMS TOPS
    print('list split to formatted pages: ',
          calculation.split_to_pages(calculation.prepare_output_list(calculated_data)), '\n')
    # outputs.to_console(calculated_data)

    # SAVE OUTPUT DICT DIVIDED TO PAGES TO A LIST
    listSplittedToPages = calculation.split_to_pages(calculation.prepare_output_list(calculated_data))
    # print(listSplittedToPages)

    for page_num, page_data in enumerate(listSplittedToPages, start=1):
        print(f'preparing page {page_num}')
        enumerated = calculation.enumerate_keys(page_data)
        merged_dict = calculation.merge_dicts(enumerated)
        print(f'{merged_dict=}')
        # nacti template a nahrad v nem pomoci merged dict


if __name__ == '__main__':
    main()
