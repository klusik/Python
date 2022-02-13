import random
l = [random.randint(0,3) for i in range(10)]
 
 
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]
 
print(l)
l_new = remove_values_from_list(l, 0)
print(l_new)
 
dif = len(l) - len(l_new)
 
print(dif)
 
for i in range (0,dif):
    l_new.append(0)
 
print(l_new)