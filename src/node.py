###
# A node in a graph.
#
import copy

class Node:
    #name = ""
    #children = []
    #edges = []
    #visited = False
    #parent = None
    #path = []

    #depth = 0
    #h = None
    #best_forgotten_f = None
    #f = None
    #g = None
    #successors = []

    def __init__(self, name_):
        self.name = name_
        self.children = []
        self.edges = []
        self.path = []
        self.successors = []
        self.parent = None
        self.visited = False
        self.depth = 0
        self.h = None
        self.best_forgotten_f = None
        self.f = None
        self.g = None
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

    def more_successors(self):
        return len(self.successors) < len(filter(lambda c: not c.name == self.parent.name, self.children))

    def generate_next_successor(self):
        if self.more_successors():
            child = filter(lambda c: not c.name == self.parent.name, self.children)[len(self.successors)]
            child.parent = self
            self.successors.append(child)

            return self.successors[-1]

    def cleanup_successor(self, node):
        names = [node.name for node in self.successors]
        idx = names.index(node.name)
        print idx
        for s in self.successors:
            print s
        del self.successors[idx]




