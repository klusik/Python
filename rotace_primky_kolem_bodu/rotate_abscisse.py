""" Test of import a module """

# IMPORTS #
import geometry

# RUNTIME #
def main():
    """ Main function """
    abscisse = abscisses.Abscisse(point_1=(1,1), point_2=(3,3))

    print(abscisse.get_length())
if __name__ == "__main__":
    main()
