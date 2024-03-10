import sys

surface = []
flat_surface = []
ground = 0
for i in range(int(input())):
    surface.append([int(j) for j in input().split()])
    if i > 1:
        if not flat_surface and surface[-1][1] == surface[-2][1]:
            flat_surface, ground = [surface[-2][0]], surface[-2][1]
        elif len(flat_surface) == 1 and surface[-1][1] != surface[-2][1]:
            flat_surface = [flat_surface[0], surface[-2][0]]

land_y = -1

def get_surface_y(x):
    a = 0
    for point in range(1, len(surface)):
        if surface[point][0] < x:
            a = point
    
    b = a+1
    return surface[a][1] + (x - surface[a][0]) * (surface[b][1] - surface[a][1]) / (surface[b][0] - surface[a][0])

# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]

    land_y = get_surface_y(x)
    height = y - ground
    distance = x - flat_surface[0] if x < flat_surface[0] else x - flat_surface[1] if x > flat_surface[1] else 0

    print(f"x: {x}, y: {y}, land_y: {land_y}, height: {height}, distance: {distance}", file=sys.stderr)
    
    if distance < 0 and h_speed < 25:
        rotate = -15
    elif distance > 0 and h_speed > -25:
        rotate = 15
    elif height < 0:
        rotate = 0
    elif h_speed > 10:
        rotate = 30
    elif h_speed < -10:
        rotate = -30
    else:
        rotate = 0

    # 2 integers: rotate power. rotate is the desired rotation angle (previous angle +/-15), power is the desired thrust power (0 to 4).
    if height < 500:
        print(rotate, "4")
    else:
        print(rotate, str(max(0, min(4, - v_speed - 18 + abs(h_speed)//5))))
