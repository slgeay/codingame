import click

from app.ai import BaseGeneticAlgorithm


@click.group()
def main():
    pass


@main.command()
def hello() -> None:
    """Show a little welcome message!"""
    print("Hello ! :wave:")


@main.command()
def test() -> None:
    """Test something"""
    BaseGeneticAlgorithm(50, 50, 50, 0.1, 0.1).run()
