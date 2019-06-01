import csv


def get_navigation_instructions(*args):
    file_name = "instructions.csv" if not args else args[0]
    csv_file = open(file_name, mode="r", encoding="utf-8")
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    instructions = {}
    for row in csv_reader:
        instructions[row[0]] = list(map(int, row[1:]))
    return instructions
