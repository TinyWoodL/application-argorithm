import sys


def common(strs):
    # return True
    if len(strs) == 0:
        return ""
    prefix = strs.pop(0)
    for str in strs:
        position = str.find(prefix)
        while position == -1 or position > 0:
            prefix = prefix[0:len(prefix)-1]
            position = str.find(prefix)
            if prefix == None:
                return ""

    return prefix


strs = ["aca","aacc","aa","aaca","aba"]
print(common(strs))
