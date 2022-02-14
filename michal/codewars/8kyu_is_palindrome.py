# Write function isPalindrome that checks if a given string (case insensitive) is a palindrome.

def is_palindrome(s):
    print(list(s.upper()))
    print(list(reversed(s.upper())))
    if list(s.upper()) == list(reversed(s.upper())):
        return True
    else:
        return False

print(is_palindrome('Bob'))