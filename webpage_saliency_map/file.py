# coding: utf-8
import csv

class Csv:
  def __init__(self, file_path: str):
    self.file = open(file_path, 'w')
    self.writer = csv.writer(self.file)

  def writerow(self ,row):
    self.writer.writerow(row)

