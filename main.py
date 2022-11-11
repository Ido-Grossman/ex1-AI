'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''
import ways


# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

def huristic_function(lat1, lon1, lat2, lon2):
    raise NotImplementedError


def find_ucs_rout(source, target):
    roads = ways.load_map_from_csv()
    closed = set()
    opened = [(roads[source], 0, 0)]
    path = []
    level = 0
    cost = 0
    while opened:
        opened.sort(key=lambda item: item[1])
        next_node = opened.pop(0)
        closed.add(next_node[0][0])
        if next_node[2] < level:
            path = path[0:level + 1]
        next_node = next_node[0]
        level += 1
        path.append(next_node[0])
        links = next_node[3]
        if target == next_node[0]:
            return path
        for link in links:
            if not link[1] in closed:
                target_junc = roads[link[1]]
                opened.append((target_junc, ways.tools.compute_distance(next_node[1], next_node[2],
                                                                        target_junc[1], target_junc[2]), level))
    return path


def find_astar_route(source, target):
    'call function to find path, and return list of indices'
    raise NotImplementedError


def find_idastar_route(source, target):
    raise NotImplementedError


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    x = [5, 1, 3, 8, 2, 4]
    from sys import argv
    dispatch(argv)
