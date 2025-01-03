#simple binary search problem
#search for the index of target T in a sorted array with array size N
#the array has 10 elements (1000, 2000, 3000... 9000, 10000)

#target = 8400
#array = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

def binary_search(array, target):
    left = 0
    right = len(array) - 1
    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1