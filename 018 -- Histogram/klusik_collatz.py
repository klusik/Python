"""Collatz conjecture with python objects"""

class Numbers:

    def getLast(self):
        return self.allNumbers[-1]

    def isNotOne(self):
        if self.allNumbers[-1] != 1:
            return True
        else:
            return False

    def isEven(self, testedValue):
        if testedValue % 2 == 0:
            return True
        else:
            return False

    def add(self, addedValue):
        self.allNumbers.append(int(addedValue))

    def avg(self):
        avg = sum(self.allNumbers)/len(self.allNumbers)
        return avg

    def view(self):
        print(f"Value: {self.inputValue}")
        for value in self.allNumbers:
            print(value, end = ' ')
        print('')

        print(f"Average value: {self.avg()}")
        print(f"{self.numOfOddsEvens()['odds']} odds and {self.numOfOddsEvens()['evens']} evens.")

        print('-'*60)

    def numOfOddsEvens(self):
        odds = 0
        evens = 0

        for value in self.allNumbers:
            if self.isEven(value):
                evens += 1
            else:
                odds += 1

        return {"odds": odds, "evens": evens}


    def __init__(self, inputValue):
        self.inputValue = inputValue
        self.allNumbers = list()

        if not str(self.inputValue).isnumeric():
            print(f"{self.inputValue} is not a number!")
            return False
        elif self.inputValue < 1:
            print(f"{self.inputValue} is not greater or equal 1")
            return False

        self.allNumbers.append(inputValue)

        while self.isNotOne():
            if self.isEven(self.getLast()):
                self.add(self.getLast()/2)
            else:
                self.add(3 * self.getLast() + 1)


def main():
    # list of numbers
    numbers = list()
    for number in range(2,101):
        numbers.append(Numbers(number))

    for number in numbers:
        number.view()




if __name__ == "__main__":
    main()