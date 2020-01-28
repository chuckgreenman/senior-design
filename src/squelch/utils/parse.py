import os

class Parse:
  def __init__(self, data_path):
    self.data_path = data_path

  def start(self):
    print("Begining the parse process")
    self.validate_folder_structure()
    print("\t* Detected valid folder structure") 

  def validate_folder_structure(self):
  	if not os.path.isdir(self.data_path):
  		raise RuntimeError('Path provided is not a directory or does not exist')
