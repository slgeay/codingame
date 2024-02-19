from json import dumps, loads
from typing import List


def find_correct_path(instructions: str, target: List[int], obstacles: List[List[int]]) -> str:
    '''

    Args:

        - instructions (str): The compressed instructions as memorized by the mutant.
        - target (List[int]): The coordinates (x, y) of the target.
        - obstacles (List[List[int]]): An array containing all (x, y) coordinates of obstacles.

    Returns:

        A string respecting the given format to fix the mutant's path.
    '''
    memo = {}
    fib_memo = {}
    
    # Generate Fibonacci numbers up to the length of instructions
    fib_numbers = [0, 1]
    while fib_numbers[-1] + fib_numbers[-2] <= len(instructions):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
    
    def compute_path(pos: (int, int), angle: (int, int), remaining_instructions: str) -> (int, int):
        '''Computes the final position given a current position, angle, and set of remaining instructions.'''
        original_pos, original_angle, original_instructions = pos, angle, remaining_instructions
        
        while remaining_instructions:
            if (pos, remaining_instructions) in memo:
                return memo[(pos, remaining_instructions)]

            if (pos, len(remaining_instructions)) in fib_memo:
                pos, angle = fib_memo[(pos, len(remaining_instructions))]
                remaining_instructions = ""
                continue

            if list(pos) in obstacles:
                memo[(original_pos, original_instructions)] = None
                return None

            fib_size = max([f for f in fib_numbers if f <= len(remaining_instructions)])

            sub_instructions = remaining_instructions[:fib_size]
            for instruction in sub_instructions:
                if instruction == "F":
                    pos = (pos[0] + angle[0], pos[1] + angle[1])
                elif instruction == "B":
                    pos = (pos[0] - angle[0], pos[1] - angle[1])
                elif instruction == "L":
                    angle = (-angle[1], angle[0])
                elif instruction == "R":
                    angle = (angle[1], -angle[0])

            if fib_size == len(remaining_instructions):
                fib_memo[(original_pos, len(original_instructions))] = (pos, angle)

            remaining_instructions = remaining_instructions[fib_size:]

        memo[(original_pos, original_instructions)] = pos
        return pos
    
    # Compute and cache the position and angle for each instruction up to i
    positions = [(0, 0)]
    angles = [(1, 0)]
    obstacle_index = len(instructions) # Assuming no obstacle is encountered initially
    for idx, instr in enumerate(instructions):
        new_pos, new_angle = positions[-1], angles[-1]
        if instr == "F":
            new_pos = (new_pos[0] + new_angle[0], new_pos[1] + new_angle[1])
        elif instr == "B":
            new_pos = (new_pos[0] - new_angle[0], new_pos[1] - new_angle[1])
        elif instr == "L":
            new_angle = (-new_angle[1], new_angle[0])
        elif instr == "R":
            new_angle = (new_angle[1], -new_angle[0])
        positions.append(new_pos)
        angles.append(new_angle)
        
        if list(new_pos) in obstacles:
            obstacle_index = idx
            break
    
    for i, instr in enumerate(instructions[:obstacle_index]):
        for command in ["F", "B", "L", "R"]:
            if instr == command:
                continue

            new_instructions = command + instructions[i+1:]
            pos = compute_path(positions[i], angles[i], new_instructions)

            if pos is not None and target == list(pos):
                commands = {'F':'FORWARD', 'B':'BACK', 'L':'TURN LEFT', 'R':'TURN RIGHT'}
                return f"Replace instruction {i+1} with {commands[command]}"
            
    return None
            
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
        loads(input()),
        loads(input())
    )
    try_solution(res)


if __name__ == "__main__":
    main()
# Ignore and do not change the code above
