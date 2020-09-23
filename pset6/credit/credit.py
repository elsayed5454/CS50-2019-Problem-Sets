from cs50 import get_string

while True:
    s = get_string("Number: ")
    if s.isdigit():
        break

if not s.isdigit():
    print("INVALID")
elif len(s) == 15 and s[0] == '3':
    print("AMEX")
elif (len(s) == 16 or 19) and s[0] == '4':
    print("VISA")
elif len(s) == 16:
    print("MASTERCARD")
else:
    print("INVALID")