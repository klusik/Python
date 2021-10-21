alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

test_string = "RFRAFXWFIADERWIN"
string_length = len(test_string)

for i in range(0,26):

    for a in range(0,string_length):
        position = alphabet.find(test_string[a])
        position = (position + i) % 26
        print(f"{alphabet[position]}")
    print("")



