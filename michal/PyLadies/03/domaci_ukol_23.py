# Nakresli pětiúhelník, šestiúhelník, sedmiúhelník, osmiúhelník.
# Aby byly tvary zhruba stejně veliké, použij pro n-úhelník délku strany např. 200/n

import turtle
maja_path = r"C:\Users\Z0001932\OneDrive - ZF Friedrichshafen AG\prace\python\projects\streda\python_git\michal\PyLadies\03\maja.gif"
turtle.register_shape(maja_path)
turtle.shape(maja_path)
turtle.resizemode("user")
turtle.shapesize(0.2, 0.2, 1)
for n in range(5,9):
    # petiuhlenik
    for i in range(n):
        turtle.forward(500/n)
        turtle.left(360/n)
    turtle.penup()
    turtle.forward(100)
    turtle.pendown()
turtle.exitonclick()

