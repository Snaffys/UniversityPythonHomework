def heapify(arr, size, ind):
    largest = ind
    l_ind = 2 * ind + 1
    r_ind = 2 * ind + 2

    if l_ind < size and arr[l_ind] > arr[largest]:
        largest = l_ind

    if r_ind < size and arr[r_ind] > arr[largest]:
        largest = r_ind

    if largest != ind:
        arr[ind], arr[largest] = arr[largest], arr[ind]
        heapify(arr, size, largest)


def heap_sort(arr):
    size = len(arr)

    for i in range(size // 2 - 1, -1, -1):
        heapify(arr, size, i)

    for i in range(size - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr
