import subprocess
from random import randint

import click

from ai import WEIGHTS_COUNT, Spring2023AntsAI
from genetic_algorithm import (
    AI,
    GENE_MAX,
    GENE_MIN,
    JAR,
    MAIN,
    Spring2023AntsGeneticAlgorithm,
)


@click.group()
def main():
    pass


@main.command()
def launch() -> None:
    """Test to launch the Game Engine"""
    print("Launching the Game Engine...")
    result = subprocess.run(
        [
            "java",
            "-cp",
            JAR,
            MAIN,
            AI,
            "X",
            AI,
            "Y",
        ],
        stdout=subprocess.PIPE,
    )
    print(result.stdout.decode("utf-8"))


@main.command()
def compete() -> None:
    """Launch the competition"""
    Spring2023AntsGeneticAlgorithm().run()


@main.command()
def test() -> None:
    """Test to create AIs"""
    Spring2023AntsAI()
    Spring2023AntsAI([randint(GENE_MIN, GENE_MAX) for _ in range(WEIGHTS_COUNT)])


if __name__ == "__main__":
    main()
