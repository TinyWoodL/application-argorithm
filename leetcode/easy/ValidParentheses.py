def validParentheses(s):
    left = ['(', '{', '[']
    map = {'(': ')', '{': '}', '[': ']'}
    stack = []
    for char in s:
        if left.count(char) > 0:
            stack.append(char)
            continue
        if len(stack) == 0:
            return False
        result = map[stack.pop()]
        if result != char:
            return False
    if len(stack) > 0:
        return False

    return True


print(validParentheses("("))
