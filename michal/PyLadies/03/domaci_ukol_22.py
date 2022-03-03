'''Nakresli trojúhelník.
Poznámka: Rovnostranný trojúhelník má vnitřní úhly 60°. Želva se ale otáčí o vedlejší úhel 180 - 60 = 120°.'''
import turtle
for i in range(3):
    turtle.forward(50)
    turtle.left(120)
turtle.exitonclick()