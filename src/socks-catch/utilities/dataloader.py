import os
import binascii
import gzip

from models.activity import Activity
from utilities.db_interact import DbInteract

activity_types = ["comment", "link"]

class DataLoader:
  def __init__(self, path, act_type):
    if not os.path.exists(path):
      raise Exception("Hmm. We couldn't find that path")
    else:
      self.verify_activity_type(act_type)
      self.load_activity(path, act_type)

  def verify_activity_type(self, act_type):
    if act_type in activity_types:
      return True
    else:
      raise Exception("Invalid activity type")

  def is_gz_file(self, file):
    with open(file, 'rb') as test_f:
      return binascii.hexlify(test_f.read(2)) == b'1f8b'

  def load_activity(self, path, act_type):
    files_to_import = os.listdir(path)
    file_count = len(files_to_import)

    for file_num, file_name in enumerate(files_to_import):
      print("Importing file", file_num+1, "of", file_count, file_name)
      self.import_file(path, file_name, act_type)

  def index_by_field_name(self, needle, haystack):
    for i, element in enumerate(haystack):
      if element == needle:
        return i
    return None

  def import_file(self, path, file_name, act_type):
    field_list = None

    if self.is_gz_file(os.path.join(path, file_name)):
      with gzip.open(os.path.join(path, file_name), 'rb') as activity_file:
        self.read_lines(activity_file)
    else:
      with open(os.path.join(path, file_name)) as activity_file:
        self.read_lines(activity_file, act_type)

  def read_lines(self, activity_file, act_type):
    db = DbInteract()
    activity = []

    for line_number, line in enumerate(activity_file):
      if line_number == 0:
        if isinstance(line, str):
          field_list = line.split(",")
          field_list = [field.strip("\n") for field in field_list]
        else:
          field_list = line.decode('utf-8').split(",")
          field_list = [field.strip("\n") for field in field_list]
        continue

      if isinstance(line, str):
        line = line.split(",")
      else:
        line = line.decode('utf-8').split(",")

      if len(field_list) != len(line):
        continue

      if act_type == 'comment':
        subreddit_id_index = self.index_by_field_name("subreddit", field_list)
        user_id_index = self.index_by_field_name("author", field_list)
        created_utc_index = self.index_by_field_name("created_utc", field_list)
        page_id_index = self.index_by_field_name("link_id", field_list)
        if line[user_id_index] != "[deleted]":
          a = (line[page_id_index][-6:], line[subreddit_id_index], line[user_id_index], 'comment', line[created_utc_index])
          activity.append(a)
      else:
        subreddit_index = self.index_by_field_name("subreddit", field_list)
        user_id_index = self.index_by_field_name("author", field_list)
        created_utc_index = self.index_by_field_name("created_utc", field_list)
        page_id_index = self.index_by_field_name("id", field_list)
        if line[user_id_index] != "[deleted]":
          a = (line[page_id_index], line[subreddit_index], line[user_id_index], 'link', line[created_utc_index])
          activity.append(a)
      
    db.add_activity_records(activity)

