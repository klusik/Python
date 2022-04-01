"""
Testing a set logics
"""
sets = list()
sets.append(set())
sets.append(set())

sets[0].add("svíčková")
sets[0].add("mléko")
sets[0].add("kakao")
sets[0].add("zmrzlina")
sets[0].add("voda")

sets[1].add("barák")
sets[1].add("slon")
sets[1].add("automobil")
sets[1].add("zf")
sets[1].add("voda")

print(f"Všechno: {sets}")

print(f"OR: {sets[0] | sets[1]}")

print(f"AND: {sets[0] & sets[1]}")

