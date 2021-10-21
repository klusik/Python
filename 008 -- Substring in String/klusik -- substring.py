text = "Testujuparsing podle slov, treba podle slova parsing. Uvidime, jak si parsing poradi se slovem, kde je za parsing tecka, takze parsing."
btcString = "USDT1.8384"

dlouhyRetezec = """USDT1.741
28.3434 SXP / 34.3434 USDT
FINISHED
USDT1.9
35.34 SXP / 43.344 USDT
FINISHED"""



textListSplit = text.split("parsing")

textListStrip = text.strip("Testuju")

# print(textListSplit)

# print(textListStrip)

# print(btcString.strip("USDT"))

dlouhyRetezecSplit = dlouhyRetezec.split("FINISHED")

print(dlouhyRetezecSplit)

print("Test {} ahoj a {} tak".format("Pepa", "Maruška"))