###
# Memory limmited A* search.
#
#!/bin/python
#

import copy
import sys
from node import Node
from parseAL import get_graph
from parseHeu import get_heuristics

MAX_NODES = 3
INFINITY = -1

##
# Wrapper for the search harness script to call.
#
def search(src, dst, space_delta):
    node = alzheimers_simulator(src, dst, src.h1)

    solution = get_partial_path(node)

    return solution

def enqueue(l, item):
    l.append(item)
    l = sorted(l, lambda c: c.f)

def dequeue(l):
    item = l[-1]
    del l[-1]

    return item

def goal_test(current, goal):
    return current.name == goal.name

def alzheimers_simulator(src, dst, total_cost):
    open_ = []
    src.g = 0
    src.fs = src.h1
    src.fn = 0

    used = 1
    enqueue(open_, src)

    while True:
        if not open_:
            return None

        best = open_[0]

        if goal_test(best, dst):
            return best

        s = best.generate_next_successor()

        s.fs = max(best.fs, s.g + s.h)

        if not best.more_successors():
            backup(best)

        if is_subset_of(best.successors, open_):
            dequeue(open_)

def is_subset_of(needle, haystack):
    h_names = [h.name for h in haystack]
    n_names = [n.name for n in needle]

    return set(n_names).issubset(h_names)

def backup(n):
    if not n.more_successors() and n.parent != None:
        old_fn = n.fn
        n.fn = min(n.successors, lambda c: c.fs)

        if old_fn != n.fn:
            backup(n.parent)





def print_path(solution):
    ans = ""
    for n in solution:
        ans += n.name + ", "

    print("[" + ans[0:len(ans) - 2] + "]")


def get_partial_path(node):
    solution = [node]
    while node.parent != None:
        #print node
        solution.append(node.parent)
        node = node.parent
    return solution[::-1]

##
# Utility to resolve a node object by it's name.
#
def get_node_by_name(graph, name):
    for g in graph:
        if g.name == name:
            return g

def get_path_length(node):
    count = 0
    while node.parent != None:
        #print node
        count += 1
        node = node.parent
    return count

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python smaestar.py <adgacency_list.al> <heuristic_list.heu> <src> <dst>"
        exit(1)

    nodes = get_graph(sys.argv[1])
    get_heuristics(sys.argv[2], nodes)
    src_node = get_node_by_name(nodes, sys.argv[3])
    dst_node = get_node_by_name(nodes, sys.argv[4])

    solution = search(src_node, dst_node, 15)

    #print_path(solution)

