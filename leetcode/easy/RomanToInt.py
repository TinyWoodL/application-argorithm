import sys


def romanToInt(s):
    roman = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    result = 0
    ignore = False
    for index in range(0, len(s)):
        if ignore:
            ignore = False
            continue
        char = s[index]
        value = roman[char]
        if index + 1 < len(s) and roman[s[index + 1]] > value:
            value = roman[s[index + 1]] - value
            ignore = True
        result += value

    return result


s = str(sys.argv[1])

print(romanToInt(s))
