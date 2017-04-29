import copy
import sys
from smanode import s_node
from parseAL import get_graph
from parseHeu import get_heuristics

MAX_NODES = 4
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

    (solutions, iterations) = nigel_thornberrys_absolutely_thrashing_search_safari(src, dst, print_debug)
    
    print "Iterations: " + str(iterations)

    if len(solutions) > 0:
        print "Solutions:"
        for s in solutions:
            print s.replace("[Path, ", "[")
    else:
        print "No solution found."

##
# This is the simplified memory A * search.
#
def nigel_thornberrys_absolutely_thrashing_search_safari(src, dst, print_debug):

    # Init the queue
    solutions = []
    open_ = []
    open_.append(src)
    # Init the source node etc.

    src.depth = 1
    src.f = src.h
    src.parent = s_node("Path")

    iterations = 0

    # While the source node has not been backed up to infinity.
    while src.f < INF and open_:
        iterations += 1

        if dst in open_:
            if print_debug:
                print "i: " + str(iterations)
            path = path_to_string(get_partial_path(dst))
            if path not in solutions:
                solutions.append(path)
                print "Solution Found - paths in memory:"
                sys.stdout.write("open queue: ")
                print_path(open_)
                for o in open_:
                    print_path(get_partial_path(o))

        # Book keeping ####################################
        if print_debug:
            print "-------------------------"
            sys.stdout.write("open_: ")
            print_path(open_)
            for o in open_:
                print o.name + " " + str(o.f)
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
            return (solutions, iterations)

        # Init the successor.
        succ = None

        # If there are more successors available that we have not yet seen.
        if best.more_successors(get_partial_path(best), open_):
            # Get the next successor.
            succ = best.next_successor(get_partial_path(best), open_)

            # Book keeping ####################################
            if print_debug:
                print "    best has more successors."
                sys.stdout.write("    succ: ")
                print succ.name
            ###################################################

            # Set the successors depth to one more than the "parent".
            succ.depth = best.depth + 1

            # If this isnt a goal and we're at max depth, set cost to infinity.
            if not goal_test(succ, dst) and succ.depth >= MAX_NODES:
                if print_debug:
                    print "        " + succ.name + " = INF, too deep"
                succ.f = INF

            # Otherwise set the costs.
            else:
                # The f-cost equals the heuristic plus the total cost from the root.
                succ.f = succ.h + get_path_cost(succ)
                # This ensures consistency.
                succ.f = max(succ.f, best.f)

        # No more successors to generate.
        else:
            if print_debug:
                print "    No more successors."
            # Set the best cost to infinity.
            # If best has some successors (i.e not a leaf node)
            if best.successors:
                # Backup the best successors cost as best's new fcost.
                min_node = min(best.successors, key=lambda x: x.f)
                backup(best, min_node, print_debug)
                open_.sort(key=lambda x: (x.f, -x.depth))

                # Reset the successor list.
                best.successors = []
            # else it's a leaf node
            else:
                best.f = INF
                open_.remove(best)

        # If we are out of memory.
        if len(open_) >= MAX_NODES:
            # Get the worst option and remove it.
            worst_leaves = filter(lambda x: x not in get_partial_path(best), open_)
            worst = worst_leaves[-1]
            #print_path(worst_leaves)

            if print_debug:
                print "    OUT  OF MEMORY"
                print "Worst: " + worst.name + " remove."

            open_.remove(worst)

        # If there was a successor generated.
        if succ != None and succ not in open_ and succ.f < INF:
                if print_debug:
                    print "Put " + succ.name + " in open_"
                open_.append(succ)

        # Sort the open_ list by f-cost and depth, prioritising f-cost.
        open_.sort(key=lambda x: (x.f, -x.depth))

    return (solutions, iterations)

##
# Sets the f-cost of a node to the best f-cost of its successors.
#
# def backup(best, best_succ, print_debug):
#     old_f = best.f
#     if best.parent != None:
#         if print_debug:
#             print "    Backup " + best.name + " [" + str(best.f) + "] with " + best_succ.name + " [" + str(best_succ.f) + "]"
#         best.f = best_succ.f
#         if best.f != old_f:
#             #backup(best.parent, best, print_debug)
#             if best.parent.successors:
#                 backup(best.parent, min(best.parent.successors, key=lambda x: x.f), print_debug)

##
# Sets the f-cost of a node to the best f-cost of its successors.
#
def backup(best, best_succ, print_debug):
    if print_debug:
        print "    Backup " + best.name + " [" + str(best.f) + "] with " + best_succ.name + " [" + str(best_succ.f) + "]"
    best.f = best_succ.f

##
# Returns true if needle is a subset of haystack.
#
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

##
# Follows the parents up until the source and counts the cost.
#
def get_path_cost(node):
    cost = 0
    while node.parent.parent != None:
        cost += float(node.get_edge(node, node.parent).cost)
        node = node.parent

    return cost

##
# Returns true if the current is the goal.
#
def goal_test(current, goal):
    return current.name == goal.name

##
# Prints a path. (Any list of nodes.)
#
def print_path(solution):
    ans = ""
    for n in solution:
        if n.name != "Path":
            ans += n.name + ", "

    print("[" + ans[0:len(ans) - 2] + "]")

##
# Converts a path to a string.
#
def path_to_string(path):
    ans = ""
    for n in path:
        ans += n.name + ", "

    return ("[" + ans[0:len(ans) - 2] + "]")

##
# Follows back up the parent until it gets to the source and
# returns the path as a list.
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
# Main just calls the file io and starts the search.
#
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

