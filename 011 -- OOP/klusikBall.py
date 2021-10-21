# Zadani: https://www.codewars.com/kata/53f0f358b9cb376eca001079

class Ball:
    ballType = "regualr"
    
    def __init__(self, ballType):
        self.ballType = ballType



ball1 = Ball

ball2 = Ball("whatever")


print(ball1.ballType)

print(ball2.ballType)

