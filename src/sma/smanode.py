###
# A node in a graph.
#
import copy
import sys

class s_node:

    def __init__(self, name_):
        self.name = name_
        self.children = []
        self.edges = []
        self.successors = []
        self.parent = None
        self.depth = 0
        self.h = None
        self.f = None
        self.is_src = False
        self.INF = float("inf")

    ##
    # QnD toString
    #
    def __str__(self):
        child = ""
        for c in self.children:
            child += c.name + ","

        child += ": "

        edge = ""
        for e in self.edges:
            edge += str(e) + ","

        return("\Node " + self.name + ": " + child + edge + "h = " + str(self.h) + "/" )

    ##
    # So that I can get the cost it takes to get here from src.
    #
    def get_edge(self, src, dst):
        for e in self.edges:
            if e.src.name == src.name and e.dst.name == dst.name:
                return e
            elif e.src.name == dst.name and e.dst.name == src.name:
                return e
    
    def print_path(self, solution):
        ans = ""
        for n in solution:
            ans += n.name + ", "

        print("[" + ans[0:len(ans) - 2] + "]")


    ##
    # Follows the parents up until the source and counts the cost.
    #
    def get_path_cost(self, node):
        cost = 0
        while node.parent.parent != None:
            cost += float(node.get_edge(node, node.parent).cost)
            node = node.parent

        return cost

    def next_successor(self, path_to_here, open_):
        child = self.get_successor(path_to_here, open_)

        if child != None:
            child.parent = self
            self.successors.append(child)
        return child
        # if child != None:
        #     if child in open_:
        #         fcost = child.f
        #     else:
        #         child.parent = self
        #         self.successors.append(child)
        #         return child

        #     ## Seen before.
        #     # make copy
        #     temp = s_node(child.name)
        #     temp.parent = self
        #     temp.edges = child.edges[:]

        #     newf = self.get_path_cost(temp) + child.h
            
        #     if newf <= fcost:
        #         child.parent = self

        #     self.successors.append(child)
        #     return child



    def get_successor(self, path_to_here, open_):
        for c in self.children:
            if c not in path_to_here and c not in self.successors:
                return c



