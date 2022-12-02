# zalozeni dictu
vozovy_park = {
    # key : value
    'znacka':['ford', 'skoda'],
    'motor':['ctyrvalec', 'trivalec'],
    'kastle':['kombi', 'hot hatch']
}

print(vozovy_park)

# ukazk
# pridani key:value paru do existujiciho dictu
#           novy key    nove values
vozovy_park['kola'] = ['15"', '14"']

# pridani nove polozky
vozovy_park['znacka'].append('mustang')
print(vozovy_park)
# it = vozovy_park.
#print(it)

l = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

print(l)

print(l[1][1])

vozovy_park.pop('motor')
print(vozovy_park)