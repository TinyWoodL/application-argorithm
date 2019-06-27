def MergeTwoSortedLists(l1, l2):
    iter1 = l1
    iter2 = l2
    if iter1 == None:
        return l2
    if iter2 == None:
        return l1
    if iter1.val > iter2.val:
        head = iter2
        iter2 = iter2.next
    else:
        head = iter1
        iter1 = iter1.next

    point = head

    while iter1 != None and iter2 != None:
        if iter1.val > iter2.val:
            point.next = iter2
            iter2 = iter2.next
        else:
            point.next = iter1
            iter1 = iter1.next

        point = point.next

    if iter1 == None:
        point.next = iter2
    else:
        point.next = iter1

    return head


def generateList(arr):
    if len(arr) == 0:
        return None
    head = ListNode(arr.pop(0))
    current = next = head
    while len(arr) != 0:
        next = ListNode(arr.pop(0))
        current.next = next
        current = next

    return head

def printList(list):
    print("")
    while list.next != None:
        print(list.val, "->")
        list = list.next
    print(list.val)

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


l1 = generateList([1, 2, 4])
l2 = generateList([1, 3, 4])
merged = MergeTwoSortedLists(l1, l2)

printList(merged)
