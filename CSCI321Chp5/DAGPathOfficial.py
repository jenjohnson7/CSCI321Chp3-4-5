#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 5D

@author: mlinderman
"""

import sys
import re
import math

class DirectedGraph:
    """Simple graph"""
    def __init__(self):
        self.edges = {}
        self.weights = {}

    def add_edge(self, source, sink, weight):
        if source in self.edges:
            self.edges[source].add(sink)
        else:
            self.edges[source] = { sink }
        self.weights[(source, sink)] = weight

    def outgoing(self, node):
        """Return list of outgoing edges as their weights
    
        Args:
            node: Source node
        
        Returns:
            List of (node, weight) tuples for outgoing edges
        """
        return [(out, self.weights[(node, out)]) for out in self.edges.get(node,[])]

    def incoming(self):
        """Reverse graph so that values in dictionary are incoming edges
        
        Returns:
            Copy of graph reversed
        """
        edges = {}
        for node, outgoing_edges in self.edges.items():
            if node not in edges:
                edges[node] = []
            for outgoing_nodes in outgoing_edges:
                if outgoing_nodes in edges:
                    edges[outgoing_nodes].append(node)
                else:
                    edges[outgoing_nodes] = [node]
        return edges
                
    def order(self):
        """Return list of nodes in topological order"""
        edges = self.incoming()
        
        candidates = set()
        for node, incoming_edges in edges.items():
            if len(incoming_edges) == 0:
                candidates.add(node)
        
        order = []
        while len(candidates) != 0:
            working_node = candidates.pop()
            order.append(working_node)
            for outgoing_node in self.edges.get(working_node,[]):
                edges[outgoing_node].remove(working_node)
                if len(edges[outgoing_node]) == 0:
                    candidates.add(outgoing_node)
        
        return order

def read5D(filename):
    """Read inputs for Rosalind 5D"""
    with open(filename, "r") as file:
        source = int(file.readline())
        sink = int(file.readline())
        
        graph = DirectedGraph()
        for line in file:
            match = re.search(r'(\d+)->(\d+):(\d+)', line)
            graph.add_edge(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return graph, source, sink                

                
def longest_path(graph, source, sink):
    """Print longest path in a DAG
    
    Assumes graph nodes are integers where the numerical ordering is 
    also a topological ordering
    
    Args:
        graph: DirectedGraph
        source, sink: Source and sink nodes
    """
    order = graph.order()
    
    path = {}
    for node in order:
        path[node] = (-math.inf, None)
    path[source] = (0, None)
    
    for node in order:
        # Since it is easier to access outgoing edges, build up score for
        # node using outgoing edges, instead of max of incoming
        longest, back = path[node]
        for dest, edge in graph.outgoing(node):
            length = longest + edge
            if dest not in path or length > path[dest][0]:
                path[dest] = (length, node)
            
    print(path[sink][0])  # Print length of path    
    node = sink
    trace = str(node)
    while node != source:
        length, node = path[node]
        trace = str(node) + "->" + trace        
    print(trace)          
    
    
if __name__ == "__main__":
     graph, source, sink = read5D(sys.argv[1])
     longest_path(graph, source, sink)