import csv
import os
import gzip
import sqlite3

def unzip_file(file_path, sqlite_database_name, table_name):
  with gzip.open(file_path, 'rt') as f:
    csv_reader = csv.reader(f)
    columns = next(csv_reader)
    print(file_path)

    cursor = create_connection(sqlite_database_name)
    next(csv_reader)
    for i, row in enumerate(csv_reader):
      placeholder = ', '.join(['?']*len(row))
      sql = "INSERT INTO " + table_name + " (" + ', '.join('"' + item + '"' for item in columns) + ") VALUES (" + placeholder + ");"
      cursor.execute(sql, tuple(row))


def iterate_files(directory, file_listing, sqlite_database_name, table_name):
  for file in file_listing:
    unzip_file(directory + '/' + file, sqlite_database_name, table_name)


def create_tables(sqlite_database_name):
  cursor = create_connection(sqlite_database_name)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS comments (
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
    retrieved_on INTEGER,
    controversiality INTEGER,
    ups INTEGER,
    gilded INTEGER,
    subreddit TEXT,
    distinguished TEXT,
    author_flair_css_class TEXT
  )""")

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
    created_utc INTEGER,
    subreddit TEXT,
    author TEXT,
    domain TEXT,
    URL TEXT,
    num_comments INTEGER,
    score INTEGER,
    ups INTEGER,
    downs INTEGER,
    title TEXT,
    selftext TEXT,
    saved BOOLEAN,
    id TEXT PRIMARY KEY,
    from_kind TEXT,
    gilded INTEGER,
    stickied BOOLEAN,
    retrieved_on INTEGER,
    over_18 BOOLEAN,
    thumbnail TEXT,
    subreddit_id TEXT,
    hide_score BOOLEAN,
    link_flair_css_class TEXT,
    author_flair_css_class TEXT,
    archived BOOLEAN,
    is_self BOOLEAN,
    `from` TEXT,
    `from_id` TEXT,
    permalink TEXT,
    name TEXT,
    author_flair_text TEXT,
    quarantine BOOLEAN,
    link_flair_text TEXT,
    distinguished TEXT
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

  iterate_files('Comments', comment_files, sqlite_database_name, "comments")
  iterate_files('Posts', post_files, sqlite_database_name, "posts")

main()
