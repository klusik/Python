from graphics import *

def main():
    win = GraphWin('Face', 200, 150) # give title and dimensions

    A = Rectangle(Point(100,100), Point(150,150))
    A.draw(win)

    win.getMouse()
    A.undraw()
    win.getMouse()


main()
