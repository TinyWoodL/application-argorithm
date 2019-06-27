def RemoveDuplicatesfromSortedArray(nums):
    if len(nums) == 0:
        return 0

    i = 0
    for index, num in enumerate(nums):
        if i == index:
            continue
        if num != nums[i]:
            i += 1
            nums[i] = num

    return i+1


print(RemoveDuplicatesfromSortedArray([1, 1, 2]))
