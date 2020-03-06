import click
from utilities.db_setup import DbSetup

@click.group()
def cli():
  pass

@click.command()
@click.option('--env', default="development", help="""
  Specify the environment to set up a database for, 
  valid options are development, production""")
def dbsetup(env):
  DbSetup(env)

cli.add_command(dbsetup)

if __name__ == "__main__":
  cli()