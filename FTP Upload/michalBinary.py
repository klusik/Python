# learning purposes only
# convert given binary number to decadic scale

def convert_bin_to_dec(sBin_number):
    index = 0
    # create list of powers of 2
    dPowers = {}
    iPowers_of_two = len(sBin_number)
    sNumber_value = ''
    for i in sBin_number:
        sNumber_value = i
        iPowers_of_two = len(sBin_number) - index
        dPowers[iPowers_of_two] = sNumber_value
        index = index + 1

    for i in dPowers[keys]:


print(convert_bin_to_dec('010111'))