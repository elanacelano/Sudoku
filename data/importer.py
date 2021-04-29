"""
Used to import .csv files into board classesto be played.
"""
import os
import csv
import sys
sys.path.append('..')
from components.board import Board

def parse_csv(file_path):
    """
    Parses csv data.
    """
    board=[[None for i in range(0,9)] for j in range(0,9)]
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row_num, row in enumerate(csv_reader):
            for col_num, value in enumerate(row):
                print(value)
                print(type(value))

def load_file():
    """
    Takes a csv file path and returns a Board Class Game
    """
    directory = "./boards"
    for root, dirs, files in os.walk(directory, topdown=False):
        for board_file in files:
            file_path = root+'/'+board_file
            parse_csv(file_path)


if __name__ == "__main__":
    print(f"running")
    load_file()