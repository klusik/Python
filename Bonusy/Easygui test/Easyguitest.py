"""
    Test the "easygui" :-)
"""

# IMPORTS #
import easygui

# RUNTIME #
if __name__ == "__main__":
    """ Main magic :-) """

    answer = easygui.ynbox("Is this the best app ever?", "The best dialogue box ever", ("Yes", "Also Yes"))

    if answer:
        easygui.msgbox(f"Wise words.")
    else:
        easygui.msgbox("Also wise words.")
