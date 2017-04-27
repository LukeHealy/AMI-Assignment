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

MAX_NODES = 8
INF = sys.maxint

##
# Wrapper for the search harness script to call.
#
def search(src, dst, space_delta):
    node = alzheimers_simulator(src, dst, src.h)

    solution = get_partial_path(node)

    return solution

def alzheimers_simulator(src, dst, total_cost):
    # Init our lists
    open_ = []

    # Add the source to the open list.
    # Initialise some required members.
    open_.append(src)
    src.g = 0
    src.f = src.h
    src.depth = 0
    src.parent = s_node("Path")

    # While we have nodes left in the open list.
    while open_:
        # Sort by both f-cost and depth, 
        # we're better off exploring deeper node first.
        open_.sort(key=lambda o: (o.f, -o.depth))

        print "-------------------------"

        sys.stdout.write("open_: ")
        print_path(open_)

        q = open_[0]
        #del open_[0]
        
        # This check is so that I can find alternative paths.
        q.visited = True
        print_path(get_partial_path(q))
        if q.depth < MAX_NODES - 1:

            # For each successor we haven't yet seen. Get the cost
            successors = filter(lambda cn:  not cn.visited, q.children)
            for c in successors:

                # Set the parent and depth.
                c.parent = q
                c.depth = q.depth + 1

                # Exit if we have found the goal.
                if goal_test(c, dst):
                    print "Found path:"
                    print_path(get_partial_path(c))
                    #return c 

                # Calculate the heuristic.
                c.g = float(q.g) + float(c.get_edge(c, q).cost)
                c.f = c.g + c.h

                #c.f = max(q.f, c.g + c.h)
            

                if c not in open_:
                    if len(open_) == MAX_NODES - 1:
                        open_[1].f = open_[-1].f
                        del open_[-1]

                    open_.insert(0, c)

            if successors:
                q.F = min(successors, key=lambda x: x.f).f
            else:
                del open_[0]
                q.f = INF

            if q.name not in [o.name for o in open_]: 
                open_.remove(q)

            open_.sort(key=lambda o: (o.f, -o.depth))

            # Backup best child f-cost in parent
            # if successors:
            #     best = min(successors, key=lambda x: x.f)
            #     q.f = best.f

        else:
            q.f = INF
            del open_[0]
            sys.stdout.write("Giving up on path: ")
            print_path(get_partial_path(q))
    return q

def goal_test(current, goal):
    return current.name == goal.name

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

