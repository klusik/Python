text1 = """Dost pravděpodobně. Ono řízení v tutěch soutěžích je poměrně dost technický, jde „jen“ o to, udržet se těsně před hranicí fyzikálních možností (kluzu apod.) Což technika dokáže odhadnout/změřit poměrně dobře. Reálný provoz ve městě je IMO mnohem větší divočina"""

text2 = """Ono dost záleží .. třeba AI projektů pro Trackmanii je docela dost a výsledky jsou hodně solidní. U těch her/simulátorů je problém v tom, že výsledky jsou deterministické, tj. opakovatelné napříč stejnými vstupními parametry. V reálu je to jiná kapitola, protože těch vstupních parametrů je nespočeně více a reprodukovatelnost výsledků je prakticky nereálná (např. díky nemožnosti mít dvě přesně stejně ojetá vozidla).
AI jako takové často pracuje nikoliv s ideálním modelem, ale eliminací nevhodných výsledků, což je (aktuálně) v reálném čase dost problematické. Vzhledem k pokroku ve výkonech HW bych si troufl odhadnout, že do toho roku 2032 by AI mělo zvládnout skutečnou jízdu Rally, ve čtvrtině případů se umístit v top 10 a v polovině v přední polovjně výsledkové listiny. U F1 by to mohlo vypadat asi celkem podobně. Na jednu stranu dráha je hodně determistická, na druhou ale jsou tu ostatní auta. Ale to už by měla AI zvládat dneska. Problém pořád je, že zrovna u řízení spousta závodníků zmiňuje, že řídí "zadkem", čili pokud je posadí k simulátoru, většinou nejsou schopni reprodukovat výsledky."""

text1_list = text1.split()
text2_list = text2.split()

output_text = ""

# alternate words
for index, word in enumerate(text2_list):
    if index >= len(text1_list):
        output_text += f"{word} "
    else:
        output_text += f"{word} {text1_list[index]} "
        
print(f"Sloučený text: {output_text}")

# eliminate every second letter
output_text_alternated = ""
for index, letter in enumerate(output_text):
    output_text_alternated += letter if index%2 else ""
print(f"Alternovaný text: {output_text_alternated}")