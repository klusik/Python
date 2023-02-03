"""
    Pushuper, but just in console :-D
"""
# IMPORTS #
import time
import os
from playsound import playsound

# RUNTIME #

def progressbar(actual_timer, timer_setup, scale):
    """ Prints a progressbar, lenght of scale """
    for position in range(scale-1):
        if position/scale < actual_timer/(timer_setup*60):
            print("#", end='')
        else:
            print('_', end='')
    print()

def main():
    # OS setup
    os.system("echo off")
    os.system("cls")

    # User input
    timer_setup = 0
    try:
        while(timer_setup <= 0):
            timer_setup = abs(int(input("Enter the number of minutes for timer: ")))
    except ValueError:
        print("Probably too much for asking for a number. Bye.")

    # Timing
    actual_timer = 0
    try:
        while True:
            os.system("cls")
            print(f"Timer will be sound every {timer_setup} minutes ({timer_setup*60} seconds)")
            print(f"Time left: {timer_setup * 60 - actual_timer} (seconds)")
            actual_timer += 1

            # Beeping
            if actual_timer == timer_setup*60:
                # Reset timer
                actual_timer = 0

                # Beep
                playsound("bell.wav")



            # Drawing a progressbar
            progressbar(actual_timer, timer_setup, 60)

            # Wait
            time.sleep(1)

    except KeyboardInterrupt:
        print("Thanks, bye :-)")

if __name__ == "__main__":
    main()