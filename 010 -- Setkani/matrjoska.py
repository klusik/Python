# Cilem je zadat pocet vrstev, pokud se zada "0," máme hotovo, panenka neni 
# obalena vrstvami kolem. Pokud se zada 1, panenka je obalena jednim spodkem a jednim vrskem. Atd.




# Zadani poctu vrstev
layerCount = 0
while True:
    layerCount = int(input("Kolik vrstev? ( n > 0 ): n = "))
    if layerCount < 0: continue
    break

print(f"Zadáno {layerCount} vrstev.")

def matrjoska(localLayerCount):
    pass
    if localLayerCount > 0:
        print(f"{localLayerCount} | ")
        matrjoska(localLayerCount-1)
    else:
        print(" PANENKA ")

    if localLayerCount > 0: 
        print(f" | {localLayerCount}")

matrjoska(layerCount)

