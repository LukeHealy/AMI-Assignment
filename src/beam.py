import sys
import copy
from parseAL import get_graph
from parseHeu import get_heuristics
from operator import attrgetter

print_debug = True

##
# Wrapper for the search harness script to call.
#
def search(current_node, dst, k):
    solutions = beam_informercial(k, current_node, dst, False)

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
def beam_informercial(k, src, dst, found, ):

    if src.name == dst.name:
        return dst

    node = src
    node.parent = None
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
            print
            sys.stdout.write("frontier: ")
            print [f.name for f in frontier]

            depth += 1
            print("depth = " + str(depth))

        for node in frontier:
            node.visited = True

            if print_debug: 
                sys.stdout.write("Current node: ")
                print node.name
                print "Possible paths: "

            for c in filter(lambda x: not x.visited, node.children):

                c.path = node.path[:]
                c.path.append(c.name)

                if print_debug:
                    sys.stdout.write("    ")
                    print_path(c.path)

                if c.name == dst.name:
                    paths_found.append(c.path)

                else:
                    beam.append(copy.deepcopy(c))

        frontier = sorted(beam, key=lambda x: x.h)[:k]

        # for f in frontier:
        #      print f

    return paths_found

def print_path(solution):
    ans = ""
    for n in solution:
        ans += n + ", "

    print("[" + ans[0:len(ans) - 2] + "]")


def get_partial_path(node):
    solution = [node]
    while node.parent != None:
        solution.append(node.parent)
        node = node.parent
    return solution[::-1]


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage: python beam.py <adgacency_list.al> <heuristic_list.heu> <src> <dst> <K>"
        exit(1)

    nodes = get_graph(sys.argv[1])
    get_heuristics(sys.argv[2], nodes)
    src_node = get_node_by_name(nodes, sys.argv[3])
    dst_node = get_node_by_name(nodes, sys.argv[4])

    solutions = search(src_node, dst_node, int(sys.argv[5]))

    print
    print "Solution Path:"
    print_path(solutions[0])

    print "Alternate Paths:"
    for s in solutions[1:]:
        print_path(s)


    