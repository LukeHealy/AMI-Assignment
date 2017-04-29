#!/bin/python 
# 
##
# Reads an adjacency list file and returns list of the nodes.
# Also constructs the graph in memory. You basically get a graph
# for each node, so any node can be the root.
#
import sys
from smanode import s_node
from edge import Edge

nodes = []
edges = []

def read_al(filename):
    try:
        f = open(filename, "r")
        contents = f.read()
        f.close()

        return contents        

    except IOError:
        print("Enter a file that exists plz.")
        exit(-1)


def parse_al(al, mode):
    lines = al.split("\n")

    edges_ = {}

    # Add edge lines to a dict.
    for l in lines:
        edges_[l] = l

    # Add each edge to the edge list.
    for e_ in edges_.values():
        e_str = e_.split(" ")
        
        edges.append(Edge(e_str[2], e_str[0], e_str[1]))

    nodes_ = {}

    # Add blank nodes to a dict, based on edges.
    for e in edges:
        if mode == "sma":
            nodes_[e.src] = s_node(e.src)
            nodes_[e.dst] = s_node(e.dst)
        elif mode == "beam":
            nodes_[e.src] = b_node(e.src)
            nodes_[e.dst] = b_node(e.dst)

    # Add the blank nodes to a list of nodes.
    for n_ in nodes_.values():
        nodes.append(n_)
    
    # Convert the edges src and dest to the new nodes we've just made
    # (Instead of just the name of it).
    for e in edges:
        e.src = nodes_[e.src]
        e.dst = nodes_[e.dst]

    # Give each node it's children, based off of edges.
    # Also give each node its edges.
    for e in edges:
        nodes_[e.src.name].children.append(e.dst)
        nodes_[e.dst.name].children.append(e.src)

        nodes_[e.src.name].edges.append(e)
        nodes_[e.dst.name].edges.append(e)



##
# I think it might get a graph?
#
def get_graph(filename, mode):
    al = read_al(filename)
    parse_al(al, mode)
    print("\nSuccessfully read adjacency list file. \n    Nodes: " +  
        str(len(nodes)) + "\n    Edges: " + str(len(edges)) + "\n")
    return(nodes)

