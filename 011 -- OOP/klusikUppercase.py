# zadani: https://www.codewars.com/kata/56cd44e1aa4ac7879200010b

class CoolStrings:
    text = "Default String."

    def __init__(self, text):
        self.text = text
        pass

    def isUpper(self):
        # main logic of this shit

        
        if self.text.isupper(): 
            
            return True
        else:
            return False
        pass

myString1 = CoolStrings("TUTO JE MUJ STRING")
myString2 = CoolStrings("Tuto je muj druhy string.")

print(myString1.isUpper())
print(myString2.isUpper())

