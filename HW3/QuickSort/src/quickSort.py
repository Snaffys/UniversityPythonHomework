def set_pivot(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if(arr[j] < pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[high], arr[i + 1] = arr[i + 1], arr[high]
    return i + 1 


def quick_sort(arr, low, high):
    if(low < high):
        pivot_index = set_pivot(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

def main():
    arr = [123, 512, -12, 25, 0, 324, -532, -532, 23, 4, 3]
    quick_sort(arr, 0, len(arr) - 1)
    print(arr)

if __name__ == "__main__":
    main()
