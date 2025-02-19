

def insertion_sort(lst):
    """
    Insertion sort CLRS
    """

    n = len(lst)
    for i in range(1, n):
        k = lst[i]
        j = i - 1 
        while j >= 0 and lst[j] > k: 
            yield lst[:j+1] + [k] + lst[j+2:],  {j+1: 'red', j: 'green'}
            lst[j+1] = lst[j]
            yield lst[:j] + [k] + lst[j+1:],  {j+1: 'red', j: 'green'}
            j = j - 1
        lst[j+1] = k

    yield lst, {}


def merge(lst, left, mid, right):

    x = lst[left:right]

    n1 = len(lst[left:mid])
    n2 = len(lst[mid:right])
    
    l1, l2 = [None] * n1, [None] * n2

    for i in range(0, n1):
        l1[i] = lst[left+i]
    for j in range(0, n2): 
        l2[j] = lst[mid+j]

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2: # compare current elements in list, and add the smallest to new list.
        if l1[i] <= l2[j]:
            yield lst, {left+i: 'red', mid+j: 'green', k: 'white'}
            lst[k] = l1[i]
            i += 1
        else:
            yield lst, {left+i: 'red', mid+j: 'green', k: 'white'}
            lst[k] = l2[j]
            j += 1
        k += 1

    # when one of the initial lists are empty, copy the rest of the other list.
    while i < n1:
        lst[k] = l1[i]
        i += 1
        k += 1
    while j < n2:
        lst[k] = l2[j]
        j += 1
        k += 1 

    yield lst, {}

def merge_sort(lst, left=0, right=None):
    if not right: 
        right = len(lst)
    if len(lst[left:right]) <= 1:
        return lst
    mid = int((left+right)/2) # midpoint, int floors
    yield from merge_sort(lst, left, mid)
    yield from merge_sort(lst, mid, right)
    yield from merge(lst, left, mid, right)
    yield lst, {}

def partition(lst):

    n = len(lst)
    pivot_value = lst[-1]
    i = -1

    for j in range(0, n-1): # dont include pivot key 
        #print('j', j, lst[j])
        if lst[j] <= pivot_value:
            i = i + 1
            #print('i', i)
            lst[i], lst[j] = lst[j], lst[i] # exchange elements
    # print(lst, len(lst), i+1 )
    lst[-1], lst[i+1] = lst[i+1], lst[-1] # swap pivot value to middle between low and high 
    # print(lst, len(lst), i+1 )
    return lst, i + 1

def quicksort(lst):

    if len(lst) > 1:
        #print('list', lst)
        lst, q = partition(lst)   
        #print('q', q)
        #print('partition', lst[:q-1], lst[q], lst[q+1:])
        
        lst_left = quicksort(lst[:q])
        lst_right = quicksort(lst[q+1:])
        lst = lst_left + lst[q:q+1] + lst_right
        #print('combined', lst)
    return lst 

if __name__ == '__main__':

    import random 

    l = [5, 6, 8, 14, 2, 4]
    n = 100
    min, max = 1, 100
    l2 = [random.randint(min, max) for _ in range(0, 32)]

    print(l)
    # print(n, l2)

    # insertion_sort(l)
    # l2_insertion_sort = insertion_sort(l2)

    # print(merge_sort(l))
    l2_merge_sort = merge_sort(l2)

    # quicksort(l)
    # l2_quicksort = quicksort(l2)

    # print(l)
    # print(l2_insertion_sort)
    for l in l2_merge_sort:
        print(l)
    # print(next(l2_merge_sort))
    # print(l2_quicksort)
    # print('Check discrepancies:')
    #print([(x,y) for (x,y) in zip(l2_insertion_sort, l2_merge_sort) if x != y])
    # print([(x,y) for (x,y) in zip(l2_insertion_sort, l2_quicksort) if x != y])







