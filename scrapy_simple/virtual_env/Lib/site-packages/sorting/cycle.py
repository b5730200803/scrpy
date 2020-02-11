def cycle(arr):
    lenArr = len(arr)
    for cur in range(lenArr - 1):
        item = arr[cur]

        index = cur
        for i in range(cur + 1, lenArr):
            if arr[i] < item:
                index += 1

        if index == cur:
            continue

        while item == arr[index]:
            index += 1
        arr[index], item = item, arr[index]

        while index != cur:

            index = cur
            for i in range(cur + 1, lenArr):
                if arr[i] < item:
                    index += 1

            while item == arr[index]:
                index += 1
            arr[index], item = item, arr[index]
    return arr
