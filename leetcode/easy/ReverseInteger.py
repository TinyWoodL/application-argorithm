import sys


def reverse(x):
    min = pow(-2, 31)
    max = pow(2, 31) - 1
    if x > max or x <= min:
        return 0
    isNeg = 1 if x < 0 else 0
    if isNeg:
        x = abs(x)
    result = 0
    while x > 0:
        lastDigit = x % 10
        result = result*10+lastDigit
        x /= 10

    if isNeg:
        result *= -1
    if int(result) > max or int(result) <= min:
        return 0

    return result


x = int(sys.argv[1])

print(reverse(x))
