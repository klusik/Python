'''
Napiš program, který ze souboru prvni.txt určí:
počet řádků v souboru, 
počet znaků v souboru. 
Tyto hodnoty zapiš do nového souboru. 
Při počítání znaků v souboru nezapoměň vynechat tzv. bílé znaky,
abys dostala správný počet písmen, číslic a případně speciálních znaků,
které jsou v souboru. 
Ujisti se také, že jsi správně spočítala počet řádků 
(že např. výsledný počet není o 1 menší než skutečný počet řádků v souboru).
'''

from os import openpty


def file_handler(input_file_name, output_file_name):
    '''
    Read content of input file, calculate numbers of lines and characters,
    write results into result.txt file

    INPUT
    input_file_name -> system path, string

    OUTPUT
    output_file_name -> system path, string
    '''

    # parsing the file names
    input_file_name = f'C:\temp\python_repo\michal\PyLadies\05_files_and_strings\{input_file_name}'
    output_file_name = f'C:\temp\python_repo\michal\PyLadies\05_files_and_strings\{output_file_name}'
    with open(r'input_file_name', mode='r') as input_file:
        input_file_content = input_file.read()

    file_lines = 0
    
    # clean the input_file_contet of whitespaces
    input_file_content_cleaned = input_file_content.replace(' ', '')
    file_chars = 0

    for character in input_file_content_cleaned:
        if character == '\n':
            file_lines = file_lines + 1
        file_chars = file_chars + 1

    with open(output_file_name, mode = 'w') as output_file
        