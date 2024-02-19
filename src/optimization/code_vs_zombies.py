from __future__ import annotations
import sys
import math
from typing import List

class Point:
    x:int
    y:int

    def __init__(self, x, y):
        self.x=x
        self.y=y

    def dist(self, other:Point) -> float:
        return math.sqrt(self.square_dist(other))

    def square_dist(self, other:Point) -> int:
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2

    def __repr__(self):
        return f"{(self.x, self.y)})"



class Player():
    name:str
    pos:Point

    def __init__(self, name, x, y):
        self.name = name
        self.pos = Point(x, y)

    def rounds_to(self, pos):
        return math.ceil(self.pos.dist(pos) / 1000) - 2


ash:Player = Player("Ash", 0, 0)


class Human():
    id:int
    pos:Point
    player_dist:int
    player_rounds:int
    zombies_rounds:int

    def __init__(self, id, x, y):
        self.id = id
        self.pos = Point(x, y)
        self.player_dist = self.pos.square_dist(ash.pos)
        self.player_rounds = ash.rounds_to(self.pos)

    def compute_zombies_rounds(self, zombies):
        self.zombies_rounds = min([zombie.rounds_to(self.pos) for zombie in zombies])

    def __repr__(self):
        return f"Human{(self.id, self.pos, self.player_dist, self.player_rounds, self.zombies_rounds)})"



humans:List[Human] = [Human(-1, 0, 0)]
fake_human = Human(-1, 0, 0)
closest_human:Human



class Zombie():
    id:int
    pos:Point
    next_pos:Point
    player_dist:int

    def __init__(self, id, x, y, xnext, ynext):
        self.id=id
        self.pos = Point(x, y)
        self.next_pos = Point(xnext, ynext)
        self.player_dist = self.next_pos.square_dist(ash.pos)
        self.human_dist = min([self.next_pos.square_dist(human.pos) for human in humans])

    def rounds_to(self, pos):
        return 1 + math.ceil(self.next_pos.dist(pos) / 400)


zombies:List[Zombie]
fake_zombie = Zombie(-1, 0, 0, 0, 0)
closest_zombie:Zombie
best_human = fake_human


# game loop
while True:
    humans = []
    closest_human = fake_human
    zombies = []
    closest_zombie = fake_zombie

    x, y = [int(i) for i in input().split()]
    ash = Player("Ash", x, y)

    human_count = int(input())

    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        human = Human(human_id, human_x, human_y)
        humans.append(human)
        if closest_human.id == -1 or human.player_dist < closest_human.player_dist:
            closest_human = human
        
    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombie = Zombie(zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext)
        zombies.append(zombie)
        if closest_zombie.id == -1 or zombie.human_dist < closest_zombie.human_dist:
            closest_zombie = zombie

    best_human = fake_human
    for human in humans:
        human.compute_zombies_rounds(zombies)
        print(human, file=sys.stderr, flush=True)
        if human.zombies_rounds < human.player_rounds:
            continue
        if best_human.id == -1 or human.player_dist < best_human.player_dist:
            best_human = human

    if best_human.id != -1 and best_human.zombies_rounds - 1 <= best_human.player_rounds:
        print(f"{best_human.pos.x} {best_human.pos.y} Human {best_human.id}")
    else:
        print(f"{closest_zombie.next_pos.x} {closest_zombie.next_pos.y} Zombie {closest_zombie.id}")
