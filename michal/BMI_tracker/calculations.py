'''
author: Michal Sykora
date: 7.5.2022
version: 0.1 pre-alpha
license: freeware
'''

# GLOBAL IMPORTS

# PRIVATE IMPORTS

# THIRD PARTY IMPORTS

# functions for handling xml files to be written
# functions for creating graphs to be written
# functions for creating PDF files to be written

# calculate BMI
def calculateBMI(weight, height):
    '''Calculate Body Mass Index
    
    INPUT
    weight - weight of user [kg], integer
    OUTPUT
    
    '''
    #BMI formula
    BMI = weight / (height * height)

    bmi_ranges = '''
                        BMI ranges
-------------------------------------------------------
| BMI             | Cathegory         | Healt risks   | 
|=====================================================|
| <18,5           | Underweight       | high          |
|-----------------------------------------------------|
| 18,5 - 24,9     | Normal            | minimal       |
|-----------------------------------------------------|
| 25 - 29,9       | Overweight        | low           |
|-----------------------------------------------------|
| 30 - 34,9       | Obesity level 1   | medium        |
|-----------------------------------------------------|
| 35 - 39         | Obesity level 2   | high          |
|-----------------------------------------------------|
| > 40            | Obesity level 3   | very high     |
-------------------------------------------------------
'''
    return BMI, bmi_ranges
