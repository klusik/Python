# file for amusement of my litte child 
# IMPORTS
import turtle

# define gif file as new coursor
maja_path = r"C:\Users\Z0001932\OneDrive - ZF Friedrichshafen AG\prace\python\projects\streda\python_git\michal\PyLadies\03\maja.gif"

# save defined gif file as a available shave in module turtle
turtle.register_shape(maja_path)

# set the maja shape active
turtle.shape(maja_path)

# non-funcitonal code
# failed attempt to resize new coursor
# turtle.resizemode("user")
# turtle.shapesize(0.2, 0.2, 1)

# test only Maja
'''
def Maja(n):
    for i in range(n):
        if i in [n/10, n/20, n/30, n/40, n/50, n/60, n/70, n/80, n/90]:
            print('''
            ODPOCIVAM v POKOJI
            ''')
        elif i == n-1:
            print('KONCIM SVUJ LET')
        else: 
            print('>>> LETIM. BZZZZZZZZZ')
'''

def Maja_g():
    '''
    Draws custom shaped coursor ...
    '''
    
    pass

# call of text only Maja()
# Maja(30000)
