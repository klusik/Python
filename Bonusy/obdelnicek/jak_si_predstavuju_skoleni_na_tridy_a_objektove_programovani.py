class Point:
    def __init__(self, x, y):
        print(f"Vytváří se objekt se souřadnicemi {x} a {y}.")
        self.x = x
        self.y = y

    def __repr__(self):
        pass

    def __str__(self):
        return("Ahoj")



point_x = 10
point_y = 20

list_of_points = [(10,20), (30,40)]

print(f"Soudarrnice jsou {point_x} a {point_y}.")

print(f"Souracnice všech bodů jsou {list_of_points}")

# co by se mi líbilo
bod_pocatek = Point(0, 0)

bod_kam_jdu = Point(10, 20)

print(bod_pocatek.x)

print(bod_pocatek)

