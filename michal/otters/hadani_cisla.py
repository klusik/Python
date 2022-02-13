#program na hadani spravneho cisla
uhodnuto = False
hadane = 100 *7-2+5+2+2-1
def h(vase):
    while True:
        if hadane == vase:
            print ('uhadnuto')
            break
        elif hadane < vase:
            print ('to je moc')
            break
        elif hadane > vase:
            print ('to je malo')
            break