import click

from app.ai import LanderGeneticAlgorithm, LanderSimulation


@click.group()
def main():
    pass


@main.command()
def hello() -> None:
    """Show a little welcome message!"""
    print("Hello ! :wave:")


@main.command()
def test_genetic() -> None:
    """Test something"""
    LanderGeneticAlgorithm(50, 50, 50, 0.1, 0.1).run()


@main.command()
def test_simulation() -> None:
    """Test something"""
    for _ in range(10):
        print(LanderSimulation())
