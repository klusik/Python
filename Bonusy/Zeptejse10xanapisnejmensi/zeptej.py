if __name__ == "__main__":
    minimum = 0
    for order in range(10):
        cislo = int(input("Napis cislo: "))
        if order:
            # not first
            if cislo < minimum:
                minimum = cislo
        else:
            # first
            minimum = cislo

    print(f"Minimalni cislo je {minimum} :-)")
