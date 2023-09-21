def wololo():
    """
    Divide given number by 2 until no remaining number is present.
    Return number of iterations needed to achieve previous state.
    If given number consists solely of powers of two,
    print "Zadali jste mocninu dvou, super!"
    """

    # ===================== VALIDATE USER INPUT =====================
    while True:
        user_input = input("Zadej cislo, wololo! ")

        try:
            user_input = int(user_input)
        except ValueError:
            print(f'What?! {user_input} is not a number. You dearly test my patience! FIX IT!!!')

        if isinstance(user_input, int):
            print('At long last you managed to pick a number. Are you proud of yourself?')


        if user_input > 0:
            print('I hear angels singing hallelujah, you picked a positive number!')
            break
        else:
            print('Again? Not a positive number. FIX IT IMMEDIATELY!!!')
            continue
    # ===================== VALIDATE USER INPUT =====================

    counter = 0
    while True:
        # the stuff
        if user_input%2 == 0:
            user_input = user_input /2
            counter += 1
        else:
            # the powers of two
            if user_input == 1:
                print('Zadali jste mocninu dvou, super!')
            break


    return counter

print(f'counter: {wololo()}')
