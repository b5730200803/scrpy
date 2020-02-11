def maxheap(arr, simulation=False):
    iteration = 0
    if simulation:
        print("iteration",iteration,":",*arr)

    for i in range(len(arr) - 1, 0, -1):
        iteration = maxheapify(arr, i, simulation, iteration)

    if simulation:
                iteration = iteration + 1
                print("iteration",iteration,":",*arr)
    return arr


def maxheapify(arr, end, simulation, iteration):
    lastParent = (end - 1) // 2

    for parent in range(lastParent, -1, -1):
        currentParent = parent

        while currentParent <= lastParent:
            child = 2 * currentParent + 1
            if child + 1 <= end and arr[child] < arr[child + 1]:
                child = child + 1

            if arr[child] > arr[currentParent]:
                arr[currentParent], arr[child] = arr[child], arr[currentParent]
                currentParent = child
                if simulation:
                    iteration = iteration + 1
                    print("iteration",iteration,":",*arr)
            else:
                break
    arr[0], arr[end] = arr[end], arr[0]
    return iteration

def minheap(arr, simulation=False):
    iteration = 0
    if simulation:
        print("iteration",iteration,":",*arr)

    for i in range(0, len(arr) - 1):
        iteration = minheapify(arr, i, simulation, iteration)

    return arr


def minheapify(arr, start, simulation, iteration):
    end = len(arr) - 1
    lastParent = (end - start - 1) // 2

    for parent in range(lastParent, -1, -1):
        currentParent = parent

        while currentParent <= lastParent:
            child = 2 * currentParent + 1
            if child + 1 <= end - start and arr[child + start] > arr[
                child + 1 + start]:
                child = child + 1

            if arr[child + start] < arr[currentParent + start]:
                arr[currentParent + start], arr[child + start] = \
                    arr[child + start], arr[currentParent + start]
                currentParent = child
                if simulation:
                    iteration = iteration + 1
                    print("iteration",iteration,":",*arr)
            else:
                break
    return iteration
