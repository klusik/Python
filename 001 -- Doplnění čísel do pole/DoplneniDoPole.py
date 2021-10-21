#cisteni

# Hello world
print("Hello World.")

# Spojeni stringů

s1 = "Ahoj"
s2 = "Michale"

spojeni = s1 + " " + s2

print(s1+" "+s2)
print(spojeni)

delsi = ''' as-d,.f as fjasdůl fjsdůlj fasůlfj s fjasůlkdfj asůljweoicneů jd f
asdfkl jasůdlfk jasůldkfj 
asůd fkljsůfkl jasůdl j
'''

print(delsi)

text = "blabla "
print(text*3)

vek = 37
text = f"Muj vek je {vek}"

print(text)

for i in text:
    if i == 'e':
        print(f"Znak '{i}' je znak 'e'")
    else:
        print(f"Znak '{i}' neni znak 'e'")

print(text[4])

#slicing
print(delsi[3:-2])
print(text[5:-2])

print(len(text))

x=6

print(delsi[::])


#můj cílový program
# dokud není zadaná nula, jedu dál.


while True:
    hodnota = int(input("Zadej text: "))
    if hodnota == 0:
        print("Jop, je to nula.")
        break

hodnota = 2
while hodnota!=0:
    hodnota = int(input("Zadej cislo: "))

print("Je to nula.")
