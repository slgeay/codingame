import sys
import math
from enum import Enum
import random
import time
from operator import methodcaller

class Cell:
    def __init__(self, cell_index, richness, neighbors):
        self.cell_index = cell_index
        self.richness = richness
        self.neighbors = neighbors

class Tree:
    def __init__(self, cell_index, size, is_mine, is_dormant):
        self.cell_index = cell_index
        self.size = size
        self.is_mine = is_mine
        self.is_dormant = is_dormant

class ActionType(Enum):
    WAIT = "WAIT"
    SEED = "SEED"
    GROW = "GROW"
    COMPLETE = "COMPLETE"

class Action:
    def __init__(self, type, target_cell_id=None, origin_cell_id=None):
        self.type = type
        self.target_cell_id = target_cell_id
        self.origin_cell_id = origin_cell_id
        self.fitness = 0

    def __str__(self):
        if self.type == ActionType.WAIT:
            return 'WAIT'
        elif self.type == ActionType.SEED:
            return f'SEED {self.origin_cell_id} {self.target_cell_id}'
        else:
            return f'{self.type.name} {self.target_cell_id}'
    
    def score(self, game):
        if self.type == ActionType.WAIT:
            return 110 + game.count[0] * 20 + 1 * (2 + game.day - game.my_sun)
        if self.type == ActionType.SEED:
            if game.day > 18 and game.count[0] > 0:
                return 0
            return 100 + game.board[self.target_cell_id].richness * 10 - game.board[self.origin_cell_id].richness
        if self.type == ActionType.GROW:
            if game.day > 22:
                return 0
            return 200 + game.board[self.target_cell_id].richness + game.trees[self.target_cell_id].size - game.count[game.trees[self.target_cell_id].size+1]
        return game.day * 11 + game.board[self.target_cell_id].richness + max(0, game.opponent_score - game.my_score) * 7
            
    
    @staticmethod
    def parse(action_string):
        split = action_string.split(' ')
        if split[0] == ActionType.WAIT.name:
            return Action(ActionType.WAIT)
        elif split[0] == ActionType.SEED.name:
            return Action(ActionType.SEED, int(split[2]), int(split[1]))
        elif split[0] == ActionType.GROW.name:
            return Action(ActionType.GROW, int(split[1]))
        elif split[0] == ActionType.COMPLETE.name:
            return Action(ActionType.COMPLETE, int(split[1]))

class Game:
    def __init__(self):
        self.day = 0
        self.sun_direction = 0
        self.next_sun_direction = 1
        self.inv_sun_direction = 3
        self.inv_next_sun_direction = 4
        self.nutrients = 0
        self.board = {}
        self.trees = {}
        self.possible_actions = []
        self.my_sun = 0
        self.my_score = 0
        self.opponents_sun = 0
        self.opponent_score = 0
        self.opponent_is_waiting = 0
        self.count = {}
        
    def set_day(self, day):
        self.day = day
        self.sun_direction = day % 6
        self.next_sun_direction = (day + 1) % 6
        self.inv_sun_direction = (day + 3) % 6
        self.inv_next_sun_direction = (day + 4) % 6

    def print_actions(self):
        [print(tree.cell_index, file=sys.stderr, flush=True) for tree in self.trees]
        [print(action, file=sys.stderr, flush=True) for action in self.possible_actions]

    def compute_next_action(self):
        # if len(self.trees) == 0 or self.my_sun < 4:
            # return "WAIT"

        # self.trees.sort(key=lambda tree: self.board[tree.cell_index].richness if tree.is_mine else 0, reverse=True)
        # return "COMPLETE " + str(self.trees[0].cell_index)
        
        self.count = [0, 0, 0, 0]
        for tree_index in self.trees:
            tree = self.trees[tree_index]
            if tree.is_mine:
                self.count[tree.size] = self.count[tree.size] + 1
        # [print(str(count), file=sys.stderr, flush=True) for count in self.count]
        
        # for action in self.possible_actions:
            # self.estimate_action(action)
            
        return self.choose_best_action()
    
    def estimate_action(self, action):
        print("Action", action, file=sys.stderr, flush=True)
        trees = self.trees.copy()
        if action.type == ActionType.COMPLETE:
            del trees[action.target_cell_id]
            action.fitness = self.nutrients + 2**(self.board[action.target_cell_id].richness - 1) - 4/3
            
        elif action.type == ActionType.GROW:
            tree = trees[action.target_cell_id]
            trees[action.target_cell_id] = Tree(tree.cell_index, tree.size, tree.is_mine, tree.is_dormant)
            action.fitness = - (3 * tree.size + 1 + self.count[tree.size + 1]) / 3
        
        elif action.type == ActionType.SEED:
            action.fitness = - self.count[0] / 3
        
        action.fitness = action.fitness + self.compute_fitness(trees)
        
    def compute_fitness(self, trees):
        fitness = 0
        for cell_index in self.board:
            fitness_cell = self.compute_fitness_cell(cell_index, trees)
            # print(str(cell_index), str(fitness_cell), file=sys.stderr, flush=True)
            fitness = fitness + fitness_cell
            
        # print("Total Fitness", str(fitness), file=sys.stderr, flush=True)
        return fitness
            
    def compute_fitness_cell(self, cell_index, trees):
        tree = trees.get(cell_index)
        if tree == None:
            return 0
        
        current_cell_index = cell_index
        for distance in range(1, 4):
            neighbor_index = self.board[current_cell_index].neighbors[self.inv_next_sun_direction]
            if neighbor_index == -1:
                break
            
            neighbor_tree = trees.get(neighbor_index)
            if neighbor_tree != None and neighbor_tree.size >= tree.size and neighbor_tree.size >= distance:
                return 0
            
            current_cell_index = neighbor_index
                
        return tree.size / 3 * (1 if tree.is_mine else -1)
        
    def choose_best_action(self):
        self.possible_actions.sort(key=methodcaller('score', self), reverse=True)
        # [print(str(action), file=sys.stderr, flush=True) for action in self.possible_actions]
        return self.possible_actions[0]
        

number_of_cells = int(input())
game = Game()
for i in range(number_of_cells):
    cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    game.board[cell_index] = Cell(cell_index, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5])

while True:
    start = time.time_ns()
    game.set_day(int(input()))
    game.nutrients = int(input())
    sun, score = [int(i) for i in input().split()]
    game.my_sun = sun
    game.my_score = score
    opp_sun, opp_score, opp_is_waiting = [int(i) for i in input().split()]
    game.opponent_sun = opp_sun
    game.opponent_score = opp_score
    game.opponent_is_waiting = opp_is_waiting
    number_of_trees = int(input())
    game.trees.clear()
    for i in range(number_of_trees):
        inputs = input().split()
        cell_index = int(inputs[0])
        size = int(inputs[1])
        is_mine = inputs[2] != "0"
        is_dormant = inputs[3] != "0"
        game.trees[cell_index] = Tree(cell_index, size, is_mine == 1, is_dormant)

    number_of_possible_actions = int(input())
    game.possible_actions.clear()
    for i in range(number_of_possible_actions):
        possible_action = input()
        game.possible_actions.append(Action.parse(possible_action))
        
    print(game.compute_next_action())