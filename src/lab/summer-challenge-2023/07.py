from json import dumps, loads

def shortest_merge_recursive(a, b, memo=None):
    if memo is None:
        memo = {}

    if (a, b) in memo:
        return memo[(a, b)]

    if not a:
        return b
    if not b:
        return a

    if a[0] == b[0]:
        merged = a[0] + shortest_merge_recursive(a[1:], b[1:], memo)
    else:
        merge_a = a[0] + shortest_merge_recursive(a[1:], b, memo)
        merge_b = b[0] + shortest_merge_recursive(a, b[1:], memo)
        merge_both = a[0] + b[0] + shortest_merge_recursive(a[1:], b[1:], memo)

        merged = min([merge_a, merge_b, merge_both], key=len)

    memo[(a, b)] = merged
    return merged

def mix_wishes(wish_a: str, wish_b: str) -> str:
    '''

    Args:

        - wish_a (str): The first wish.
        - wish_b (str): The second wish.

    Returns:

        The hybrid wish you created.
    '''

    return shortest_merge_recursive(wish_a, wish_b)

# Ignore and do not change the code below


def try_solution(mixed_ab: str):
    '''
    Try a solution

    Args:

        - str (str): The hybrid wish you created.
    '''
    json = mixed_ab
    print("" + dumps(json, separators=(',', ':')))

def main():
    res = mix_wishes(
        loads(input()),
        loads(input())
    )
    try_solution(res)


if __name__ == "__main__":
    main()
# Ignore and do not change the code above
