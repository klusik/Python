# zelva, python modul (velmi popisny nazev..)
import turtle
'''
turtle.forward(50) # opens window with right arrow of size 50
turtle.shape("turtle")
turtle.left(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)

turtle.exitonclick()

# the same using a cycle
for j in range(3):

    for i in range(20):
        i = i + 100
        turtle.forward(i)
        turtle.penup() # od ted zelva nekresli
        turtle.forward(i/2)
        turtle.pendown() # od ted zelva kresli
        turtle.forward(i)
        turtle.left(90)
    turtle.left(20)
turtle.exitonclick()

# nasleduje while zyklus
usr_input = input("rekni A")
while usr_input != "A":
    print("zkus to znovu")
    usr_input = input("rekni A")
'''
# naprogramujeme si hru "oko bere"

'''
zacinas s 0 body
pocitac v kazdem kole vypise, kolik mas bodu a zepta se, jestli chces pokracovat
pokud odpovis ne, hra konci
pokud odpovis ano, pocitat "otoci kartu" = hadone vybere cislo
    od 2 do 10, vypise jej a pricte k bodum
pokud mas vice nez 21 bodu, prohravas
cilem hry je ziskat co nejvice bodu, idelane 21 (priblizit se co nejvice k 21)
'''
# IMPORTS
import random

score = 0
while True:
    print(f"your score is {score}.")
    cont = input("Do you want to continue? y/n: ")
    if cont == "y":
        card = random.randrange(2,10)
        print(f"You received {card} card.")
        score = score + card
        print(f"Now your score is {score}.")
    else:
        print(f"You ended the game with score {score}")
        break
    if score == 21:
        print("You are victorious")
        break
    elif score > 21:
        print("You lost your game")
        break
