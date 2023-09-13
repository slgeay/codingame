from json import dumps, loads
from typing import List


def best_remaining_mutant(mutant_scores: dict, threshold: int) -> str:
    '''

    Args:

        - mutant_scores (dict): The score corresponding to each mutant
        - threshold (int): The score threshold above which mutants should be ignored

    Returns:


    '''
    candidates = {mutant:score for mutant,score in mutant_scores.items() if score <= threshold} 
    return max(candidates, key=candidates.get)

# Ignore and do not change the code below


def try_solution(output: str):
    '''
    Try a solution

    Args:

        - str (str): 
    '''
    json = output
    print("" + dumps(json, separators=(',', ':')))

def main():
    res = best_remaining_mutant(
        loads(input()),
        loads(input())
    )
    try_solution(res)


if __name__ == "__main__":
    main()
# Ignore and do not change the code above
