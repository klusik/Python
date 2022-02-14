# * No Loops Allowed *
# You will be given an array (a) and a value (x). All you need to do is check
# whether the provided array contains the value, without using a loop.
# Array can contain numbers or strings. X can be either. Return true if the array contains the value, false if not.
# zjistil jsem, ze kata neni napsana pro python, tak to nemuzu vykazat v codewars, ale stejne to napisu

def cont(a, x):
    if x in a:
        return True
    else:
        return False
print(cont ([4,3,2,1,0,'a','b','c','d'], 0))