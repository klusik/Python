# Pokusy s OOP

class Animals:
    _hairy = True
    _age = 10

    def __init__(self, _hairy, _age):
        self._hairy = _hairy
        self._age = _age
        

    def setHairy(self, _hairy):
        self._hairy = _hairy

    def getHairy(self):
        return self._hairy

    def setAge(self, _age):
        self._age = _age

    def getAge(self):
        return self._age


pes = Animals(True, 5)

print(str(pes.getHairy())+" "+str(pes.getAge()))

pes.setHairy(False)

print(str(pes.getHairy())+" "+str(pes.getAge()))

pes.setAge(10)

print(str(pes.getHairy())+" "+str(pes.getAge()))
