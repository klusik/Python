'''
Práce se soubory. Připrav si 2 krátké textové soubory s několika
řádky (např. prvni.txt a druhy.txt)
4.

Napiš program, který vypíše obsah souboru prvni.txt na obrazovku.
'''

with open(r'C:\temp\python_repo\michal\PyLadies\05_files_and_strings\prvni.txt', mode='r') as file:
    file_content = file.read()
    print(file_content)