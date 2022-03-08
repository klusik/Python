# Napiš program, který postupně načte od uživatele dvě čísla a jednoznakový řetězec – buď '+', '-', '*' nebo '/'. Program provede na číslech příslušnou operaci.
# more advanced stuff

# imports
import operator

# dict with all available operators
operator = {
  "+": operator.add,
  "-": operator.sub,
  "*": operator.mul,
  "/": operator.truediv
}

a = float(input("zadejte prvni cislo:"))
b = float(input("zadejte druhe cislo:"))
usr_def_operator = (input("zadejte operator:"))

result = operator[usr_def_operator](a,b)

print(result)



