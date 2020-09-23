from sys import argv
from cs50 import get_string

if (len(argv) == 2):
    # Prompt user for inputs
    k = int(argv[1])
    p = get_string("plaintext: ")
    # Caesar's cipher
    print("ciphertext: ", end="")
    for c in p:
        if c.isalpha():
            if c.isupper():
                print(f"{chr((ord(c) - 65 + k) % 26 + 65)}", end="")
            else:
                print(f"{chr((ord(c) - 97 + k) % 26 + 97)}", end="")
        else:
            print(c, end="")
    print()
# Prints an error message
else:
    print("Usage: python caesar.py k")
    exit(1)