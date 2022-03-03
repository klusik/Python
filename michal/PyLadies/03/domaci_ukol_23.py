# Nakresli pětiúhelník, šestiúhelník, sedmiúhelník, osmiúhelník.
# Aby byly tvary zhruba stejně veliké, použij pro n-úhelník délku strany např. 200/n

import turtle
# petiuhlenik
for i in range(5):
    turtle.forward(500/5)
    turtle.left(360/5)
turtle.exitonclick()

# sestiuhelnik
for i in range(6):
    turtle.forward(500/6)
    turtle.left(360/6)
turtle.exitonclick()

# sedmiuhlenik
for i in range(7):
    turtle.forward(500/7)
    turtle.left(360/7)
turtle.exitonclick()

# osmiuhlenik
for i in range(8):
    turtle.forward(500/8)
    turtle.left(360/8)
turtle.exitonclick()