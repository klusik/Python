""" try except """
a = 1
b = 0

# Try except
try:
    print(f"Podíl dvou čísel {a} / {b} = {a / b}")
    
except ZeroDivisionError:
    print("Neděl nulou!")
    raise
    
except TypeError:
    print("Zkoušíš dělit řetězce, jo?")
    
print("A toto je konec.")
