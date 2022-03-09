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

"""
PHP 

$sql_query = "SELECT * FROM table";

$db_data = mysqli_query($sql_query);

while($row = mysqli_fetch_array($db_data)) {
...
}

for ($i=0, $i<10, $i++) {
}

foreach $radek in $veci {
...
}

C 
for (i=0; i<10; udelej() {
...
}
"""

