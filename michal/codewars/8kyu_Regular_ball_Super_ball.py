# https://www.codewars.com/kata/53f0f358b9cb376eca001079/train/python
# Create a class Ball. Ball objects should accept one argument for "ball type" when instantiated.
# If no arguments are given, ball objects should instantiate with a "ball type" of "regular."

class Ball(object):
    # your code goes here
    def __init__(self, ball_type='regular'):
        self.ball_type = ball_type
        
    def Determine_Type(self):
        if self.ball_type == "super":
            print(f"ball type: {self.ball_type}")
        else:
            print (f"ball type: {self.ball_type}")
            
# create instance

reg = Ball('super')
sup = Ball()

reg.Determine_Type()




            
    