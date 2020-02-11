def bubble(arr, simulation=False):
    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]

    n = len(arr)
    finishedSwap = True

    iteration = 0
    if simulation:
        print("iteration",iteration,":",*arr)

    while finishedSwap:
        finishedSwap = False
        for i in range(1, n):
            if arr[i - 1] > arr[i]:
                swap(i - 1, i)
                finishedSwap = True
                if simulation:
                    iteration = iteration + 1
                    print("iteration",iteration,":",*arr)

    return arr
