import pathlib
import docxtpl
import calculation
import logging

# CONSTANTS 
WORD_OUTPUT_NAME = 'generated_labels'
OUTPUT_FOLDER = 'output'


def to_word(data, template):
    """Output the label data to word files.
    :param: data: input, dictionary
    :param: template: output, file ready to print
    """

    print('exporting to word')

    # reformat the dicts for replace
    data = calculation.prepare_output_list(data)

    # prepare paginated data
    page_splitted_data = calculation.split_to_pages(data)

    # for each page
    for page_num, page_data in enumerate(page_splitted_data, start=1):
        # open new template for each page
        doc = docxtpl.DocxTemplate(template)

        # prepare numbers for replacing
        replace_ready = calculation.enumerate_keys(page_data)
        merged_dict = calculation.merge_dicts(replace_ready)

        doc.render(context=merged_dict)

        # save to new file
        filename = f'{page_num:02}_{WORD_OUTPUT_NAME}.docx'
        logging.debug(f'saving to file {filename}')
        doc.save(pathlib.Path(OUTPUT_FOLDER) / filename)

    logging.info('output to word finished')