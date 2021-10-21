dAuta = {'skoda': 100,
         'ford': 120,
         }

print(dAuta['skoda'])
x = dAuta.get('ford')
print(x)
from enum import Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED)
print(repr(Color.RED))
type(Color.RED)


