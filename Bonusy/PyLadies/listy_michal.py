import pprint

lst = ["ahoj", "michale", "omg"]

print("ahoj" in lst)

new_lst = lst

print(id(lst), id(new_lst))

slv = {'a': 1, 'b': 1}
# slv.pop('a')

pprint.pprint(slv, indent=2)