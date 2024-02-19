from json import dumps, loads
from typing import List


def merge_files(file_contents: List[str]) -> str:
    '''

    Args:

        - file_contents (List[str]): A list of strings, where each string represents the contents of a file.

    Returns:

        The contents of the merged file.
    '''
    students = dict()
    for file in file_contents:
        for line in file.split("\n"):
            student = {name:value for name,value in (field.split("=") for field in line.split(";"))}
            name = student.pop("Name")
            if name in students:
                students[name].update(student)
            else:
                students[name] = student

    return "\n".join([f"Name={name};{''.join([f'{key}={value};' for key,value in sorted(student.items())])}"[:-1] for name,student in sorted(students.items())])

# Ignore and do not change the code below


def try_solution(merged_file: str):
    '''
    Try a solution

    Args:

        - str (str): The contents of the merged file.
    '''
    json = merged_file
    print("" + dumps(json, separators=(',', ':')))

def main():
    res = merge_files(
        loads(input())
    )
    try_solution(res)


if __name__ == "__main__":
    main()
# Ignore and do not change the code above
