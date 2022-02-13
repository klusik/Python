# INSTRUCTIONS:
# Story
# Your online store likes to give out coupons for special occasions. Some customers try to cheat the system by entering
# invalid codes or using expired coupons.
#
# Task
# Your mission:
# Write a function called checkCoupon which verifies that a coupon code is valid and not expired.
#
# A coupon is no more valid on the day AFTER the expiration date. All dates will be passed as strings in this format:
# "MONTH DATE, YEAR".
#
# Examples:
# checkCoupon("123", "123", "July 9, 2015", "July 9, 2015")  == True
# checkCoupon("123", "123", "July 9, 2015", "July 2, 2015")  == False

# My comments:
# The idea how to solve the task is to compare entered coupon and valid coupon. The issue is with date. It cannot be
# simply compared (month given as string, convert is affected by local environment => in defferent languages names of
# months are not same is in english => the code would not work everywhere.).
# To make dates comparable months names must be converted to numbers. Then the whole date can be stored
# in a tuple. As tuple is comparing from first item onwards, the order of data stored in tuple must be YYYYY, MM, DD.

def check_coupon(entered_code, correct_code, current_date, expiration_date):
    # lists containing separated strings of dates
    lstCurrentDate = current_date.split()
    #print('list of current dates splitted: ', lstCurrentDate)

    lstExpirationDate = expiration_date.split()
    #print('list of exp dates splitted: ', lstExpirationDate)

    sCurrentYear = int(lstCurrentDate[2])  # saved as string
    #print('Current Year: ', sCurrentYear)

    sCurrentMonth = lstCurrentDate[0]  # contains name, not number of the month
    #print('Current Month: ', sCurrentMonth)

    sCurrentDay = lstCurrentDate[1]
    sCurrentDay = int(sCurrentDay[0])  # slicing the string, gets rid of comma and converts to int
    #print('Current Day', sCurrentDay)

    sExpYear = int(lstExpirationDate[2])  # saved as string
    #print('Exp Year: ', sExpYear)

    sExpMonth = lstExpirationDate[0]  # contains name, not number of the month
    #print('Exp Month: ', sExpMonth)

    sExpDay = lstExpirationDate[1]
    sExpDay = int(sExpDay[0])  # slicing the string, gets rid of comma and converts to int
    #print('Exp Day: ', sExpDay)


    # dict converting name of month to number
    dMonths = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    # cycle to convert month name into number
    for dKey in dMonths.keys():
        if dKey == sCurrentMonth:
            sCurrentMonth = dMonths[sCurrentMonth]
            #print('aktualni mesic prepsany cyklem z nazvu na cislo: ', sCurrentMonth)
        if dKey == sExpMonth:
            sExpMonth = dMonths[sExpMonth]
            #print('exp month presany cyklem z nazvu na cislo: ', sExpMonth)

    # tuple to store the coupon that is being checked
    tChecked = (sCurrentYear, sCurrentMonth, sCurrentDay)
    #print('tuple current: ', tChecked)

    # tuple to stor the coupon that is correct
    tCorrect = (sExpYear, sExpMonth, sExpDay)
    #print('tuple correct: ', tCorrect)

    # now the two tuples are comparable
    if tChecked > tCorrect and entered_code != correct_code:
        return False
    else:
        return True



