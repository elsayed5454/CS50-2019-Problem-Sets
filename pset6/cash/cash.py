from cs50 import get_float

while True:
    n = get_float("Change owed: ")
    if n > 0:
        break

n = round(n * 100)
c = 0

while n >= 25:
    c += 1
    n -= 25

while n >= 10:
    c += 1
    n -= 10

while n >= 5:
    c += 1
    n -= 5

while n >= 1:
    c += 1
    n -= 1

print(c)