'''
Nakonec souboru prvni.txt přidej obsah souboru druhy.txt.
'''

def add():
    '''
    Read content of file prvni.txt, append it to end of file druhy.txt.

    INPUT
    input_file - system path, string

    OUTPUT
    output_file - system path, string
    '''
    in_file = r'C:\temp\python_repo\michal\PyLadies\05_files_and_strings\prvni.txt'
    out_file = r'C:\temp\python_repo\michal\PyLadies\05_files_and_strings\druhy.txt'
    # read
    with open(in_file, mode='r') as input_file:
        in_file_content = input_file.read()
        print('content of the file stored in the memory')
    
    # save
    with open(out_file, mode='a') as output_file:
        # add new line at the end of the file
        print(file=output_file)
        print(in_file_content, file=output_file)
        print('saved')

add()
