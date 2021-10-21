# zadani: https://www.codewars.com/kata/568018a64f35f0c613000054


import random

class Player:
    lives = 5

    def __init__(self, lives=5):
        self.lives = lives
        pass

    def loseLife(self):
        self.lives = self.lives - 1
        pass


print("Vitejte v nove hre!")

# new player
player = Player()

print(f"Vitej novy hraci, jako novy hrac mas {player.lives} zivotu.")

guessedNumber = random.randrange(1, 10)

while True:

    if player.lives == 0:
        print("Vycerpali jste zivoty, cus.")
        break
    
    while True:
        number = int(input("Zadej cislo, ktere si myslis, ze pocitac vybral (1--10): "))
        if number < 1 or number > 10:
            continue
        break

    if (number < guessedNumber):
        player.loseLife()
        print(f"Strilite moc nizko. Zbývá vám {player.lives} zivotu.")

    if (number > guessedNumber):
        player.loseLife()
        print(f"Strilite moc vysoko. Zbývá vám {player.lives} zivotu.")

    if (number == guessedNumber):
        print("Yes, trefa.")
        break


    
    
    