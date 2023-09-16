from json import dumps, loads
from typing import List


def find_correct_path(instructions: List[str], target: List[int]) -> str:
    '''

    Args:

        - instructions (List[str]): The list of instructions as memorized by the mutant.
        - target (List[int]): The coordinates (x, y) of the target.

    Returns:

        A string respecting the given format to fix the mutant's path.
    '''
    for i, instr in enumerate(instructions):
        for command in ["FORWARD", "BACK", "TURN LEFT", "TURN RIGHT"]:
            if instr == command:
                continue

            pos = (0, 0)
            angle = (1, 0)
            for j, instruction in enumerate(instructions):
                if j == i:
                    instruction = command

                if instruction == "FORWARD":
                    pos = (pos[0] + angle[0], pos[1] + angle[1])
                elif instruction == "BACK":
                    pos = (pos[0] - angle[0], pos[1] - angle[1])
                elif instruction == "TURN LEFT":
                    angle = (-angle[1], angle[0])
                elif instruction == "TURN RIGHT":
                    angle = (angle[1], -angle[0])
            
            if target == list(pos):
                return f"Replace instruction {i+1} with {command}"

# Ignore and do not change the code below


def try_solution(recipe: str):
    '''
    Try a solution

    Args:

        - str (str): A string respecting the given format to fix the mutant's path.
    '''
    json = recipe
    print("" + dumps(json, separators=(',', ':')))

def main():
    res = find_correct_path(
        loads(input()),
        loads(input())
    )
    try_solution(res)


if __name__ == "__main__":
    main()
# Ignore and do not change the code above
