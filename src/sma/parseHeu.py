import sys

##
# Reads a heuristic file and stores them in each node.
#
def get_heuristics(filename, graph, src, dst):
    try:
        f = open(filename, "r")
        contents = f.read()
        f.close()

        heu = {}
        heu[dst.name] = 0
        
        check_file(contents, graph)

        for l in contents.split("\n"):
            check_line(l)
            p = l.split(" ")
            heu[p[0]] = p[1].strip()
        
        for g in graph:
            if g.name != src.name or g.name != dst.name:
                g.h = float(heu[g.name])

    except IOError:
        print("File IO error.")
    except KeyError, e:
        print("Invalid heuristic file, KeyError: " + str(e) + ".")
        exit()
    except ValueError, e:
        print("Invalid heuristic file, ValueError: " + str(e) + ".")
        exit()

def check_line(line):
    parts = line.split(" ")
    if len(parts) != 2:
        print "Malformed line: '" + line + "'"
        exit()

def check_file(contents, graph):
    if len(contents.split("\n")) < len(graph) - 2:
        print "Not enough heuristics provided."
        exit()