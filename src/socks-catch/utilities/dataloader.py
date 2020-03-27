import os
import binascii
import zipfile

from models.activity import Activity
from utilities.db_interact import DbInteract

activity_types = ["comment", "link"]

class DataLoader:
  def __init__(self, path, act_type):
    if not os.path.exists(path):
      raise Exception("Hmm. We couldn't find that path")
    else:
      self.verify_activity_type(act_type)
      self.verify_dir_structure(path)
      self.load_activity(path, act_type)

  def verify_dir_structure(self, path):
    for file in os.listdir(path):
      if not self.is_gz_file(os.path.join(path, file)):
        raise Exception("Invalid file type detected", file)

  def verify_activity_type(self, act_type):
    if act_type in activity_types:
      return True
    else:
      raise Exception("Invalid activity type")

  def is_gz_file(self, file):
    with open(file, 'rb') as test_f:
      return os.path.isdir(file) or binascii.hexlify(test_f.read(2)) == b'1f8b'

  def load_activity(self, path, act_type):
    files_to_import = os.listdir(path)
    file_count = len(files_to_import)

    for file_num, file_name in enumerate(files_to_import):
      print("Importing file", file_num+1, "of", file_count, file_name)
      self.import_file(path, file_name, act_type)

  def import_file(self, path, file_name, act_type):
    os.mkdir(os.path.join(path, "working_directory"))

    with zipfile.ZipFile(os.path.join(path, file_name)) as zip_ref:
      zip_ref.extractall(os.path.join(path, "working_directory", file_name))

    with open(os.join.path(path, "working_directory", file_name)) as activity_file:
      for line_number, line in activity_file:
        print(line_number, line)
