import click


@click.group()
def main():
    pass


@main.command()
def hello() -> None:
    """Show a little welcome message!"""
    print("Hello ! :wave:")
