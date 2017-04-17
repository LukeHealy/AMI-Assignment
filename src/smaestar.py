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

MAX_NODES = 4
INFINITY = -1

##
# Wrapper for the search harness script to call.
#
def search(src, dst, space_delta):
    node = alzheimers_simulator(src, dst, src.h)

    solution = get_partial_path(node)

    return solution


def goal_test(current, goal):
    return current.name == goal.name

def alzheimers_simulator(src, dst, total_cost):
    src.g = 0
    src.f = src.h
    src.parent = Node("Source")
    src.best_forgotten_f = 0

    open_ = []
    used = 1
    
    open_.append(src)

    while True:
        print "---------------------------"
        open_ = sorted(open_, key=lambda x: (x.f, -x.depth))
        sys.stdout.write("open: ")
        print_path(open_)

        if not open_:
            return None

        best = open_[0]

        if goal_test(best, dst):
            return best

        print("best: " + best.name)
        sys.stdout.write("children: ")
        print_path(filter(lambda x: not x.name == best.parent.name, best.children))
        s = best.generate_next_successor()

        print("s = " + s.name)
        s.g = float(s.get_edge(best, s).cost)

        if not goal_test(s, dst) and used > MAX_NODES:
            s.f = INFINITY
        else:
            s.f = max(best.best_forgotten_f, best.g + s.g + s.h)

        if not best.more_successors():
            backup(best)

        if is_subset_of(best.successors, open_):

            del open_[0]

        used += 1

        if used > MAX_NODES:
            bad = open_[-1]
            del open_[-1]

            bad.parent.cleanup_successor(bad)

            if bad.parent.name not in [o.name for o in open_]: # Parent not in open, put it in
                open.append(best.parent)

            used += 1

        open_.append(copy.copy(s))

def is_subset_of(needle, haystack):
    h_names = [h.name for h in haystack]
    n_names = [n.name for n in needle]
    print set(n_names).issubset(h_names)
    return set(n_names).issubset(h_names)

def backup(n):
    if n.parent != None:
        old_f = n.best_forgotten_f
        n.best_forgotten_f = min(n.successors, lambda c: c.f)

        if old_f != n.best_forgotten_f:
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
    src_node = get_node_by_name(nodes, sys.argv[3])
    dst_node = get_node_by_name(nodes, sys.argv[4])
    get_heuristics(sys.argv[2], nodes, src_node, dst_node)

    solution = search(src_node, dst_node, 15)

    #print_path(solution)

