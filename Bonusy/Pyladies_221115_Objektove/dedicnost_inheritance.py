"""
    Ukazkovy kód na dědičnost
"""


# CLASSES #
class Vehicle:
    weight = 1500
    height = 150
    length = 430
    wheels = 4
    fuel_capacity = 60


class Diesel:
    fuel = "Diesel"


class Gasoline:
    fuel = "Gasoline"


class GasolineCar(Vehicle, Gasoline):
    pass


class DieselCar(Vehicle, Diesel):
    pass


class Motorbike(Vehicle, Gasoline):
    wheels = 2


class Bicycle(Vehicle):
    wheels = 2
    fuel = None


# OBJECTS #
ford_mondeo = GasolineCar()
wv_transporter = DieselCar()
babeta = Motorbike()
author_21 = Bicycle()

# PRINTS #
print(f"My Ford has a {ford_mondeo.fuel} as a fuel.")
print(f"Neighbourgh's Transporter has {wv_transporter.fuel} as a fuel")
print(f"My bike has {babeta.wheels} wheels.")
