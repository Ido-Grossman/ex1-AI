'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''
import ways


# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

def huristic_function(lat1, lon1, lat2, lon2):
    distance = ways.tools.compute_distance(lat1, lon1, lat2, lon2)
    return distance / 110


def find_rout(source, target, mode, roads):
    import heapq
    # loading the roads from the map.
    # creating the closed nodes list.
    closed = set()
    # creating the opened nodes list and adding the first node, where 0 is the cost to it, and -1 is the parent.
    opened = [(0, roads[source], -1)]
    # creating a map of parents and putting source and target parents as -1, the algorithm will later change the target
    # parent.
    parents = {source: -1, target: -1}
    cost = 0
    target_node = roads[target]
    while opened:
        next_node = heapq.heappop(opened)
        min_cost, parent, next_node = next_node[0], next_node[2], next_node[1]
        node_index = next_node[0]
        parents[node_index] = parent
        closed.add(node_index)
        links = next_node[3]
        if target == node_index:
            cost = min_cost
            break
        for link in links:
            if not link[1] in closed:
                target_junc = roads[link[1]]
                if mode == 'ucs':
                    f = min_cost
                else:
                    f = min_cost + huristic_function(next_node[1], next_node[2], target_node[1], target_node[2])
                new_cost = link[2] + f
                found = False
                index = 0
                for item in opened:
                    if item[1] is target_junc:
                        found = True
                        break
                    index += 1
                if found:
                    old_node = opened.pop(index)
                    if new_cost < old_node[0]:
                        old_node = (new_cost, old_node[1], node_index)
                    heapq.heappush(opened, old_node)
                else:
                    heapq.heappush(opened, (new_cost, target_junc, node_index))
    path = [target]
    parent = parents[target]
    while parent != -1:
        path.insert(0, parent)
        parent = parents[parent]
    return path, cost


def find_ucs_rout(source, target):
    roads = ways.load_map_from_csv()
    path, cost = find_rout(source, target, 'ucs', roads)
    print(cost)
    return path


def find_astar_route(source, target):
    roads = ways.load_map_from_csv()
    path, cost = find_rout(source, target, 'astar', roads)
    print(cost)
    return path


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
    x = [[0, 5], [1, 1], [2, 3], [1, 8], [4, 2], [3, 4]]
    from sys import argv
    dispatch(argv)
