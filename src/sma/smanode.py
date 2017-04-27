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
        self.path = []
        self.successors = []
        self.parent = None
        self.visited = False
        self.depth = 0
        self.h = None
        self.f = None
        self.g = None
        self.F = None
        self.is_src = False
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


    def more_successors(self):
        #sys.stdout.write("Children: ")
        #self.print_path(self.children)
        #sys.stdout.write("Successors: ")
        #self.print_path(self.successors)
        return len(self.successors) < len(filter(lambda c: c.name != self.parent.name and not c.is_src, self.children))

    def next_successor(self):
        if self.more_successors():
            child = filter(lambda c: c.name != self.parent.name and not c.is_src, self.children)[len(self.successors)]
            #print "Set " + child.name + "'s parent to " + self.name
            child.parent = self
            self.successors.append(child)

            return self.successors[-1]



