#
# CW: https://www.codewars.com/kata/59175441e76dc9f9bc00000f
#
# Rule: 2*n^2

def main():
    # Let a user enter a value:

    atomicNumber = round(int(input("Enter the atomic number (will be rounded): ")))

    if atomicNumber < 1:
        atomicNumber = 1

    # Let the layers begin!

    # Initial value
    layer = 1

    # Creating and empty list for electrons
    electrons = list()

    # Full set now :-)
    electronsRemainToDistribute = atomicNumber

    while True:
        # implementing the rule
        maximumElectrons = layer*layer << 1

        # save the electrons
        if electronsRemainToDistribute > 0:
            # We still have free electrons to distribute
            if electronsRemainToDistribute > maximumElectrons:
                # Fill all the electrons
                electrons.append(maximumElectrons)
                # Compute new count of remaining electrons
                electronsRemainToDistribute -= maximumElectrons
            else:
                # Count of remaining electrons is less than
                # the capacity of the layer or same
                electrons.append(electronsRemainToDistribute)
                # we are finished
                break

        # let's hop to another layer
        layer += 1

    print("Electron values are:")
    print(electrons)

if __name__ == "__main__":
    main()

    # :-)