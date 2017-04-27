import sys
import copy
from beamnode import b_node
from parseAL import get_graph
from parseHeu import get_heuristics
from operator import attrgetter

##
# Wrapper for the search harness script to call.
#
def search(src, dst, k, find_all, print_debug):
    if k < 1:
        print "Why is k < 1?"
        exit()

    solutions = beam_informercial(k, src, dst, find_all, print_debug)

    return solutions

# Utility to grab a node object given it's name.
#
def get_node_by_name(graph, name):
    for g in graph:
        if g.name == name:
            return g

##
# Where the good stuff happens.
#
def beam_informercial(k, src, dst, find_all, print_debug):

    if src.name == dst.name:
        return dst

    node = src
    node.parent = None
    node.path = []
    node.path.append(node.name)
    frontier = []
    frontier.append(src)
    node.visited = True
    paths_found = []

    depth = 0
    # While the frontier isn't empty.
    while frontier:
        beam = []

        if print_debug:
            print "-------------------------------------"
            depth += 1
            print("depth = " + str(depth))
            sys.stdout.write("frontier: ")
            print [f.name for f in frontier]

        # Explore the whole frontier
        for node in frontier:
            # Mark as visited so that we don't consider it
            # if it appears somewhere down the track.
            node.visited = True

            if print_debug: 
                sys.stdout.write("Current node: ")
                print node.name
                print "Possible paths: "

            # For every child we havn't yet been to.
            for c in filter(lambda x: not x.visited, node.children):
                # Shallow copy the path by slicing all of it.
                c.path = node.path[:]
                c.path.append(c.name)

                if print_debug:
                    sys.stdout.write("    ")
                    print_path(c.path)

                # We found the goal.
                if c.name == dst.name:
                    # Save the path that we found.
                    paths_found.append(c.path)

                    # Print all paths currently in memory
                    print "Path found. Current paths in memory:"
                    for f in frontier:
                        print_path(f.path)
                    # If we want to exit early, do so.
                    # Otherwise keep looking.
                    if not find_all:
                        return paths_found
                # Append a copy of every child to the beam.
                else:
                    beam.append(copy.deepcopy(c))

        # The new frontier is the best k in the beam.
        frontier = sorted(beam, key=lambda x: x.h)[:k]

    return paths_found

##
# Prints a list of node names nicely
#
def print_path(solution):
    ans = ""
    for n in solution:
        ans += n + ", "

    print("[" + ans[0:len(ans) - 2] + "]")

##
# Follows parents up and returns the list of steps.
#
def get_partial_path(node):
    solution = [node]
    while node.parent != None:
        solution.append(node.parent)
        node = node.parent
    return solution[::-1]


if __name__ == '__main__':
    if len(sys.argv) < 8:
        print "Usage: python beam.py <adgacency_list.al> <heuristic_list.heu> <src> <dst> <K> <findall> <debug>"
        exit(1)

    nodes = get_graph(sys.argv[1], "beam")
    src_node = get_node_by_name(nodes, sys.argv[3])
    dst_node = get_node_by_name(nodes, sys.argv[4])
    get_heuristics(sys.argv[2], nodes, src_node, dst_node)

    solutions = search(src_node, dst_node, int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))

    if solutions != None and len(solutions) > 0:
        print
        print "Solution Path:"
        print_path(solutions[0])

        print "Alternate Paths:"
        for s in solutions[1:]:
            print_path(s)
    else:
        print "No solutions found. Running again in verbose mode."
        solutions = search(src_node, dst_node, int(sys.argv[5]), int(sys.argv[6]), 1)



    