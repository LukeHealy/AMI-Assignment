###
# Memory limmited A* search.
#
#!/bin/python
#

import copy
import sys
from smanode import s_node
from parseAL import get_graph
from parseHeu import get_heuristics

##
# Wrapper for the search harness script to call.
#
def search(src, dst, space_delta):
    node = alzheimers_simulator(src, dst, src.h)

    solution = get_partial_path(node)

    return solution

def alzheimers_simulator(current_node, dst, total_cost):
    # Init our lists
    open_ = []
    closed_ = []

    # Add the source to the open list.
    # Initialise some required members.
    open_.append(current_node)
    current_node.g = 0
    current_node.f = current_node.h
    # This is for simplicity.
    current_node.parent = s_node("Path")

    # While we have nodes left in the open list.
    while open_:
        # Get the best option.
        open_ = sorted(open_, key=lambda o: o.f)

        #sys.stdout.write("open_: ")
        #print_path(open_)

        q = open_[0]
        del open_[0]
        
        closed_.append(q)

        for ch in filter(lambda cn: q.parent.name != cn.name, q.children):
            # Copy the child into a new node. This is so that we can have
            # more than one path per node. (Otherwise we would overwrite the
            # heuristic in existing paths)
            c = copy.deepcopy(ch)
            # Set the parent.
            c.parent = q
            # Exit if we have found the goal.
            if c.name == dst.name:
                print "Found path:"
                print_path(get_partial_path(c))

            # Calculate the heuristic.
            c.g = float(q.f) + float(c.get_edge(c, q).cost)
            c.f = (c.g) + (c.h)

            # Get any record of this node already visited
            alternate_path = filter(lambda cn: cn.name == c.name, open_)
            alternate_path += filter(lambda cn: cn.name == c.name, closed_)

            alternate_path = sorted(alternate_path, lambda cn: cn.f)
            # Ensure that we only keep looking down this path if we either havn't 
            # been there, or we have found a more promising path.
            if alternate_path:
                if alternate_path[0] >= c.f:
                    open_.insert(0, c)
            else:
                open_.insert(0, c)

    return q

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
        print "Usage: python astar.py <adgacency_list.al> <heuristic_list.heu> <src> <dst>"
        exit(1)

    nodes = get_graph(sys.argv[1], "sma")
    src_node = get_node_by_name(nodes, sys.argv[3])
    dst_node = get_node_by_name(nodes, sys.argv[4])
    get_heuristics(sys.argv[2], nodes, src_node, dst_node)

    solution = search(src_node, dst_node, 15)

    #print_path(solution)

