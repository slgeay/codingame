boost = True
last_checkpoint = ()
checkpoints: dict[tuple[int,int], int] = {}
thrust = 100

# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    if boost:
        checkpoint = (next_checkpoint_x, next_checkpoint_y)
        if last_checkpoint == checkpoint:
            pass
        elif checkpoints.get(checkpoint):
            if next_checkpoint_angle == 0:
                if max(checkpoints, key=checkpoints.get) == checkpoint:
                    thrust = "BOOST"
                else:
                    last_checkpoint = checkpoint
            else:
                pass
        else:
            checkpoints[(next_checkpoint_x, next_checkpoint_y)] = next_checkpoint_dist
            last_checkpoint = checkpoint

    if thrust != "BOOST":
        #thrust = next_checkpoint_dist // max (1, abs(next_checkpoint_angle)) * 5
        #print(str(next_checkpoint_dist) + " " + str(next_checkpoint_angle) + " " + str(thrust), file=sys.stderr, flush=True)
        thrust = min(100, next_checkpoint_dist // 5) if abs(next_checkpoint_angle) < 70 else 0

    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + str(thrust))
    
    if thrust == "BOOST":
        thrust = 100
        boost = False
