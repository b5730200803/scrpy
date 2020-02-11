def quick(arr, simulation=False):
    iteration = 0
    if simulation:
        print("iteration",iteration,":",*arr)
    arr, _ = quicksortrec(arr, 0, len(arr) - 1, iteration, simulation)
    return arr

def quicksortrec(arr, first, last, iteration, simulation):
    if first < last:
        pos = partition(arr, first, last)
        if simulation:
            iteration = iteration + 1
            print("iteration",iteration,":",*arr)

        _, iteration = quicksortrec(arr, first, pos - 1, iteration, simulation)
        _, iteration = quicksortrec(arr, pos + 1, last, iteration, simulation)

    return arr, iteration

def partition(arr, first, last):
    wall = first
    for pos in range(first, last):
        if arr[pos] < arr[last]:  # last is the pivot
            arr[pos], arr[wall] = arr[wall], arr[pos]
            wall += 1
    arr[wall], arr[last] = arr[last], arr[wall]
    return wall
