from sys import argv
from cs50 import get_string

if (len(argv) == 2):
    # Prompt user for inputs
    for c in argv[1]:
        if c.isalpha():
            continue
        else:
            print("ERROR")
            exit(1)
    p = get_string("plaintext: ")
    # Vigenere's cipher
    print("ciphertext: ", end="")
    m = len(argv[1])
    k = argv[1]
    j = -1
    for c in p:
        if c.isalpha():
            j += 1
            if j == m:
                j = 0
            # Check for upper case
            if c.isupper():
                c = ord(c) - 65
                if k[j].isupper():
                    x = ord(k[j]) - 65
                    c = (c + x) % 26
                else:
                    x = ord(k[j]) - 97
                    c = (c + x) % 26
                c = chr(c + 65)
                print(f"{c}", end="")
            # Check for lower case
            else:
                c = ord(c) - 97
                if k[j].isupper():
                    x = ord(k[j]) - 65
                    c = (c + x) % 26
                else:
                    x = ord(k[j]) - 97
                    c = (c + x) % 26
                c = chr(c + 97)
                print(f"{c}", end="")
        else:
            print(c, end="")
    print()
# Prints an error message
else:
    print("Usage: python vigenere.py k")
    exit(1)