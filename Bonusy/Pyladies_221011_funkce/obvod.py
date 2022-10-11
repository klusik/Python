""" Obvod kruhu """

from math import pi

def obvod(polomer):
    return 2 * pi * polomer

polomer = int(input("Zafdej polomer: "))

print("Obvod je ", obvod(polomer))