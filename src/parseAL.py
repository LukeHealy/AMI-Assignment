#!/bin/python 
# 
##
# Reads an adjacency list file and returns list of the nodes.
# Also constructs the graph in memory. You basically get a graph
# for each node, so any node can be the root.
#
import sys
from node import Node
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


def parse_al(al):
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
        nodes_[e.src] = Node(e.src)
        nodes_[e.dst] = Node(e.dst)

    # Add the blank nodes to a list of nodes.
    for n_ in nodes_.values():
        nodes.append(n_)
    
    # Convert the edges src and dest to the new nodes we've just made
    # (Instead of just the name of it).
    for e in edges:
        e.src = get_node_by_name(e.src)
        e.dst = get_node_by_name(e.dst)

    # Give each node it's children, based off of edges.
    # Also give each node its edges.
    for n in nodes:
        n.children = []
        n.edges = []
        for e in edges:
            if e.src == n:
                n.children.append(e.dst)
                n.edges.append(e)
            elif e.dst == n:
                n.children.append(e.src)
                n.edges.append(e)
        

##
# Utility to resolve a node object by it's name.
#
def get_node_by_name(name):
    for g in nodes:
        if g.name == name:
            return g

##
# I think it might get a graph?
#
def get_graph(filename):
    al = read_al(filename)
    parse_al(al)
    print("\nSuccessfully read adjacency list file. \n    Nodes: " +  
        str(len(nodes)) + "\n    Edges: " + str(len(edges)) + "\n")
    return(nodes)

