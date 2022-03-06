# file for amusement of my litte child 

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
Maja(30000)
