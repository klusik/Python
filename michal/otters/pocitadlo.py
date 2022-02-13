def countWord(path, word):
    print('zadana cesta k souboru ', path, ' a hledane slovo ', word)

    f = open(path, 'r')

    wordCount = 0

    while True:
        # nacteni radku
        radek = f.readline()
        if radek == '':  # end of file
            break

        new_radek = radek
        counter = 0

        # Prohledavam radek pro hledane slovo
        while True:
            # prohledavam zbytek radku, zda se slovo znovu nevyskytuje
            index = new_radek.find(word)

            # opakuji do konce radku
            if (index == -1):
                break

            # kdyz ho najdu, tak
            # a) zvysim hodntu pocitadla
            counter += 1

            # b) vytvorim novy radek, ktery umaze vse do konce hledaneho slova
            new_radek = new_radek[index + len(word):]

        wordCount = wordCount + counter

    # uzavru soubor        
    f.close()

    print('slovo ', word, 'se v souboru vyskytuje ', wordCount, ' krat')
    return wordCount


countWord('C:\Users\Z0001932\Desktop\pika.txt', 'Snorlax')
