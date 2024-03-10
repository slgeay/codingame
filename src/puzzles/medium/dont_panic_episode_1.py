nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in input().split()]
elevators = {f: p for f, p in [map(int, input().split()) for _ in range(nb_elevators)]}

while True:
    inputs = input().split()
    clone_floor = int(inputs[0])
    clone_pos = int(inputs[1])
    direction = inputs[2]

    if clone_floor == -1:
        print("WAIT")
        continue

    out_pos = exit_pos if clone_floor == exit_floor else elevators.get(clone_floor, [0,width - 1][direction == "RIGHT"])

    if direction == "RIGHT":
        if clone_pos > out_pos:
            print("BLOCK")
            continue
    else:
        if clone_pos < out_pos:
            print("BLOCK")
            continue
    
    print("WAIT")
    
    
