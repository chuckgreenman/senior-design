import click
from utils.parse import Parse 

@click.group()
def cli():
    pass

@click.command()
@click.option('--path', default=None, help="location of raw csv data")
def parse(path):
    """Decompose raw CSV data into graph elements."""
    p = Parse(data_path=path)
    p.start()

cli.add_command(parse)

if __name__ == '__main__':
    cli()
