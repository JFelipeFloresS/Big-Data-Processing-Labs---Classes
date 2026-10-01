def my_main(my_array):
    res = 0

    size = len(my_array)

    for i in range(size - 1):
        for j in range(i + 1, size):
            if my_array[i] > my_array[j]:
                res += 1

    return res

if __name__ == "__main__":
    my_array = [1, 3, 5, 2, 4, 6]
    res = my_main(my_array)
    print(res)