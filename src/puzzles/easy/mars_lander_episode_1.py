import sys
import math

surface_n = int(input())  # the number of points used to draw the surface of Mars.
surface = []
for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    surface.append((int(j) for j in input().split()))


a = 0
for point in range(1, len(surface)):
    if surface[point][0] < x:
        a = point

b = a+1
land_y = surface[a][1] + (x - surface[a][0]) * (surface[b][1] - surface[a][1]) / (surface[b][0] - surface[a][0])

# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]

    if land_y == -1:


    # 2 integers: rotate power. rotate is the desired rotation angle (should be 0 for level 1), power is the desired thrust power (0 to 4).
    if y > 2133 + land_y:
        print("0 0")
    else:
        print("0 " + str(max(0, min(4, - v_speed - 36))))
