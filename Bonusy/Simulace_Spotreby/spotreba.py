"""
    How to simulate a car (it's consumption)

    I don't know what to do more :-D
"""
'''
---=========================================================================---
LOG
24.4.2022 22:03 Michal Sykora: 
Initial idea behind this task is a conversation I had coulple years ago with
experienced car service technician on topic of fuel consumption during
acceleration. 

Technician tried to convince me, that less fuel is burned when full throttle
is applied thus reducing time needed for reaching desired velocity. Proof:
it's obvious, innit?

I opposed, that even if the time needed for acceleration is doubled, fuel
savings will be greater when throttle is open for limited fuelflow (let's say
50%).

The ultimate goal of this program is to prepare simple simulation of fuel
consumption during acceleration to some speed, providing comparable and 
human readable data of each acceleration method.

Luckily enough, I have simple OBD-II device at my disposal now, so that some
parameters can be defined based on observation.

Problem decomposition
---------------------
Goal is to determine amount of fuel needed to reach user specified speed.

Example:
--------
Run100 - When throttle is 100% open, desired speed is reached in N seconds
        consuming M litres of fuel
Run25 - When throttle is 25% open, desired speed is reached in N seconds
        consuming M litres of fuel

As the level of openess of throttle is not possible to measure exactly in 
real life conditions, I suggest scenarios with 10%, 25%, 50%, 75% and 100%
of fuelflow.

Constants
---------
Based on OBD-II observations on my Ford Focus II 1.6l 74kW car, following
was recorded (full throttle = 100l/100km):

Throttle position   |   fuel consumtion [l/100km]   |   acceleration 0-100km/h [s]
10%                 |   100 * 0.1 = 10              |   12 * 10 = 120**
25%                 |   100 * 0.25 = 25             |   12 * 3 = 36**
50%                 |   100 * 0.5 = 50              |   12 * 2 = 24**
75%                 |   100 * 0.75 = 75             |   12 * 1.5 = 18**
100%                |   100***                      |   12*

* based on manufacturer data
** derived from manufacturer data
*** observed

Above table is oversimplification of the real life conditions, e.g. acceleration
is not linear (not same task to accel to 100km/h and 200km/h), environment is
omitted, etc. In case of interest, more detailed characteristics can be
added in future versions.

fuel_consumed_accel = fuel_consumption / distance_traveled 

To be able to determine fuel consumption during acceleration, traveled length
must be known. Not sure, how to do that. 
---=========================================================================---
'''
# CLASSES #
class Car:
    def __init__(self,
                 valves = 4,
                 ventiles = 16,
                 ):
        self.valves = valves
        self.ventiles = ventiles

    def magic(self) -> bool:
        return True


# RUNTIME #
def main():
    car = Car()


if __name__ == "__main__":
    main()
