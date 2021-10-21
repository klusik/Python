from typing import no_type_check_decorator


def matrydshka(n):
    if n==0:
        print("panenka")
    else:
        print(n)
        matrydshka(n-1)
        print(n)
    
matrydshka(7)

