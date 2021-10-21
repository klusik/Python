# Pokus o dict

dLidiNaMatematickemPatku = {"Tomas": 40, "Rudolf": 37, "Michal":38, "Lukas":25, "Adam":18, "Ivos":24, "Mirousek":37}

print(dLidiNaMatematickemPatku)

print("Tomas" in dLidiNaMatematickemPatku)

print(dLidiNaMatematickemPatku["Ivos"])

for lidi in dLidiNaMatematickemPatku:
    print(lidi + ": " + str(dLidiNaMatematickemPatku[lidi]))


from enum import Enum 

class lidi(Enum):
    TOMAS = 1
    MICHAL = 2
    RUDOLF = 3

print(repr(lidi.TOMAS))