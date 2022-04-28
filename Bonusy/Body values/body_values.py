"""
    Body values

    For losing weight purposes
"""

# IMPORTS #
import easygui
import xml

# CLASSES #
class Body:
    """ Body of the person """
    def __init__(self,
                 year_of_birth=None, # For determining the age of a person
                 height=None, # For determining BMI
                 sex=None, # For determining BMI and ideal weight
                 ):
        pass


class BodyValues:
    """ Values the Body has """
    def __init__(self,
                 weight=None, # Weight in kg
                 waist_circumference=None, # Waist circumference in cm
                 date_of_measurement=None, # Date of measurement (timestamp)
                 ):
        pass



# RUNTIME #
def main():
    # Create a body
    body = Body()

if __name__ == "__main__":
    main()