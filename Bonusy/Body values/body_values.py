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
        self.year_of_birth = year_of_birth
        self.height = height
        self.sex = sex



class BodyValues:
    """ Values the Body has """
    def __init__(self,
                 weight=None, # Weight in kg
                 waist_circumference=None, # Waist circumference in cm
                 date_of_measurement=None, # Date of measurement (timestamp)
                 ):
        self.weight = weight
        self.waist_circumference = waist_circumference
        self.date_of_measurement = date_of_measurement



# RUNTIME #
def main():
    # Create a body
    body = Body()

if __name__ == "__main__":
    main()