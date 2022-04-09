"""
coding challenge

máš zadané kladné celé n

najdi všechna taková a, b, c, že a+b+c = n (s tím, že např. trojice 1, 3, 8 je jiná než 3, 1, 8)

Udělej to v O(n^2)
"""

# RUNTIME #
def main():
    try:
        input_number = int(input("Enter the whole positive number: "))
        if input_number <= 0:
            raise(ValueError)
    except ValueError:
        print("Bad format of number.")

    

if __name__ == "__main__":
    main()