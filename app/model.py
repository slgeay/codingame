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

    def __repr__(self):
        return f"Player{(self.name, self.pos)})"



class Human():
    id:int
    pos:Point
    player_dist:int
    player_rounds:int
    zombies_rounds:int

    def __init__(self, id, x, y):
        self.id = id
        self.pos = Point(x, y)
        #self.player_dist = self.pos.square_dist(ash.pos)
        #self.player_rounds = ash.rounds_to(self.pos)

    def compute_zombies_rounds(self, zombies):
        self.zombies_rounds = min([zombie.rounds_to(self.pos) for zombie in zombies])

    def __repr__(self):
        return f"Human{(self.id, self.pos)})"



class Zombie():
    id:int
    pos:Point
    next_pos:Point
    player_dist:int

    def __init__(self, id, x, y, xnext, ynext):
        self.id=id
        self.pos = Point(x, y)
        self.next_pos = Point(xnext, ynext)
        #self.player_dist = self.next_pos.square_dist(ash.pos)
        #self.human_dist = min([self.next_pos.square_dist(human.pos) for human in humans])

    def rounds_to(self, pos):
        return 1 + math.ceil(self.next_pos.dist(pos) / 400)

    def __repr__(self):
        return f"Zombie{(self.id, self.pos, self.next_pos)})"



