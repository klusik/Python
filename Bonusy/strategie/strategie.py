cache = {20: (2.0, "žádné"), 19: (1.0, "žádné"), 18: (0.5, "žádné")}

def expected_value(n: int) -> float:
    if n > 20:
        return 0.0
    elif n in cache:
        return cache[n][0]
    else:
        tlacitko_4_7 = sum(expected_value(n+i) for i in range(4,8)) / 4
        tlacitko_1_8 = sum(expected_value(n+i) for i in range(1,9)) / 8
        cache[n] = (max(tlacitko_4_7, tlacitko_1_8), "4-7" if tlacitko_4_7 > tlacitko_1_8 else "1-8")
        return cache[n][0]

print(expected_value(0))
for n in range(0, 20):
    print(f"Když máš {n}, zmáčkni tlačítko {cache[n][1]}.")