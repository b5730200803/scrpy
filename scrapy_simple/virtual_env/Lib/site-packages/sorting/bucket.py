def bucket(arr):
    numBuckets = len(arr)
    buckets = [[] for bucket in range(numBuckets)]
    for value in arr:
        index = value * numBuckets // (max(arr) + 1)
        buckets[index].append(value)
    sortedList = []
    for i in range(numBuckets):
        sortedList.extend(nextSort(buckets[i]))
    return sortedList

def nextSort(arr):
    for i in range(1, len(arr)):
        j = i - 1
        key = arr[i]
        while arr[j] > key and j >= 0:
            arr[j+1] = arr[j]
            j = j - 1
        arr[j + 1] = key
    return arr
