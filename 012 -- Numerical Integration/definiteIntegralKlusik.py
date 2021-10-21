# Definite integral of x^2 from a to b with delta

integralStart       = 0
integralEnd         = 3
integralSteps       = 100


# The integrated function y = x^2 
def x2(x):
    return x*x 

# computes Delta from boundaries and number of steps
def getDelta(integralStart, integralEnd, integralSteps):
    delta = abs(integralEnd - integralStart)/integralSteps
    return delta

def main():

    # reseting a counter
    sum = 0

    # creates a cycle in integralSteps steps (duh)
    for x in range(1, integralSteps+1):

        # I need to get not that integer from above, but x which is sent to x^2 function.
        # So I just multiply that integer x with a delta. And that's it.
        xDelta = x * getDelta(integralStart, integralEnd, integralSteps)
        
        # Computes a function value
        y = x2(xDelta)

        # sums it up
        sum = sum + y*getDelta(integralStart, integralEnd, integralSteps)

    print(sum)

if __name__ == "__main__": main()