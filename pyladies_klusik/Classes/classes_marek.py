class Kotatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def zamnoukej(self):
        print("Mňau!")


kocky = ['Mourek', 'Micka', 'PanKoťátko', 'Kusaj', 'Udaj', 'Mourek', 'Mourek']

kocky_jedinecne = []
for kocka in kocky:
    kocka_objekt = Kotatko(kocka)
    kocky_jedinecne.append(kocka_objekt)


print(kocky_jedinecne[0].jmeno)

