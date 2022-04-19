class Kotatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def zamnoukej(self):
        print("Mňau!")


kocky = ['Mourek', 'Micka', 'PanKoťátko', 'Kusaj', 'Udaj', 'Mourek', 'Mourek']

kocky_jedinecne = []
for kocka in kocky:
    if kocka not in kocky_jedinecne:
        kocky_jedinecne.append(kocka)

kocky_objekty = []
for kocka in kocky_jedinecne:
    kocka_objekt = Kotatko(kocka)
    kocky_objekty.append(kocka_objekt)


for kocka in kocky_objekty:
    print(kocka.jmeno)

