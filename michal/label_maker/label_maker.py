# order of imports must be as follows due to logging
import logging

import config

config.setup_logging()

import inputs
import calculation
import outputs

log = logging.getLogger(__name__)


# import outputs

def main():
    log.info('Start program')

    # GET DATA FROM CSV FILE, RETURN LIST OF DICTS
    # data = inputs.csv_input()
    # data is list of dicts
    data = inputs.csv_input_hardwork()
    #print('all available data:', data, '\n')

    # FROM DATA CREATE LIST OF DICTs INCLUDING UNIT PRICE
    # calculated data is dict like data with added unit price 
    calculated_data = calculation.calculate_unit_price(data)
    #print('calculated data is data with added unit price: ', calculated_data, '\n')

    # REFORMAT CALCULATED_DATA DICT TO OUTPUT DICT CONTAINING KEYS TOP_ROW, MIDDLE_ROW AND BOTTOM_ROW
    rows_dict = calculation.prepare_output_dic(calculated_data[0])
    #print(f'single dict formatted to top-middle-bottom_row scheme: {rows_dict=}', '\n')

    # CREATE LIST OF OUTPUT DICTS
    list_of_row_dicts = calculation.prepare_output_list(calculated_data)
    #print(f'list of "row" dicts: {list_of_row_dicts=}', '\n')

    # SPLIT LIST OF DICTS TO PAGES CONTAINING 36 ITEMS TOPS
    paginated_list_of_row_dicts = calculation.split_to_pages(list_of_row_dicts)
    #print(f'list splitted to formatted pages: {paginated_list_of_row_dicts=}', '\n')
    # outputs.to_console(calculated_data)

    # ADD LINE NUMBERS TO DICT KEYS
    # MERGE DICTS TO ONE DICT
    for page_num, page_data in enumerate(paginated_list_of_row_dicts, start=1):
        #print(f'preparing page {page_num=}')
        # add line number
        enumerated = calculation.enumerate_keys(page_data)

        # merge dicts to one dict
        merged_dict = calculation.merge_dicts(enumerated)
        #print(f'{merged_dict=}')
        # nacti template a nahrad v nem pomoci merged dict

    # ==================================================================================================================
    #                                                   OUTPUT
    # ==================================================================================================================
    path_to_word_file = r'C:\UserData\git_ws\myOnlyRealPrivateRepo\michal\label_maker\templates\labels_template.docx'
    data_to_word = outputs.to_word(calculated_data, path_to_word_file)
    print(data_to_word)


    log.info('program end'.center(80, '-'))

if __name__ == '__main__':
    main()
