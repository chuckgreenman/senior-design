import click
from utilities.db_setup import DbSetup
from algorithm.action_graph import ActionGraph
from models.user import User

@click.group()
def cli():
  pass

@click.command()
@click.option('--env', default="development", help="""
  Specify the environment to set up a database for, 
  valid options are development, production""")
def dbsetup(env):
  DbSetup(env)

@click.command()
@click.argument('user_id')
def crawl(user_id):
  print("lets crawl user")
  u = User(user_id)
  u.crawl()

cli.add_command(dbsetup)
cli.add_command(crawl)

if __name__ == "__main__":
  cli()