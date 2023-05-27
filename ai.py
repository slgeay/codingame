from enum import IntEnum
from heapq import heappop, heappush
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
        self.paths_from_base = {}

    def initialize(self):
        # Read initial game state
        number_of_cells = int(input())
        for i in range(number_of_cells):
            cell_info = list(map(int, input().split()))
            self.map[i] = {
                "type": cell_info[0],
                "resources": cell_info[1],
                "neigh": cell_info[2:8],
            }
            if cell_info[0] == Type.CRYSTAL:
                self.cells_with_crystals.append(i)
            elif cell_info[0] == Type.EGG:
                self.cells_with_eggs.append(i)

        _ = int(input())
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
        self.paths_from_base = {}

        # Read turn info
        for i in range(len(self.map)):
            cell_info = list(map(int, input().split()))
            self.map[i]["resources"] = cell_info[0]
            self.map[i]["myAnts"] = cell_info[1]
            self.map[i]["oppAnts"] = cell_info[2]
            self.total_resources += cell_info[0]
            self.total_my_ants += cell_info[1]
            if self.map[i]["type"] == Type.CRYSTAL and cell_info[0] > 0:
                self.cells_with_crystals.append(i)
            elif self.map[i]["type"] == Type.EGG and cell_info[0] > 0:
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
        resource_cells.sort(
            key=lambda cell: min(
                self.calculate_priority(base, cell) for base in self.bases
            )
        )

        remaining_ants = self.total_my_ants
        max_paths = remaining_ants // 10
        path_count = 0

        for cell in resource_cells:
            if path_count >= max_paths:
                break

            # Find the closest base for each cell
            closest_base, shortest_path = self.find_closest_base(cell)
            path_without_beacon = [
                cell for cell in shortest_path if cell not in beacons
            ]

            # Only continue if we have enough ants to create a valid chain
            if remaining_ants < len(path_without_beacon):
                continue

            paths.append(shortest_path)
            strength = self.calculate_strength(cell)
            for cell in shortest_path:
                beacons[cell] = max(beacons.get(cell, 0), strength)
            remaining_ants -= len(path_without_beacon)

            path_count += 1

        return paths, beacons

    def find_closest_base(self, cell):
        closest_base = None
        shortest_path = []
        shortest_distance = float("inf")

        for base in self.bases:
            path = self.calculate_shortest_path(base, cell)
            if len(path) < shortest_distance:
                closest_base = base
                shortest_path = path
                shortest_distance = len(path)

        return closest_base, shortest_path

    def calculate_path_resources(self, path, t):
        return sum(
            self.map[cell]["resources"] for cell in path if self.map[cell]["type"] == t
        )

    def calculate_priority(self, base, cell):
        # Calculate path and its properties
        path = self.calculate_shortest_path(base, cell)
        total_eggs = self.calculate_path_resources(path, Type.EGG)
        total_crystals = self.calculate_path_resources(path, Type.CRYSTAL)
        return -(100 * total_eggs + total_crystals) / len(path) ** 4

    def calculate_shortest_path(self, start, end):
        # Get the precomputed path from start to end
        paths_from_start = self.precalculate_shortest_path(start)
        return paths_from_start.get(end, [])

    def precalculate_shortest_path(self, start):
        if start in self.paths_from_base:
            return self.paths_from_base[start]

        # Initialize the priority queue with the start cell
        queue = [(0, start)]  # (distance, cell)

        # Initialize the distances with a high value
        distances = [float("inf")] * len(self.map)
        distances[start] = 0

        # Initialize the previous cell path
        previous_cells = [None] * len(self.map)
        paths = {}  # To store paths from start to every other cell

        while queue:
            # Get the cell with the smallest known distance from the start
            current_distance, current_cell = heappop(queue)
            # Loop through each neighbour of the current cell
            for neighbour in self.map[current_cell]["neigh"]:
                # If the neighbour cell doesn't exist, skip
                if neighbour == -1:
                    continue

                # Calculate the distance to the neighbour cell, decreasing it if the cell has resources
                distance = current_distance + 1  # Each move costs 1
                if self.map[neighbour]["resources"] > 0:
                    ratio = self.map[neighbour]["resources"] / self.total_resources
                    if self.map[neighbour]["type"] == Type.CRYSTAL:
                        distance -= ratio / self.total_resources
                    elif self.map[neighbour]["type"] == Type.EGG:
                        distance -= ratio / self.total_my_ants

                # If this path to the neighbour cell is shorter, update our data
                if distance < distances[neighbour]:
                    distances[neighbour] = distance
                    previous_cells[neighbour] = current_cell
                    heappush(queue, (distance, neighbour))

            # If we're here, it means we've finished checking all neighbours of current_cell,
            # So we can create the shortest path from start to current_cell
            path = []
            temp_cell = current_cell
            while temp_cell is not None:
                path.append(temp_cell)
                temp_cell = previous_cells[temp_cell]
            path.reverse()
            paths[current_cell] = path

        self.paths_from_base[start] = paths  # Store all paths from this start node
        return paths

    def calculate_strength(self, cell):
        return 1


if __name__ == "__main__":
    game = Game()
    game.initialize()
    while True:
        game.play_turn()
