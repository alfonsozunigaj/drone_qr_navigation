import csv
import json


def get_navigation_instructions_from_csv(*args):
    file_name = "InputFileManager/instructions.csv" if not args else args[0]
    csv_file = open(file_name, mode="r", encoding="utf-8")
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    instructions = {}
    for row in csv_reader:
        instructions[row[0]] = [{"roll": row[1],
                                 "pitch": row[2],
                                 "yaw": row[3],
                                 "v_move": row[4],
                                 "duration": row[5]
                                 }]
    return instructions


def get_navigation_instructions_from_json(*args):
    file_name = "InputFileManager/instructions.json" if not args else args[0]
    json_file = open(file_name, mode="r", encoding="utf-8")
    instructions = json.loads(json_file.read())
    return instructions


if __name__ == '__main__':
    print (get_navigation_instructions_from_csv())
    print (get_navigation_instructions_from_json())
