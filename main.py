# Ido Grossman 208985424
'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''
import math
from ways import tools, graph, info
new_limit = 0

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions


def huristic_function(lat1, lon1, lat2, lon2):
    distance = tools.compute_distance(lat1, lon1, lat2, lon2)
    return distance / 110


@tools.timed
def find_rout(source, target, mode, roads):
    import heapq
    from ways import info
    # loading the roads from the map.
    # creating the closed nodes list.
    closed = set()
    # creating the opened nodes list and adding the first node, where 0 is the cost to it, and -1 is the parent.
    opened = []
    # Sets source node and target node to their respective junctions.
    source_node, target_node = roads[source], roads[target]
    huristic_cost = 0
    # Sets the huristic cost from the source to target if the mode is astar
    if mode == 'astar':
        huristic_cost = huristic_function(source_node.lat, source_node.lon, target_node.lat, target_node.lon)
    # Adds the source node to the open nodes list
    opened.append((0, source_node, -1, 0))
    # creating a map of parents and putting source and target parents as -1, the algorithm will later change the target
    # parent.
    parents = {source: -1, target: -1}
    cost = 0
    while opened:
        # Takes the minimum out of the minimum heap
        next_node = heapq.heappop(opened)
        # Ordering the tuple in variables for clarity
        prev_cost, parent, prev_huristics, next_node = next_node[0], next_node[2], next_node[3], next_node[1]
        node_index = next_node.index
        # Sets the parent of the node in the parents map
        parents[node_index] = parent
        # Adds the current node to the closed nodes list.
        closed.add(node_index)
        links = next_node.links
        # If the current node is the target node it sets the cost for getting here and breaks out of the loop
        if target == node_index:
            cost = prev_cost
            break
        # Looping over all the successors of the node
        for link in links:
            # Making sure the junction isn't in the closed junctions list.
            if link.target not in closed:
                target_junc = roads[link.target]
                h, g = 0, prev_cost
                # If we do ucs we don't need heuristic function, So it will be 0, if it's astar h will be the heuristic
                # function
                if mode == 'ucs':
                    h = 0
                else:
                    h = huristic_function(target_junc.lat, target_junc.lon, target_node.lat, target_node.lon)
                # Sets f as the cost to the junction
                f = g + h - prev_huristics
                # Sets the new_cost as f + the distance to the link target divided by 1000 to convert it to km, and
                # all this is divided by the max speed in the link
                new_cost = f + ((link.distance / 1000) / info.SPEED_RANGES[link.highway_type][1])
                # Checking if the link is in the open list.
                found = False
                index = 0
                for item in opened:
                    if item[1] is target_junc:
                        found = True
                        break
                    index += 1
                # If the link is in the open list, it updates its cost if new_cost is lower than his cost.
                if found:
                    old_node = opened.pop(index)
                    if new_cost < old_node[0]:
                        old_node = (new_cost, old_node[1], node_index, h)
                    heapq.heappush(opened, old_node)
                else:
                    heapq.heappush(opened, (new_cost, target_junc, node_index, h))
    # Creates a list of the path from source to target and returns it with the cost and huristic function
    path = [target]
    parent = parents[target]
    while parent != -1:
        path.insert(0, parent)
        parent = parents[parent]
    return path, cost, huristic_cost


def find_ucs_rout(source, target):
    # Calling the findrout function with ucs mode and returns the path.
    roads = graph.load_map_from_csv()
    path, cost, x = find_rout(source, target, 'ucs', roads)
    return path


def find_astar_route(source, target):
    # Calling the findrout function with astar mode and returns the path.
    roads = graph.load_map_from_csv()
    path, cost, x = find_rout(source, target, 'astar', roads)
    return path


def DFSF(state, g, path, f_limit, goal, roads):
    global new_limit
    # Sets the state and goal node from the roads.
    state_node, goal_node = roads[state], roads[goal]
    # Updating the new_f as the previous g + the heuristic function from this state to the goal
    new_f = g + huristic_function(state_node.lat, state_node.lon, goal_node.lat, goal_node.lon)
    # If the new_f is higher than f_limit it sets the new_limit to be the minimum of new_limit and new_f
    if new_f > f_limit:
        new_limit = min(new_limit, new_f)
        return None
    # If we reached the goal we return the path.
    if state == goal:
        return path
    # Looping over all the successors.
    for link in state_node.links:
        # Activates the DFSF function on the next link.
        path_copy = path.copy()
        path_copy.append(link.target)
        sol = DFSF(link.target, g + ((link.distance / 1000) / info.SPEED_RANGES[link.highway_type][1]), path_copy,
                   f_limit, goal, roads)
        if sol:
            return sol
    return None


@tools.timed
def idastar_algo(source, target, roads):
    global new_limit
    # Sets the state and goal node from the roads.
    source_node, target_node = roads[source], roads[target]
    # Sets the new_limit to be the heuristic function from source to target goal.
    new_limit = huristic_function(source_node.lat, source_node.lon, target_node.lat, target_node.lon)
    # Keeps iterating until finding answer
    while True:
        # Sets the f_limit to be the new_limit and new_limit to be infinity
        f_limit = new_limit
        new_limit = math.inf
        # Tries to find solution and if it succeeds, It returns the path.
        sol = DFSF(source, 0, [source], f_limit, target, roads)
        if sol:
            return sol


def find_idastar_route(source, target):
    roads = graph.load_map_from_csv()
    return idastar_algo(source, target, roads)


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
    from sys import argv
    dispatch(argv)
