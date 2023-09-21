"""
    Nurofen: Dosage planner & calculator

    Author: Rudolf Klusal, 2023
"""

# IMPORTS #
import person


# RUNTIME #
if __name__ == "__main__":
    user = person.Person(name='default', age=9)

    print(user)

    user.save_to_file()