from cs50 import get_string
from sys import argv


def main():

    words = set()
    if len(argv) == 2:
        text = argv[1]
        file = open(text, "r")
        for line in file:
            words.add(line.rstrip("\n"))
        file.close()

        print("What message would you like to censor?")
        msg = get_string("")
        msg = msg.split()
        for word in msg:
            if word.lower() in words:
                for i in range(len(word)):
                    print("*", end="")
            else:
                print(f"{word}", end="")
            print(" ", end="")
        print()

    else:
        print("Usage: python bleep.py dictionary")
        exit(1)


if __name__ == "__main__":
    main()
