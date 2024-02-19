import pytest

from ai import Spring2023AntsAI, Type
from migration import add_zeros, process_content


@pytest.fixture
def ai():
    ai = Spring2023AntsAI()

    # Simplified map for testing purposes
    ai.map = [
        {
            "neigh": [1, -1, -1, -1],
            "resources": 0,
            "type": Type.EMPTY,
            "myAnts": 0,
            "oppAnts": 0,
        },  # Cell 0 (base)
        {
            "neigh": [0, 2, -1, -1],
            "resources": 10,
            "type": Type.CRYSTAL,
            "myAnts": 0,
            "oppAnts": 0,
        },  # Cell 1
        {
            "neigh": [1, 3, -1, -1],
            "resources": 5,
            "type": Type.EGG,
            "myAnts": 0,
            "oppAnts": 0,
        },  # Cell 2
        {
            "neigh": [2, -1, -1, -1],
            "resources": 0,
            "type": Type.EMPTY,
            "myAnts": 0,
            "oppAnts": 0,
        },  # Cell 3
    ]
    ai.bases = [0]
    ai.cells_with_crystals = [1]
    ai.cells_with_eggs = [2]
    ai.total_resources = 15
    ai.total_my_ants = 50

    return ai


def test_shortest_path(ai):
    # We expect the shortest path from cell 0 to cell 3 is [0, 1, 2, 3]
    assert ai.calculate_shortest_path(0, 3) == [0, 1, 2, 3]


def test_no_path(ai):
    ai.map = [
        {"neigh": [1, -1, -1, -1], "resources": 0, "type": Type.EMPTY},  # Cell 0
        {"neigh": [0, -1, -1, -1], "resources": 0, "type": Type.EMPTY},  # Cell 1
        {"neigh": [-1, -1, -1, -1], "resources": 0, "type": Type.EMPTY},  # Cell 2
        {"neigh": [-1, -1, -1, -1], "resources": 0, "type": Type.EMPTY},  # Cell 3
    ]

    # We expect that there is no path from cell 0 to cell 3
    assert ai.calculate_shortest_path(0, 3) == []


def test_create_beacon_paths(ai):
    paths, beacons = ai.create_beacon_paths()

    assert paths == [[0, 1, 2], [0, 1]]
    assert beacons == {0: 1, 1: 1, 2: 1}


def test_generate_actions(ai):
    beacons = {0: 1, 1: 2, 2: 3}
    actions = ai.generate_actions(beacons)
    assert actions == ["BEACON 0 1", "BEACON 1 2", "BEACON 2 3"]


def test_find_closest_base(ai):
    closest_base, shortest_path = ai.find_closest_base(2)
    assert closest_base == 0
    assert shortest_path == [0, 1, 2]


def test_calculate_path_resources(ai):
    path = [0, 1, 2]
    resources = ai.calculate_path_resources(path, Type.CRYSTAL)
    assert resources == 10


def test_calculate_priority(ai):
    priority1 = ai.calculate_priority(0, 1)
    priority2 = ai.calculate_priority(0, 2)

    assert priority1 == -0.625
    assert priority2 == -6.296296296296297


def test_add_zeros():
    assert add_zeros([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 0.0, 0.0]
    assert add_zeros([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 0.0, 0.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 0.0, 0.0]


def test_process_content():
    assert process_content("1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0") == "1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,0.0,0.0"
    assert process_content("1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0") == "1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,0.0,0.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0,0.0,0.0"

