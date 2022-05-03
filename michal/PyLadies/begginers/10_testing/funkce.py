def pocitam_znaky(text, znak, index):
    if not 0 < index < len(text):
        raise IndexError
    # NOTE: pozor na jednicky
    return text[index + 1 :  ].count(znak)
