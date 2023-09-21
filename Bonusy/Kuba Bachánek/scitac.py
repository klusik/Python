veta = (input("Zadej větu: "))

#seznam souhlásek, samohlásek a interpunkčních znamének, z něhož bude program rozpoznávat
souhlasky = "bcčdďfghjklmnňpqrřsštťvwzž"
samohlasky = "aeiouyáéěíóúů"
interpunkce = ".,!?"

#výstupní hodnota znamének
pocet_samohlasky = 0
pocet_souhlasky = 0
pocet_interpunkce = 0

#blok příkazů na zjištění konkretních počtů
for pismeno in veta:
    if pismeno.lower() in samohlasky:
        pocet_samohlasky += 1
    elif pismeno.lower() in souhlasky:
        pocet_souhlasky += 1
    elif pismeno.lower() in interpunkce:
        pocet_interpunkce += 1

#příkaz ke zjištění počtu slov ve větě.
slova = veta.split()
pocet_slov = len(slova)

print(f"Věta obsahuje: \n{pocet_slov} slov \n{pocet_souhlasky} souhlásek \n{pocet_samohlasky} samohlásek "
      f"\n{pocet_interpunkce} interpunkčních znamének")