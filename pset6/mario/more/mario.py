from cs50 import get_int
# Prompt uset for non negative integer inclusive between 1 and 8
while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break

for i in range(n):
    for j in range(n - (i + 1), 0, -1):
        print(" ", end="")
    for k in range(-1, i):
        print("#", end="")
# Just add two spaces and the same loop as above
    print("  ", end="")
    for k in range(-1, i):
        print("#", end="")
    print()