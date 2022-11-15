# IMPORTS #
import random
import string

# CLASSES #
class Human:
    def __init__(self,
                 age = 0, # default age
                 height = 50, # default height
                 weight = 3.5, # default weight
                 name = "", # default name
                 gender = "M", # default gender
                 ):
        """ This method would run automatically after object creation """
        # Set values of attributes
        self.age = age
        self.height = height
        self.weight = weight
        self.name = name

        self.set_name(name)

    # SETTERS for attributes
    def set_age(self, age):
        self.age = age

    def set_height(self, height):
        self.height = height

    def set_weight(self, weight):
        self.weight = weight

    def set_name(self, name):
        if name == "":
            name_length = random.randint(4, 8) # 4 to 8 characters
            for position in range(name_length):
                if position == 0:
                    name += str(random.choice(string.ascii_uppercase))
                else:
                    name += str(random.choice(string.ascii_lowercase))
            self.name = name
        else:
            self.name = name

    # GETTERS of attributes
    def get_age(self):
        return self.age

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_name(self):
        return self.name

    # Compute stuff
    def get_bmi(self):
        return self.weight/((self.height/100)**2)


class People:
    people = []

    def save_human(self, human_to_be_saved: Human):
        self.people.append(human_to_be_saved)

    def get_avg_bmi(self):
        bmi_bulk = 0
        if self.people:
            for human in self.people:
                bmi_bulk += human.get_bmi()
            return bmi_bulk/len(self.people)
        else:
            return None


    def get_max_bmi(self):
        max_bmi = 0
        for human in self.people:
            if human.get_bmi() > max_bmi:
                max_bmi = human.get_bmi()

        return max_bmi

    def get_min_bmi(self):
        min_bmi = 0
        for counter, human in enumerate(self.people):
            if counter == 0:
                min_bmi = human.get_bmi()

            if human.get_bmi() < min_bmi:
                min_bmi = human.get_bmi()

        return min_bmi

    def print_all(self):
        for counter, human in enumerate(self.people):
            print(f"{counter + 1}: {human.get_name()}"
                  f"\n\tHeight: {human.get_height()}"
                  f"\n\tWeight: {human.get_weight()}"
                  f"\n\tBMI:    {human.get_bmi()}")


# Generate people
people = People()

for _ in range(100): #generate 100 humans
    human = Human(
        age = random.randint(20, 60),
        weight = random.randint(50, 150),
        height = random.randint(150, 200),
    )

    people.save_human(human)

# Display all humans
people.print_all()

# Empty line
print()

# Display minimal BMI
print(f"Minimal BMI: {people.get_min_bmi()}")

# Display maximal BMI
print(f"Maximal BMI: {people.get_max_bmi()}")

# Display average BMI
print(f"Average BMI: {people.get_avg_bmi()}")
    
