import click
from utilities.db_setup import DbSetup
from algorithm.action_graph import ActionGraph
from algorithm.relationship_graph import RelationshipGraph
from utilities.dataloader import DataLoader
from utilities.db_interact import DbInteract
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
@click.option('--path', help="""
  Specify the directory where the baseline code is
  stored, this will kick off the import process.""")
@click.argument('act_type')
def importbaseline(path, act_type):
  DataLoader(path, act_type)

@click.command()
@click.argument('user_id')
def crawl(user_id):
  print("lets crawl user")
  u = User(user_id)
  u.crawl()

@click.command()
def refreshactiongraph():
  ActionGraph.refresh()
  print("Action Graph refreshed.")

@click.command()
def refreshrelationshipgraph():
  RelationshipGraph.refresh()
  print("Relationship Graph refreshed")

@click.command()
def crawlusermeta():
  db = DbInteract()
  unique_users = db.get_unique_users()
  for row in unique_users:
    u = User(row[0])
    u.pull_metadata()
    
  print("User metadata refreshed")

cli.add_command(dbsetup)
cli.add_command(importbaseline)
cli.add_command(crawl)
cli.add_command(refreshactiongraph)
cli.add_command(refreshrelationshipgraph)
cli.add_command(crawlusermeta)

if __name__ == "__main__":
  cli()
