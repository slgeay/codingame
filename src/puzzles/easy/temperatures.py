result = 9999

n = int(input())  # the number of temperatures to analyse
for i in input().split():
    # t: a temperature expressed as an integer ranging from -273 to 5526
    t = int(i)
    if (abs(t) < abs(result) or abs(t) == abs(result) and t > result):
        result = t

print(0 if n == 0 else result)
