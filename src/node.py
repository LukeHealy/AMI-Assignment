###
# A node in a graph.
#

class Node:
    name = ""
    children = []
    edges = []
    visited = False
    parent = None
    path = []

    h = None
    fn = None
    fs = None
    g = None

    successors = []

    def __init__(self, name):
        self.name = name

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
        return len(successors) < len(children)

    def generate_next_successor(self):
        if more_successors():
            successors.append(children[len(successors)])

        return successors[-1]

