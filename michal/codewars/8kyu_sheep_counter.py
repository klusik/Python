# name of KATA = If you can't sleep, just count sheep!!
# given a non-negative ninteger, 3 for example, return a string with a murmur: '1 sheep...2sheep...3sheep...'
# input will always be valid, i.e. no negative integers.

# name of KATA = If you can't sleep, just count sheep!!
# given a non-negative ninteger, 3 for example, return a string with a murmur: '1 sheep...2sheep...3sheep...'
# input will always be valid, i.e. no negative integers.

def count_sheep(n):
    # your code

    # validation

    while True:
        try:
            n = int(n)
        except ValueError:
            print('exception: number not entered')
            validation = False
            break
        if n > 0:
            validation = True
            break
        else:
            validation = False
            print('nesmyslny pocet ovci')
            break

    # program
    output = []
    if validation:
        for i in range(1, n+1):
            output.append(str(i))
            output.append(' sheep...')

    return str(''.join(map(str, output)))


count_sheep(9)
