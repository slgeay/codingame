while True:
    max_h = 0
    max_i = 0

    for i in range(8):
        mountain_h = int(input())
        if (mountain_h > max_h):
            max_h = mountain_h
            max_i = i

    print(max_i)
