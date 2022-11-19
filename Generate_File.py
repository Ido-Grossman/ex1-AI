# Ido Grossman 208985424
from main import find_rout, idastar_algo
from sys import argv
import csv
import ways


def draw_graph(path):
    import ways.draw
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError('Please install matplotlib:  http://matplotlib.org/users/installing.html#windows')
    plt.axis('equal')
    ways.draw.plot_path(roads, path)
    plt.show()


def calc_times():
    # The problems to check
    problems = [(76280, 61948), (207900, 207905), (295088, 295091), (376201, 376202), (425712, 425721), (476204, 476215),
         (567140, 567155), (617256, 617259), (681216, 681221), (572770, 2820)]
    # Activates all the algorithm on the problems to check
    for source, target in problems:
        print("ucs:", end=' ')
        find_rout(source, target, 'ucs', roads)
        print("astar:", end=' ')
        find_rout(source, target, 'astar', roads)
        print("idastar:", end=' ')
        path = idastar_algo(source, target, roads)
        # Draw a graph based on the idastar results.
        draw_graph(path)


def generate_file():
    # Open the mode name +Runs.txt file in the results folder
    file_export = open('results\\' + mode + 'Runs.txt', 'a+')
    # Open the problems csv file.
    with open('ways\\problems.csv') as csv_file:
        # Reads the problems csv
        csv_reader = csv.reader(csv_file, delimiter=',')
        not_row = 0
        # If there were 2 blank rows in a row, It finishes reading
        for row in csv_reader:
            if not row:
                not_row += 1
                continue
            if not_row >= 2:
                break
            not_row = 0
            # Sets the source and target junctions
            source, target = int(row[0]), int(row[1])
            # Makes the line out of the path, cost and if it's astar, The huristic cost as well
            path, cost, huristic_cost = find_rout(source, target, mode.lower(), roads)
            line = (' '.join(str(j) for j in path)) + ' - ' + str(cost)
            if mode == 'ASTAR':
                line += ' - ' + str(huristic_cost)
            line += '\n'
            # Write to the file.
            file_export.write(line)
    file_export.close()


if __name__ == '__main__':
    # Gets the mode of the file: times, UCS, ASTAR and load the roads
    mode = argv[1]
    roads = ways.load_map_from_csv()
    if mode == 'times':
        calc_times()
    else:
        generate_file()
