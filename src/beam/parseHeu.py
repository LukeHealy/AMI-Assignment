import sys

##
#
#
def get_heuristics(filename, graph, src, dst):
    try:
        f = open(filename, "r")

        heu = {}
        heu[src.name] = sys.maxint
        heu[dst.name] = 0
        for l in f:
            p = l.split(" ")
            heu[p[0]] = p[1].strip()
        
        for g in graph:
            if g.name != src.name or g.name != dst.name:
                g.h = float(heu[g.name])

    except IOError:
        print("File IO error")