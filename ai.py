from enum import IntEnum
from heapq import heappop, heappush
import math
import sys

def debug(s):
    print(s, file=sys.stderr, flush=True)

class Type(IntEnum):
    EMPTY = 0
    EGG = 1
    CRYSTAL = 2

class Game:
    def __init__(self):
        # Initialization
        self.map = {}
        self.bases = []
        self.opp_bases = []
        self.cells_with_crystals = []
        self.cells_with_eggs = []
        self.total_resources = 0
        self.total_my_ants = 0

    def initialize(self):
        # Read initial game state
        number_of_cells = int(input())
        for i in range(number_of_cells):
            cell_info = list(map(int, input().split()))
            self.map[i] = {
                'type': cell_info[0],
                'resources': cell_info[1],
                'neigh': cell_info[2:8]
            }
            if cell_info[0] == Type.CRYSTAL:
                self.cells_with_crystals.append(i)
            elif cell_info[0] == Type.EGG:
                self.cells_with_eggs.append(i)
        
        number_of_bases = int(input())
        self.bases = list(map(int, input().split()))
        self.opp_bases = list(map(int, input().split()))

    def play_turn(self):
        self.read_turn_info()
        paths, beacons = self.create_beacon_paths()
        actions = self.generate_actions(beacons)

        # If no actions, wait
        if not actions:
            actions.append("WAIT")
        
        # Print actions
        print(";".join(actions))

    def read_turn_info(self):
        self.cells_with_crystals = []
        self.cells_with_eggs = []
        self.total_resources = 0
        self.total_my_ants = 0

        # Read turn info
        for i in range(len(self.map)):
            cell_info = list(map(int, input().split()))
            self.map[i]['resources'] = cell_info[0]
            self.map[i]['myAnts'] = cell_info[1]
            self.map[i]['oppAnts'] = cell_info[2]
            self.total_resources += cell_info[0]
            self.total_my_ants += cell_info[1]
            if self.map[i]['type'] == Type.CRYSTAL and cell_info[0] > 0:
                self.cells_with_crystals.append(i)
            elif self.map[i]['type'] == Type.EGG and cell_info[0] > 0:
                self.cells_with_eggs.append(i)

    def generate_actions(self, beacons):
        actions = []
        for cell, strength in beacons.items():
            actions.append(f"BEACON {cell} {strength}")
        return actions

    def create_beacon_paths(self):
        paths = []
        beacons = {}
        resource_cells = self.cells_with_crystals + self.cells_with_eggs
        resource_cells.sort(key=lambda cell: min(self.calculate_priority(base, cell) for base in self.bases))

        remaining_ants = self.total_my_ants
        for cell in resource_cells:
            for base in self.bases:
                path = self.calculate_shortest_path(base, cell)
                path_without_beacon = [cell for cell in path if cell not in beacons]
                # Only continue if we have enough ants to create a valid chain
                if remaining_ants < len(path_without_beacon):
                    break
                paths.append(path)
                strength = self.calculate_strength(cell)
                for cell in path:
                    beacons[cell] = max(beacons.get(cell, 0), strength)
                remaining_ants -= len(path_without_beacon)


        return paths, beacons

    def calculate_path_resources(self, path):
        return sum(self.map[cell]['resources'] for cell in path)

    def calculate_priority(self, base, cell):
        # Calculate path and its properties
        path = self.calculate_shortest_path(base, cell)
        total_resources = self.calculate_path_resources(path)
        average_resources_per_move = total_resources / len(path)
        ant_ratio = self.total_my_ants / (self.total_my_ants + total_resources)

        # Prioritize closer cells and cells where our ants are less numerous
        distance = len(path) or float('inf')
        priority = distance - average_resources_per_move * ant_ratio

        # Additional considerations
        if self.map[cell]['type'] == Type.EGG:
            egg_ratio = self.map[cell]['resources'] / self.total_my_ants
            priority -= average_resources_per_move * egg_ratio
        else:
            crystal_ratio = self.map[cell]['resources'] / self.total_resources
            priority -= average_resources_per_move * crystal_ratio

        return priority

    def calculate_shortest_path(self, start, end):
        # Initialize the priority queue with the start cell
        queue = [(0, start)]  # (distance, cell)

        # Initialize the distances with a high value
        distances = [float('inf')] * len(self.map)
        distances[start] = 0

        # Initialize the previous cell path
        previous_cells = [None] * len(self.map)

        while queue:
            # Get the cell with the smallest known distance from the start
            current_distance, current_cell = heappop(queue)

            # If we've reached the end cell, we're done
            if current_cell == end:
                break

            # Loop through each neighbour of the current cell
            for neighbour in self.map[current_cell]['neigh']:
                # If the neighbour cell doesn't exist, skip
                if neighbour == -1:
                    continue

                # Calculate the distance to the neighbour cell, decreasing it if the cell has resources
                distance = current_distance + 1  # Each move costs 1
                if self.map[neighbour]['resources'] > 0:
                    ratio = self.map[neighbour]['resources'] / self.total_resources
                    if self.map[neighbour]['type'] == Type.CRYSTAL:
                        distance -= ratio/self.total_resources
                    elif self.map[neighbour]['type'] == Type.EGG:
                        distance -= ratio/self.total_my_ants

                # If this path to the neighbour cell is shorter, update our data
                if distance < distances[neighbour]:
                    distances[neighbour] = distance
                    previous_cells[neighbour] = current_cell
                    heappush(queue, (distance, neighbour))

        # If we've reached the end cell, build and return the path
        if current_cell == end:
            path = []
            while current_cell is not None:
                path.append(current_cell)
                current_cell = previous_cells[current_cell]
            path.reverse()
            return path

        # If there's no path to the end cell, return an empty list
        return []

    def calculate_strength(self, cell):
        return 1

game = Game()
game.initialize()
while True:
    game.play_turn()
