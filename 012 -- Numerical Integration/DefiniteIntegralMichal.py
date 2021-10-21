# Definite ingegral Michal
# urcity integral
# zadani fce, pod kterou budeme pocitat plochu

def x2(x):
	return x*x
	
def plocha(start, end, n):
	'''
	vypocita plochu pod krivkou
	argumenty jsou
	pocateni hodnota intervalu
	konecna hodnota intervalu
	pocet vzorku
	'''
	lplocha =[]
	for i in range(1, n+1):
		delta = (abs(start-end)/n)
		vyska = x2(i * delta)
		obsah = vyska * delta
		lplocha.append(obsah)
		
	return sum(lplocha)
	
print(plocha(0, 3, 10))





