import copy
import sys
from smanode import s_node
from parseAL import get_graph
from parseHeu import get_heuristics

MAX_NODES = 50
INF = float("inf")

##
# Wrapper for the search harness script to call.
#
def search(src, dst, print_debug):
    if MAX_NODES < 1:
        print "No memory available."
        exit()

    if MAX_NODES == 1:
        if goal_test(src, dst):
            print "The source is the goal."
        else:
            print "No solution found."
        exit()


    solutions = nigel_thornberrys_absolutely_thrashing_search_safari(src, dst, print_debug)

    if len(solutions) > 0:
        print "Solutions:"
        for s in solutions:
            print s
    else:
        print "No solution found."

##
# 
#
def nigel_thornberrys_absolutely_thrashing_search_safari(src, dst, print_debug):

    # Init the queue
    solutions = []
    open_ = []
    open_.append(src)
    # Init the source node etc.

    src.depth = 1
    src.g = 0
    src.f = src.h
    src.parent = s_node("Path")

    # While the source node has not been backed up to infinity.
    while src.f < INF:

        for o in open_:
            if goal_test(o, dst):
                path = path_to_string(get_partial_path(o))
                if path not in solutions:
                    solutions.append(path)

        # Book keeping ####################################
        if print_debug:
            print "-------------------------"
            sys.stdout.write("open_: ")
            print_path(open_)
        ###################################################

        # If the open queue becomes empty, no solution exists.
        if not open_:
            print "Fail"
            return 

        # Get the most promising node.
        best = open_[0]

        # Book keeping ####################################
        if print_debug:
            sys.stdout.write("best: [" + str(best.f) + "]")
            print best.name
            print_path(get_partial_path(best))
        ###################################################

        # If we have a goal in the queue, record it's path.
        if goal_test(best, dst):
            path = path_to_string(get_partial_path(best))
            if path not in solutions:
                solutions.append(path)
        
            return solutions

        # Init the successor.
        succ = None

        # If there are more successors available that we have not yet seen.
        if best.more_successors():
            # Get the next successor.
            succ = best.next_successor()

            # Book keeping ####################################
            if print_debug:
                print "    best has more successors."
                sys.stdout.write("    succ: ")
                print succ.name
            ###################################################

            # Set the successors depth to one more than the "parent".
            succ.depth = best.depth + 1

            # If this isnt a goal and we're at max depth, set cost to infinity.
            if not goal_test(succ, dst) and succ.depth == MAX_NODES:
                if print_debug:
                    print "        " + succ.name + " = INF, too deep"
                succ.f = INF

            # Otherwise set the costs.
            else:
                # Get the cost from the "parent" to the successor.
                succ.g = float(succ.get_edge(succ, best).cost)
                # The f-cost equals the heuristic plus the total cost from the root.
                succ.f = succ.h + get_path_cost(succ)
                #print "        " + succ.name + ".f = " + str(succ.f)
                # This ensures consistency.
                succ.f = max(succ.f, best.f)
                #print "        " + succ.name + ".f = " + str(succ.f)

        # No more successors to generate.
        else:
            if print_debug:
                print "    No more successors."
            # Set the best cost to infinity.
            best.f = INF
            # If best has some successors (i.e not a leaf node)
            if best.successors:
                # Backup the best successors cost as best's new fcost.
                backup(best, min(best.successors, key=lambda x: x.f), print_debug)
                # Reset the successor list.
                best.successors = []

        # If we are out of memory.
        if len(open_) >= MAX_NODES:
            # Get the worst option and remove it.
            worst = open_[-1]
            if print_debug:
                print "    OUT  OF MEMORY"
                print "Worst: " + worst.name + " remove."

            open_.remove(worst)

        # If there was a successor generated.
        if succ != None:
            # If succ is not already in open_, add it.
            if succ not in open_:
                if print_debug:
                    print "Put " + succ.name + " in open_"
                open_.append(succ)

        # Sort the open_ list by f-cost and depth, prioritising f-cost.
        open_.sort(key=lambda x: (x.f, -x.depth))

    return solutions

def backup(best, best_succ, print_debug):
    if print_debug:
        print "    Backup " + best.name + "[ " + str(best.f) + "] with " + best_succ.name + " [" + str(best_succ.f) + "]"
    best.f = best_succ.f

def is_subset(needle, haystack):
    sys.stdout.write("        needle: ")
    print_path(needle)
    sys.stdout.write("        haystack: ")
    print_path(haystack)

    n_names = [n.name for n in needle]
    h_names = [h.name for h in haystack]

    n = set(n_names)
    h = set(h_names)

    return n.issubset(h)


def get_path_cost(node):
    cost = 0
    while node.parent != None:
        #print node.name
        # print node.g
        # print type(node.g)
        cost += float(node.g)
        node = node.parent
    return cost

def goal_test(current, goal):
    return current.name == goal.name

def print_path(solution):
    ans = ""
    for n in solution:
        ans += n.name + ", "

    print("[" + ans[0:len(ans) - 2] + "]")


def path_to_string(path):
    ans = ""
    for n in path:
        ans += n.name + ", "

    return ("[" + ans[0:len(ans) - 2] + "]")

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
    src_node.is_src = True
    dst_node = get_node_by_name(nodes, sys.argv[4])
    get_heuristics(sys.argv[2], nodes, src_node, dst_node)

    search(src_node, dst_node, int(sys.argv[5]))

