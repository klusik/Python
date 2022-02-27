'''
Výzva   Zkus napsat program, který ti poradí, co si vzít na sebe podle počasí (prší/je slunečno). Použij k tomu zanořené ify.

Program může vypadat následovně. Pokud venku prší, vem si kabát. Pokud prší a fouká k tomu, vem si větrovku a dlouhé kalhoty. Pokud svítí sluníčko, obleč si šaty/kraťasy. Pokud svítí slunce a k tomu fouká, vem si kabátek.

Kreativitě se meze nekladou. 
'''
# IMPORTS
import random

# weather definition
weather = ["hot", "sunny", "cloudy", "cold", 
           "rainy", "chilly" "snowy", "freezing"]

# generate weather conditions
weather_conditions = random.choice(weather)

if weather_conditions == "hot":
    print("Je hic. Nic si neberte a jdete na nudaplaz.")
elif weather_conditions == "sunny" or \
     weather_conditions == "cloudy":
     print("Je teplo, vezmete si kratky rukav.")
elif weather_conditions == "cold":
    print("Je chladneji. Vezmete si svetr")
elif weather_conditions == "rainy":
    print("Prsi, vezmete si neco nepromokaveho.")
elif weather_conditions == "chilly":
    print("Prituhlo, vezmete si neco tepleho")
elif weather_conditions == "snowy":
    print("Napadnul snih, vezmete si snehuly")
else:
    print("""
Mrzne az prasti, nelezte ven
a zapnete si plynove topeni 
dokud to jeste funguje...
""")

