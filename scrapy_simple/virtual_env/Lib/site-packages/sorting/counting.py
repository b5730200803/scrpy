def counting(arr):
    m = min(arr)
    different = 0
    if m < 0:
        different = -m
        for i in range(len(arr)):
            arr[i] += -m
    k = max(arr)
    tempArr = [0] * (k + 1)
    for i in range(0, len(arr)):
        tempArr[arr[i]] = tempArr[arr[i]] + 1

    for i in range(1, k + 1):
        tempArr[i] = tempArr[i] + tempArr[i - 1]

    resultArr = arr.copy()
    for i in range(len(arr) - 1, -1, -1):
        resultArr[tempArr[arr[i]] - 1] = arr[i] - different
        tempArr[arr[i]] = tempArr[arr[i]] - 1

    return resultArr
