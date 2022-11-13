from main import find_rout
import csv
import ways

ucsruns = open('results\\UCSRuns.txt', 'a+')
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
        path, cost = find_rout(source, target, 'ucs', roads)
        line = (' '.join(str(j) for j in path)) + ' - ' + str(cost) + '\n'
        ucsruns.write(line)
ucsruns.close()
