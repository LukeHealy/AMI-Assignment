###
#
#!/bin/python
#
# Memory limmited A* search.
#

import copy
import sys
from smanode import s_node
from parseAL import get_graph
from parseHeu import get_heuristics

MAX_NODES = 10
INFINITY = sys.maxint

##
# Wrapper for the search harness script to call.
#
def search(src, dst):
    for i in range(1, MAX_NODES - 1):

        print("Iteration: " + str(i))

        src.g = 0
        src.f = src.h
        it_just_keeps_happening(src, dst, 0, i, INFINITY)

##
# Where the good stuff happens.
#
def it_just_keeps_happening(current_node, dst, iteration, max_, f_limit):
    if goal_test(current_node, dst):
        return current_node, f_limit

    successors = filter(lambda x: not x.visited, current_node.children)

    if not successors:
        return None, INFINITY

    for s in successors:
        s.parent = current_node
        s.f = max(get_path_cost(s) + s.h, current_node.f)

    while True:
        best = successors.sort(lambda x: x.f)[0]
        if best.f > f_limit:
            return None, best.f
        alt_f4 = successors[1].f
        result,best.f = it_just_keeps_happening(
            best, dst, iteration, max_, min(f_limit, alt_f4))

##
# 
#
def unvisit(node):
    if node.parent != None:
        unvisit(node.parent)
    node.visited = False
    node.parent = None

##
#
#
def get_path_cost(node):
    cost = 0
    if node.parent != None:
        cost += float(get_path_cost(node.parent))

        return node.get_edge(node, node.parent).cost
    else:
        return 0


##
#
#
def goal_test(current, goal):
    return current.name == goal.name

##
#
#
def print_path(solution):
    ans = ""
    for n in solution:
        ans += n.name + ", "

    print("[" + ans[0:len(ans) - 2] + "]")

##
#
#
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


##
#
#
def get_depth(node):
    count = 0
    while node.parent != None:
        #print node
        count += 1
        node = node.parent
    return count

##
#
#
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python smaestar.py <adgacency_list.al> <heuristic_list.heu> <src> <dst>"
        exit(1)

    nodes = get_graph(sys.argv[1], "sma")
    src_node = get_node_by_name(nodes, sys.argv[3])
    dst_node = get_node_by_name(nodes, sys.argv[4])
    get_heuristics(sys.argv[2], nodes, src_node, dst_node)

    search(src_node, dst_node)


