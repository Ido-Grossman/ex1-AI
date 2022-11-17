from main import find_rout
from sys import argv
import csv
import ways

mode = argv[1]
file_export = open('results\\' + mode + 'Runs.txt', 'a+')
roads = ways.load_map_from_csv()
with open('ways\\problems.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    not_row = 0
    for row in csv_reader:
        if not row:
            not_row += 1
            continue
        if not_row >= 2:
            break
        not_row = 0
        source, target = int(row[0]), int(row[1])
        path, cost, huristic_cost = find_rout(source, target, mode.lower(), roads)
        line = (' '.join(str(j) for j in path)) + ' - ' + str(cost)
        if huristic_cost != 0:
            line += ' - ' + str(huristic_cost)
        line += '\n'
        file_export.write(line)
file_export.close()
