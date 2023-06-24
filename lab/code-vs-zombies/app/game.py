from random import randint, random
from typing import List
from ai import AI
from model import Human, Player, Zombie

MAX_ZOMBIES = 100
MAX_HUMANS = 100

class Game():
    zombies:List[Zombie] = []
    humans:List[Human] = []
    ash:Player
    ai:AI

    def __init__(self):
        self.ash = Player("Ash", 0, 0)

        for i in range(randint(1, MAX_HUMANS)):
            self.humans.append(Human(i, 0, 0))

        for i in range(randint(1, MAX_ZOMBIES)):
            self.zombies.append(Zombie(i, 0, 0, 0, 0))
            
        self.ai = AI()



    def run(self):
        while self.zombies:
            str = f"{self.ash.pos.x} {self.ash.pos.y}\n"
            str += f"{len(self.humans)}\n"
            for human in self.humans:
                str += f"{human.id} {human.pos.x} {human.pos.y}\n"
            str += f"{len(self.zombies)}\n"
            for zombie in self.zombies:
                str += f"{zombie.id} {zombie.pos.x} {zombie.pos.y} {zombie.next_pos.x} {zombie.next_pos.y}\n"

            result = self.ai.iterate(str).split()
            print(result)
            return
        



