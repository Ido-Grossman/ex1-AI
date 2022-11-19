# Ido Grossman 208985424
'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''
import collections
from collections import namedtuple
from ways import load_map_from_csv

def return_distance(item):
    x = item[2]
    return x

def highways(links):
    link_type_histogram = {}
    for link in links:
        if link[3] in link_type_histogram:
            link_type_histogram[link[3]] += 1
        else:
            link_type_histogram[link[3]] = 0
    return link_type_histogram

def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    x = roads[0]
    links = []
    junction_links = {}
    for junction in roads.junctions():
        junction_links[junction[0]] = len(junction[3])
        for link in junction[3]:
            links.append(link)
    junction_links = list(junction_links.values())
    return {
        'Number of junctions' : len(roads.junctions()),
        'Number of links' : len(links),
        'Outgoing branching factor' : Stat(max=max(junction_links), min=min(junction_links)
                                           , avg=sum(junction_links) / len(junction_links)),
        'Link distance' : Stat(max=max(links, key=return_distance)[2]
                               , min=min(links, key=return_distance)[2]
                               , avg=sum(item[2] for item in links) / len(links)),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : collections.Counter(highways(links)),  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()

