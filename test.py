import pytest

from ai import Game, Type

@pytest.fixture
def game():
    game = Game()

    # Simplified map for testing purposes
    game.map = [
        {'neigh': [1, -1, -1, -1], 'resources': 0, 'type': Type.EMPTY, 'myAnts': 0, 'oppAnts': 0},  # Cell 0 (base)
        {'neigh': [0, 2, -1, -1], 'resources': 10, 'type': Type.CRYSTAL, 'myAnts': 0, 'oppAnts': 0},  # Cell 1
        {'neigh': [1, 3, -1, -1], 'resources': 5, 'type': Type.EGG, 'myAnts': 0, 'oppAnts': 0},  # Cell 2
        {'neigh': [2, -1, -1, -1], 'resources': 0, 'type': Type.EMPTY, 'myAnts': 0, 'oppAnts': 0},  # Cell 3
    ]
    game.bases = [0]
    game.cells_with_crystals = [1]
    game.cells_with_eggs = [2]
    game.total_resources = 15
    game.total_my_ants = 50

    return game

def test_shortest_path(game):
    # We expect the shortest path from cell 0 to cell 3 is [0, 1, 2, 3]
    assert game.calculate_shortest_path(0, 3) == [0, 1, 2, 3]

def test_no_path(game):
    game.map = [
        {'neigh': [1, -1, -1, -1], 'resources': 0, 'type': Type.EMPTY},  # Cell 0
        {'neigh': [0, -1, -1, -1], 'resources': 0, 'type': Type.EMPTY},  # Cell 1
        {'neigh': [-1, -1, -1, -1], 'resources': 0, 'type': Type.EMPTY},  # Cell 2
        {'neigh': [-1, -1, -1, -1], 'resources': 0, 'type': Type.EMPTY},  # Cell 3
    ]

    # We expect that there is no path from cell 0 to cell 3
    assert game.calculate_shortest_path(0, 3) == []

def test_create_beacon_paths(game):
    paths, beacons = game.create_beacon_paths()

    assert paths == [[0, 1, 2], [0, 1]]
    assert beacons == {0: 1, 1: 1, 2: 1}

def test_generate_actions(game):
    beacons = {0: 1, 1: 2, 2: 3}
    actions = game.generate_actions(beacons)
    assert actions == ["BEACON 0 1", "BEACON 1 2", "BEACON 2 3"]

def test_find_closest_base(game):
    closest_base, shortest_path = game.find_closest_base(2)
    assert closest_base == 0
    assert shortest_path == [0, 1, 2]

def test_calculate_path_resources(game):
    path = [0, 1, 2]
    resources = game.calculate_path_resources(path, Type.CRYSTAL)
    assert resources == 10

def test_calculate_priority(game):
    priority1 = game.calculate_priority(0, 1)
    priority2 = game.calculate_priority(0, 2)

    assert priority1 == -0.625
    assert priority2 == -6.296296296296297
