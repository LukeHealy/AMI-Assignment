
def get_heuristics(filename, graph):
    try:
        f = open(filename, "r")

        heu = {}

        for l in f:
            p = l.split(" ")
            heu[p[0]] = p[1].strip()
        
        for g in graph:
            g.h = float(heu[g.name])
    except IOError:
        print("File IO error")