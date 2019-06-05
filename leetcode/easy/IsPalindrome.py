import sys


def isRaplinedrom(x):
    if x < 0:
        return False
    x = str(x)
    length = len(x)
    for index in range(0, length/2):
        if x[index] != x[length - index - 1]:
            return False

    return True


x = int(sys.argv[1])

print(isRaplinedrom(x))
