from json import dumps, loads
from typing import List
import sys


def gear_balance(n_gears: int, connections: List[List[int]]) -> List[int]:
    '''

    Args:

        - n_gears (int): An integer representing the number of gears in the system (numbered from 0 to N-1).
        - connections (List[List[int]]): An array representing all pairs of gears connected together.

    Returns:

        An array of two integers representing the number of gears rotating clockwise and counterclockwise respectively, or [-1, -1] if the configuration is invalid.
    '''
    gears = [None] * n_gears
    gears[0] = True
    
    while(None in gears):
        for gear1, gear2 in connections:
            if gears[gear1] is None and gears[gear2] is None:
                pass
            elif gears[gear1] is None:
                gears[gear1] = not gears[gear2]
            elif gears[gear2] is None:
                gears[gear2] = not gears[gear1]

    for gear1, gear2 in connections:
        if gears[gear1] == gears[gear2]:
            return [-1, -1]

    return [gears.count(True), gears.count(False)]

# Ignore and do not change the code below


def try_solution(output: List[int]):
    '''
    Try a solution

    Args:

        - List[int] (List[int]): An array of two integers representing the number of gears rotating clockwise and counterclockwise respectively, or [-1, -1] if the configuration is invalid.
    '''
    json = output
    print("" + dumps(json, separators=(',', ':')))

def main():
    res = gear_balance(
        loads(input()),
        loads(input())
    )
    try_solution(res)


if __name__ == "__main__":
    main()
# Ignore and do not change the code above
