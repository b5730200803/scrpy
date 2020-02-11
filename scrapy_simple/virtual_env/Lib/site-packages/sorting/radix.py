def radix(arr, simulation=False):
    isDone = False
    position = 1

    iteration = 0
    if simulation:
        print("iteration",iteration,":",*arr)

    while not isDone:
        queueList = [list() for _ in range(10)]
        isDone = True

        for num in arr:
            digitNumber = num // position % 10
            queueList[digitNumber].append(num)
            if isDone and digitNumber > 0:
                isDone = False

        index = 0
        for numbers in queueList:
            for num in numbers:
                arr[index] = num
                index += 1

        if simulation:
            iteration = iteration + 1
            print("iteration",iteration,":",*arr)

        position *= 10
    return arr
