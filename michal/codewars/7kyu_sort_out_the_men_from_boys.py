# zadani:
# ze zadaneho listu urci, ktere prvky jsou liche a ktere sude
# vystup bude list, ktery obsahuje dva listy - sude prvky a liche prvky serazene vzestupne resp. sestupne

def men_from_boys(arr):
    # your code here
    odd = []
    even = []
    for i in arr:
        if i % 2 == 0:
            even.append(i)
            # to make list distinct (= remove duplicates), transfer it to set
            set_even = set(even)
            # set does not support + -> transfer back to list
            even = list(set_even)
            # print('even', even, 'set_even', set_even)
        else:
            odd.append(i)
            set_odd = set(odd)
            odd = list(set_odd)
            # print('odd', odd, 'set_odd', set_odd)
    odd.sort(reverse=True)
    even.sort()
    output = even + odd

    # print('odd:', odd, 'even', even)

    return output

print(men_from_boys([7, 3, 14, 17]))
