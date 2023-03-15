"""
    Enter values of drive ratios and other values,
    compute engine rpms.
"""


def input_from_user(
        question_prompt: str = '?',
        lowest: float = None,
        highest: float = None,
) -> float:
    """ User input for values """
    while True:
        usr_value = float(input(question_prompt))

        if lowest and highest:
            if lowest < usr_value < highest:
                return usr_value

        elif lowest:
            if lowest < usr_value:
                return usr_value
        elif highest:
            if highest > usr_value:
                return usr_value
        else:
            return usr_value

def get_speed(gbx_ratio, drivetrain_ratio, wheel_diameter, speed) -> int:
    return int(((speed / 3.6) * gbx_ratio * drivetrain_ratio * 60)/(3.14 * wheel_diameter))


if __name__ == "__main__":
    try:
        gbx_ratios = []

        # Gears in gearbox
        for gear in range(1, 6):
            gbx_ratios.append(
                input_from_user(
                    question_prompt=f"Enter a ratio of {gear}. gear: ",
                    lowest=0,
                )
            )

        # Gears in a drivetrain
        drivetrain = input_from_user(
            question_prompt="Enter a drivetrian ratio: ",
            lowest=0,
        )

        # Wheel circumference
        wheel_diameter = input_from_user(
            question_prompt="Enter a wheel diameter: ",
            lowest=0.001
        )


    except IndexError as err:
        print(f"Internal error {str(err)}")

    except ValueError as err:
        print(f"Value coudln't be recognized: {str(err)}")


    # Computation:
    speeds = [30, 50, 60, 80, 90, 110, 130, 150, 200]

    for speed in speeds:
        revolutions = []
        for gear in gbx_ratios:
            revolutions.append(
                get_speed(
                    gbx_ratio=gear,
                    drivetrain_ratio=drivetrain,
                    wheel_diameter=wheel_diameter,
                    speed=speed,
                )
            )

        print(f"For speed {speed}:")
        for gear, revolution in enumerate(revolutions):
            print(f"Gear {gear + 1}: {revolution} rpm")


