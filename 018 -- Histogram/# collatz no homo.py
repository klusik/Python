# collatz no homo

class Kolac:
    def __init__(self, number) -> None:
        self.number = number
        self.lst = []

    def magic (self):
        while True:
            if self.number <= 1:
                return self.lst
            else:
                if self.number%2 == 0:
                    self.lst.append(self.number/2)
                else:
                    return self.number * 3 + 1
kolac = Kolac(100)
print(kolac.magic())


