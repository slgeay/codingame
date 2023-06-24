import sys
from typing import Callable

def print_err(s):
    print(s, file=sys.stderr)

def print_grid(grid):
    for i in range(len(grid)):
        print("".join(grid[i]))

def print_err_grid(grid):
    for i in range(len(grid)):
        print_err("".join(grid[i]))


class Direction:
    name: str
    output:str
    test : Callable
    h: int
    w: int
    
    def __init__(self, name: str, output: str, test: Callable, h = 0, w = 0):
        self.name = name
        self.output = output
        self.test = test
        self.h = h
        self.w = w

    def __repr__(self):
        return f"Direction<{self.name}\"{self.output}\"({self.h},{self.w})>"


north = Direction('North', '^', lambda ball: ball.n <= ball.h, h = -1)
south = Direction('South', 'v', lambda ball: ball.n < height - ball.h , h = 1)
west = Direction('West', '<', lambda ball: ball.n <= ball.w, w = -1)
east = Direction('East', '>', lambda ball: ball.n < width - ball.w , w = 1)


class Ball:
    h: int
    w: int
    n: int

    def __init__(self, h, w, n):
        self.h = h
        self.w = w
        self.n = n

    def __repr__(self):
        return f"<{self.h},{self.w}={self.n}>"

    def can_go(self, direction:Direction, output):
        h = self.h + self.n * direction.h
        w = self.w + self.n * direction.w
        return direction.test(self) and (grid[h][w]  == 'H' or grid[h][w] == '.' and output[h][w] == '.')


grid = []
balls = []
holes = []
width, height = [int(i) for i in input().split()]
output = [['.'] * width for i in range(height)]
for i in range(height):
    row = input()
    for j in range(width):
        if (row[j] == "H"):
            holes.append([i, j])
        elif (row[j].isnumeric()):
            balls.append(Ball(i, j, int(row[j])))
            output[i][j] = '?'
    grid.append(list(row))

balls.sort(key = lambda ball: ball.n)

def resolve(balls, output):
    print_err(f"resolve {balls}")
    print_err_grid(grid)

    if not balls: # success
        print_grid(output)
        exit()

    ball = balls.pop(0)

    for direction in [north, south, east, west]:
        if ball.can_go(direction, output):
            print_err(f"{ball.n} can do {direction.name}")
            new_output = [row[:] for row in output]
            new_output[ball.h][ball.w] = '.'
            ok = True
            for i in range(ball.n):
                ih = ball.h + i * direction.h
                iw = ball.w + i * direction.w
                if new_output[ih][iw] != '.' or grid[ih][iw] == 'H' or grid[ih][iw] == 'h':
                    print_err(f"Nope: [{new_output[ih][iw]},{grid[ih][iw]}] is {direction.name}({ih},{iw})")
                    ok = False
                    break
                new_output[ih][iw] = direction.output
            if ok:
                nh = ball.h + ball.n * direction.h
                nw = ball.w + ball.n * direction.w
                if grid[nh][nw] == 'H':
                    grid[nh][nw] = 'h'
                    resolve(balls, new_output)
                    grid[nh][nw] = 'H'
                elif ball.n > 1:
                    if grid[nh][nw] == '.' and new_output[nh][nw] == '.':
                        balls.insert(0, Ball(nh, nw, ball.n - 1))
                        new_output[nh][nw] = '?'
                        resolve(balls, new_output)
                        balls.pop(0)
            print_err(f"{ball.n} shouldn't go {direction.name}")

    balls.insert(0, ball)

resolve(balls, output)
