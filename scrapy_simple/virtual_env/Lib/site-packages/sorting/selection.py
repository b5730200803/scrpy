def selection(arr, simulation=False):
    iteration = 0
    if simulation:
        print("iteration",iteration,":",*arr)

    for i in range(len(arr)):
        minimum = i

        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minimum]:
                minimum = j

        arr[minimum], arr[i] = arr[i], arr[minimum]

        if simulation:
                iteration = iteration + 1
                print("iteration",iteration,":",*arr)

    return arr
