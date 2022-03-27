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

def file_handler():
    '''
    Read content of input file, calculate numbers of lines and characters,
    write results into result.txt file

    INPUT
    input_file_name -> system path, string

    OUTPUT
    output_file_name -> system path, string
    '''

    # parsing the file names
    input_file_name = r'C:\temp\python_repo\michal\PyLadies\05_files_and_strings\prvni.txt'
    output_file_name = r'C:\temp\python_repo\michal\PyLadies\05_files_and_strings\status.txt'
    
    # read content of input file
    with open(input_file_name, mode='r') as input_file:
        input_file_content = input_file.read()

    # declarations
    file_lines = 1
    file_chars = 0

    # clean the input_file_contet of whitespaces
    input_file_content_cleaned = input_file_content.strip()
    
    
    # cycle throug content of file and count lines and chars
    for character in input_file_content_cleaned:
        # find end of line
        if character == '\n':
            file_lines = file_lines + 1
            print(f'New line.')
        # raise counter for each character
        file_chars = file_chars + 1
        print(f'New char. total: {file_chars}')
    print(f"Total chars: {file_chars}, total line: {file_lines}")

    # write statistics data to output file
    with open(output_file_name, mode = 'w') as output_file:
        print(f'Total chars: {file_chars}, total lines: {file_lines}.', file=output_file)
        print('Statistics saved to output file.')

# RUNTIME
file_handler()
