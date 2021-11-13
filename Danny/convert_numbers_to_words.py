# Program for rewriting a number from
# a text to the number.
#
# Input is limited from "one" to "five",
# letters only lowercase (Python is case
# sensitive).
#
# All lines are heavily commented, so I hope
# you'll understand everything
#
# Author:   klusik@klusik.cz
#           2021
#

# PROGRAM

# First we need to ask user for input.
userInput = input("Input the number from one to five in words in lowercase: ")

# Check if the input is only in lowercase
# and say the user mildly 'fuck you' in that case
# but proceeds anyway
if userInput.islower():
    # Everything is okay here
    print("Cool, you wrote all lowercase words!")
else:
    # User wrote not all lowercase letters!
    print("Wtf dude, I said only lowercase, but I am not stupid, converting!")

    # Converting to lowercase, methot lower() does that
    userInput = userInput.lower()

# Now we are sure the letters are in lowercase, now we can
# try to convert them.
if userInput == "one":
    # If the word is 'one'
    print(f"The word {userInput} is converted to 1.")
elif userInput == "two":
    # Or if the first is not 'one,' try 'two'
    print(f"The word {userInput} is converted to 2.")
elif userInput == "three":
    # You know the drill...
    print(f"The word {userInput} is converted to 3.")
elif userInput == "four":
    print(f"The word {userInput} is converted to 4.")
elif userInput == "five":
    print(f"The word {userInput} is converted to 5.")
else:
    # This block of code is entered if all
    # things above failed.
    print("Wtf, dude, can't you just write a letter to five? :-D Bye.")

# And that's it :-)



