import subprocess
from random import randint

import click
from ai import SYNAPSES_COUNT, GreenCircleAI
from genetic_algorithm import GENE_MAX, GENE_MIN, GreenCircleGeneticAlgorithm


@click.group()
def main():
    pass


@main.command()
def hello() -> None:
    """Show a little welcome message!"""
    print("Hello ! :wave:")


@main.command()
def launch() -> None:
    """Test to launch the Game Engine"""
    result = subprocess.run(
        [
            "/usr/lib/jvm/java-8-openjdk-amd64/bin/java",
            "-cp",
            "cp_7wdcdfymzs7kpssaoh0wot2cw.jar",
            "SkeletonMain",
            "Toto",
            "Titi",
        ],
        stdout=subprocess.PIPE,
    )
    print(result)
    # score = int(result.stdout.decode('utf-8').splitlines()[-1])
    # print(score)
    # with open('log.txt', 'w') as f:
    #     f.write("\n".join(result.stdout.decode('utf-8').splitlines()[:-1]))


@main.command()
def compete() -> None:
    """Launch the competition"""
    GreenCircleGeneticAlgorithm().run()


@main.command()
def test() -> None:
    """Test to create a AI"""
    GreenCircleAI([randint(GENE_MIN, GENE_MAX) for _ in range(SYNAPSES_COUNT)])
