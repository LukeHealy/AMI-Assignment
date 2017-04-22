###
# Stores an edge in a graph.
#

class Edge:
    cost = 0
    src = None
    dst = None

    def __init__(self, cost, src, dst):
        self.cost = cost
        self.src = src
        self.dst = dst

    ##
    # QnD toString
    #
    def __str__(self):
        return("|Edge " + self.src.name + "," + self.dst.name + ":" + self.cost + "|")