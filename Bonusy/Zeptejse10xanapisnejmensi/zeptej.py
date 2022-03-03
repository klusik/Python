if __name__ == "__main__":
    minimum = 0
    for order in range(10):
        cislo = int(input("Napis cislo: "))
        if order:
            if cislo < minimum:
                minimum = cislo
        else:
            minimum = cislo

    print(f"Minimalni cislo je {minimum} :-)")