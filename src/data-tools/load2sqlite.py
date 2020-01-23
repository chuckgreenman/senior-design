import csv
import os
import gzip
import sqlite3

def unzip_file(file_path):
  with gzip.open(file_path, 'rt') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
      print(row)
      input()

def iterate_files(directory, file_listing):
  for file in file_listing:
    unzip_file(directory + '/' + file)


def create_tables(sqlite_database_name):
  cursor = create_connection(sqlite_database_name)
  cursor.execute("""
  CREATE TABLE comments (
    id TEXT PRIMARY KEY,
    body TEXT,
    score_hidden BOOLEAN,
    archived BOOLEAN,
    name TEXT,
    author TEXT,
    author_flair_text TEXT,
    downs INTEGER,
    created_utc INTEGER,
    subreddit_id TEXT,
    link_id TEXT,
    parent_id TEXT,
    score INTEGER,
    retrived_on INTEGER,
    contraversial INTEGER,
    gilded INTEGER,
    subreddit TEXT,
    distinguished TEXT,
    author_flair_css_class TEXT
  )""")

  cursor.execute("""
    CREATE TABLE posts (
    )""")


def create_connection(sqlite_database_name):
  connection = sqlite3.connect(sqlite_database_name)
  return connection.cursor()


sqlite_database_name = "default_name" 

def main():
  print("This script will create a sqlite database in the current directory.")
  print("Provide a name to continue > ")
  sqlite_database_name = input()

  create_tables(sqlite_database_name)

  comment_files = os.listdir("Comments")
  post_files = os.listdir("Posts")

  iterate_files('Comments', comment_files)
  iterate_files('Posts', post_files)

main()
