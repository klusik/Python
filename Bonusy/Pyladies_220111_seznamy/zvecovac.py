text = "ahoj, tohle je všechno malými"

for znak in range(len(text)):
    print(f"{text[0:znak]}{text[znak].upper()}{text[znak + 1:]}")