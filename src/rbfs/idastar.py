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

MAX_NODES = 15
INFINITY = sys.maxint

##
# Wrapper for the search harness script to call.
#
def search(src, dst):
    node = alzheimers_simulator(src, dst)

    solution = get_partial_path(node)

    return solution

##
#
#
def alzheimers_simulator(src, dst):
    
    iteration = 1
    while True:
        src.parent = s_node("Path")
        src.g = 0
        src.f = src.h
        f_bound = src.f

        t_node = src
    
        sys.stdout.write("iteration: ")
        print iteration
        iteration += 1
        (t_node, t) = explore(t_node, f_bound, 0, src, dst)
        unvisit(t_node)
        if goal_test(t_node, dst):
            print "Found: "
            print_path(get_partial_path(t_node))
        if t == INFINITY:
            print "Not found"
            return src
        f_bound = t

##
# 
#
def explore(node, f_bound, prev_g, src, dst):
    node.visited = True
    sys.stdout.write("    current node: ")
    print node.name

    if node.name == src.name:
        node.g = 0
    else:
        node.g = node.get_edge(node.parent, node).cost

    node.f = float(node.g) + float(node.h)
    if node.f > f_bound:
        return (node, node.f)
    if goal_test(node, dst):
        return (node, node.f)

    min_ = INFINITY

    for succ in filter(lambda x: not x.visited, node.children):
        sys.stdout.write("    succ: ")
        print succ.name
        succ.parent = node
        succ.g = succ.get_edge(node, succ).cost
        (t_node, t) = explore(succ, float(prev_g) + float(succ.g), f_bound, src, dst)

        if goal_test(t_node, dst):
            return (t_node, t)

        min_ = min(t, min_)

    return (t_node, min_)

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

    solution = search(src_node, dst_node)

    #print_path(solution)

