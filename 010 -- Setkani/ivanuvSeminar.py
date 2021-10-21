myList = [number*number for number in range(10)]
myList2 = [(n+1/n) for n in range(0, 11) if n>0]
myList3 = [n*n for n in range(10) if n%2==0]

text = "Per aspera ad inferi"
print(text)
myListString = [text[i] for i in range(0, len(text)) if text[i]!="a" and text[i]!="e" and text[i]!="i"  and text[i]!="o"  and text[i]!="u"]


print(myList)
print(myList2)
print(myList3)
print(myListString)