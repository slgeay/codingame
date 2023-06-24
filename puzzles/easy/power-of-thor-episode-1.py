light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]

while True:
    remaining_turns = int(input())
    move = ""

    if (light_y < initial_ty):
        move += "N"
        initial_ty -= 1
    elif (light_y > initial_ty):
        move += "S"
        initial_ty += 1

    if (light_x < initial_tx):
        move += "W"
        initial_tx -= 1
    elif (light_x > initial_tx):
        move += "E"
        initial_tx += 1

    print(move)
