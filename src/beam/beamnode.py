###
# A node in a graph.
#
import copy

class b_node:

    def __init__(self, name_):
        self.name = name_
        self.children = []
        self.edges = []
        self.path = []
        self.parent = None
        self.visited = False
        self.h = None

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
    # Returns a deep copy of the node, because deepcopy is mad slow.
    #
    def clone(self):
        new = b_node(str(self.name))
        new.children = self.children[:]
        new.edges = self.edges[:]
        new.path = self.path[:]
        new.parent = self.parent
        new.visited = True
        new.h = float(self.h)

        return new
