import math

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x, y = [int(i) for i in input().split()]
left, right, up, down = 0, w - 1, 0, h - 1

def moveY():
    global y
    y = math.floor((up + down) / 2)

def goUp():
    global down
    down = y - 1
    moveY()

def goDown():
    global up
    up = y + 1
    moveY()

def moveX():
    global x
    x = math.floor((left + right) / 2)

def goLeft():
    global right
    right = x - 1
    moveX()

def goRight():
    global left
    left = x + 1
    moveX()

switch = {
    'U': goUp,
    'D': goDown,
    'L': goLeft,
    'R': goRight
}

# game loop
while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    for c in bomb_dir:
        switch[c]()

    print(x, y)
