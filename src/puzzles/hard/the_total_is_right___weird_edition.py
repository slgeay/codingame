import sys
import math


n = int(input())
a = int(input())

mem = {a}
mem_per_size = {1: {a}}

for size in range(2, 13):
    mem_per_size[size] = set()
    for left_size in range(1, size):
        right_size = size - left_size
        for left in mem_per_size[left_size]:
            for right in mem_per_size[right_size]:
                for operation in ['+', '-', '*', '/']:
                    result = None
                    if operation == '+':
                        result = left + right
                    elif operation == '-':
                        result = left - right
                    elif operation == '*':
                        result = left * right
                    elif operation == '/' and left % right == 0:
                        result = left // right
    
                    if result is None or result <= 0 or result in mem:
                        continue

                    if result == n:
                        print(size)
                        sys.exit()

                    mem.add(result)
                    mem_per_size[size].add(result)

                        
