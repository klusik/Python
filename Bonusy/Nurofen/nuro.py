"""
    Nurofen: Dosage planner & calculator

    Author: Rudolf Klusal, 2023
"""

# IMPORTS #
import src.person

# RUNTIME #
if __name__ == "__main__":
    person = src.person.Person(name='Maruska', age=4)

    print(person.name, person.age)