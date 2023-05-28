from enum import IntEnum
from heapq import heappop, heappush
import math
import sys


WEIGHTS_COUNT = 8 * 12
DEFAULT_WEIGHTS = [
    0,0,0,0,0,0,0,0.1,100,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0  # noqa
]


def debug(s: str):
    print(s, file=sys.stderr, flush=True)


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


class Type(IntEnum):
    EMPTY = 0
    EGG = 1
    CRYSTAL = 2


class Spring2023AntsAI:
    def __init__(self, weights=DEFAULT_WEIGHTS):
        # Initialization
        self.map = {}
        self.bases = []
        self.opp_bases = []
        self.cells_with_crystals = []
        self.cells_with_eggs = []
        self.total_crystals = 0
        self.total_eggs = 0
        self.total_resources = 0
        self.total_my_ants = 0
        self.paths_from_base = {}
        self.weights = weights

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
                self.total_crystals += cell_info[0]
                self.cells_with_crystals.append(i)
            elif self.map[i]["type"] == Type.EGG and cell_info[0] > 0:
                self.total_eggs += cell_info[0]
                self.cells_with_eggs.append(i)

    def generate_actions(self, beacons):
        actions = []
        for cell, strength in beacons.items():
            actions.append(f"BEACON {cell} {strength}")
        return actions

    def compute_weighted_factor(self, i):
        # Initialize the inputs with various game state attributes
        inputs = [
            1,
            len(self.bases),
            len(self.cells_with_crystals),
            len(self.cells_with_eggs),
            self.total_crystals,
            self.total_eggs,
            self.total_resources,
            self.total_my_ants,
        ]
        # Multiply each input with a corresponding weight
        i *= len(inputs)
        return sum(self.weights[i + j] * x for j, x in enumerate(inputs))

    def ccwf(self, i, min, max):
        return clamp(self.compute_weighted_factor(i), min, max)

    def create_beacon_paths(self):
        paths = []
        beacons = {}
        resource_cells = self.cells_with_crystals + self.cells_with_eggs

        # Sort the resource cells by priority calculated using distance and resources
        resource_cells.sort(
            key=lambda cell: min(
                self.calculate_priority(base, cell) for base in self.bases
            )
        )

        remaining_ants = self.total_my_ants
        max_paths = math.floor(self.ccwf(0, 1, remaining_ants))
        path_count = 0

        for cell in resource_cells:
            # Check if the maximum path count has been reached
            if path_count >= max_paths:
                break

            # Find the closest base for each cell
            _, shortest_path = self.find_closest_base(cell)
            path_without_beacon = [
                cell for cell in shortest_path if cell not in beacons
            ]

            # Only continue if we have enough ants to create a valid chain
            if remaining_ants < len(path_without_beacon):
                continue

            # Update the paths and beacons with the shortest path and its strength
            paths.append(shortest_path)
            strength = self.calculate_strength(cell)
            for cell in shortest_path:
                beacons[cell] = max(beacons.get(cell, 0), strength)
            remaining_ants -= len(path_without_beacon)

            # Increase the path count
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
        # Calculate the shortest path from the base to the cell
        path = self.calculate_shortest_path(base, cell)
        
        # Calculate the total resources in the path
        total_eggs = self.calculate_path_resources(path, Type.EGG)
        total_crystals = self.calculate_path_resources(path, Type.CRYSTAL)

        # Return a priority value based on the resource totals and path length
        # The priority is calculated as the weighted sum of total eggs and crystals divided by the path length
        return -(
            self.ccwf(1, 0, 1000) * total_eggs + self.ccwf(2, 0, 100) * total_crystals
        ) / len(path) ** self.ccwf(3, 0, 10)

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
                    if self.map[neighbour]["type"] == Type.CRYSTAL:
                        distance -= clamp(
                            self.map[neighbour]["resources"]
                            * self.ccwf(4, 0, 10)
                            / self.ccwf(5, 1, 100)
                            / self.ccwf(6, 1, 100),
                            0,
                            0.99,
                        )
                    elif self.map[neighbour]["type"] == Type.EGG:
                        distance -= clamp(
                            self.map[neighbour]["resources"]
                            * self.ccwf(7, 0, 10)
                            / self.ccwf(8, 1, 100)
                            / self.ccwf(9, 1, 100),
                            0,
                            0.99,
                        )

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
        # Calculate the shortest path from the closest base to the cell
        _, shortest_path = self.find_closest_base(cell)
        
        # Calculate the strength of the path based on the distance and resources
        # The strength is calculated as a weighted product of resources and distance, clamped between 1 and 100
        distance = len(shortest_path)
        resources = self.map[cell]["resources"]
        return math.ceil(
            clamp(
                self.ccwf(10, 0, 10) * resources * distance ** self.ccwf(11, -2, 2),
                1,
                100,
            )
        )

    def read_weights(s: str):
        return [float(w) for w in s.split(",")]


if __name__ == "__main__":
    try:
        with open(sys.argv[1], "r") as f:
            s = f.read()
    except Exception:
        s = None
    
    if s:
        weights = Spring2023AntsAI.read_weights(s)
        ai = Spring2023AntsAI(weights)
    else:
        ai = Spring2023AntsAI()
    
    ai.initialize()
    while True:
        ai.play_turn()
