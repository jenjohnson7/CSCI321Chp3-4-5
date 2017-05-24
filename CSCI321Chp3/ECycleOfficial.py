#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 3F

@author: michaellinderman
"""

import sys
import copy

# 170 minutes

def read3F(filename):
    """Read 3F input"""
    with open(filename, "r") as file:
        graph = {}
        for line in file:
            a_node, b_nodes = map(str.strip, line.split("->"))
            graph[a_node] = list(map(str.strip, b_nodes.split(",")))
        return graph

def eularian_cycle(graph):
    """Find Eularian cycle in graph
    
    Args:
        graph: Graph represented as dictionary of edges
    
    Return:
        List of nodes in cycle
    """
    graph = copy.deepcopy(graph)

    has_outgoing = set()  
    cycle = [next(iter(graph.keys()))]  # Select a random starting point      
    while len(graph) > 0:
        node = cycle[-1]
        to_nodes = graph.get(node)
        if to_nodes == None:
            # We got "stuck" 
            # 1. Select arbitrary node with outgoing edges (and index in cycle)
            new_start = has_outgoing.pop()
            # 2. "Roll" cycle to make new_start the start of cycle and repeat
            index = cycle.index(new_start)  # O(E) (could be O(1) with more smarts)
            cycle = cycle[index:] + cycle[1:index+1]
        else:
            cycle.append(to_nodes.pop())
            if len(to_nodes) == 0:
                graph.pop(node)  # Remove from graph (and nodes with outgoing edges)
                has_outgoing.discard(node)            
            else:
                has_outgoing.add(node)
    
    
    return cycle        
    

def verify_eularian(graph, cycle):
    """Verify cycle is Eularian cycle
    
    Args:
        graph: Graph represented as dictionary of edges
        cycle: Iterable sequence of nodes in cycle
        
    Raises:
        Error if not a valid cycle
    """ 
    graph = copy.deepcopy(graph)
    
    for i in range(len(cycle)-1):
        node = cycle[i]
        to_nodes = graph[node]
        try:
            to_nodes.remove(cycle[i+1])
        except Exception as error:
            print("Bad edge @",i,":",node,"->",cycle[i+1])
            raise error
        if len(to_nodes) == 0:
            graph.pop(node)
        
    if len(graph) > 0:
        raise ValueError("Graph still has nodes")
    
    
#print(eularian_cycle({0 : [3], 1 : [0], 2 : [1,6], 3 : [2], 4 : [2], 5 : [4], 6 : [5,8], 7 : [9], 8 : [7], 9 : [6]}))
#print(eularian_cycle({0 : [6,1], 1 : [2], 2 : [0, 3], 3 : [0], 4 : [2, 6], 5 : [4], 6 : [4, 5]}))

if __name__ == "__main__":
    graph = read3F(sys.argv[1])
    cycle = eularian_cycle(graph)
    verify_eularian(graph, cycle)
    print("->".join(map(str,cycle)))