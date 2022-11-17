import csv

csv_file = open('results\\astarcsv.csv', 'a+')
with open('results\\AStarRuns.txt', 'r') as text_file:
    for line in text_file:
        line = line.rstrip()
        text = line.split(' - ')
        real_cost, huristic_cost = text[1], text[2]
        to_write = real_cost + ', ' + huristic_cost + '\n'
        csv_file.write(to_write)
