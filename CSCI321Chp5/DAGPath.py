#Jen Johnson
#CSCI321
#Problem 4 DAG Path

import sys
import numpy as np
from Queue import *

def path_from_source_to_node_is_valid(result, node):
    print(result[1][node])
    if result[1][node] == 0:
        print(str(node) + " is okay. update")
        return True
    if result[1][node] == -1:
        print(str(node) + " is not valid. do not update")
        return False
    else: #predecessor is another node
        print("calling on " + str(result[1][node]))
        return path_from_source_to_node_is_valid(result, result[1][node])

def DAG_path(edges, weights, q, result, s, sink, source):
    """uses a DP approach to find the max weight path through the DAG
    given in edges and weights arrays"""

    #for each node in topological order using s and q
    for x in range (0, len(s)+1):
        next_elt = q.get()
        print("working on " + str(next_elt))

        current_weight = 0
        current_predecessor_index = -1
        best_predecessor_index = -1
        max_weight = 0

        for y in range (0, sink):
            #get all incoming edges
            if edges[y][next_elt] == 1:
                print("incoming edge from " + str(y))
                if path_from_source_to_node_is_valid(result, y):
                    current_weight = weights[y][next_elt]+result[0][y]
                    current_predecessor_index = y
                    #get maximum weight and predecessor
                    if current_weight>max_weight:
                        max_weight = current_weight
                        best_predecessor_index = current_predecessor_index
        #record results
        result[0][next_elt]=max_weight
        result[1][next_elt]=best_predecessor_index

    #get the path from the table using predecessors
    current_node = sink
    path = []

    while current_node>source:
        path.append(current_node)
        current_node = result[1][current_node]

    #first node in path is source
    path.append(source)

    #reverse path
    final_path = path[::-1]

    #format the path string
    max_length_path=str(final_path[0])
    for i in range (1, len(final_path)):
        max_length_path+="->" +str(final_path[i])

    return max_length_path

def main():
    """reads input file-->data, calls DAG Path on the input arrays,
    and writes output file"""

    f = open("DAGPathInput.txt")

    #get num_lines to make reading in data easier
    num_lines = sum(1 for line in open('DAGPathInput.txt'))
    num_lines = num_lines-2

    #get source and sink nodes
    source_str = f.next()
    source = int(source_str)
    sink_str = f.next()
    sink = int(sink_str)

    #initialize arrays for data
    edges = np.zeros((sink, sink+1), dtype=np.int)
    #weights = np.zeros((sink, sink+1), dtype=np.int)
    weights = np.full((sink, sink+1), -1e4, dtype=np.int)

    #initialize structures for getting nodes in topological order
    q = Queue()
    s = set()
    q.put(source)
    s.add(source)

    #splitting each line
    for i in range(0, num_lines):
        next_str = f.next()
        split = next_str.split("-")
        source_node = int(split[0])
        split2 = split[1]
        split2 = split2[1:]
        split3 = split2.split(":")
        sink_node = int(split3[0])
        weight = int(split3[1])

        #putting data into arrays
        edges[source_node][sink_node]=1
        weights[source_node][sink_node]=weight

        #adding nodes to queue q using set s
        current_length=len(s)
        s.add(source_node)
        if len(s)!=current_length:
            q.put(source_node)

    #the sink node is the last node to visit
    q.put(sink)

    #first row is the max weight of the path going to that node
    #second row is the predecessor index of node that results in max weight path
    result = np.zeros((2, sink+1), dtype=np.int)

    #initialize all scores to -inf since nodes w/o predecessors are impossible to reach
    for i in range (1, sink+1):
        result[0][i] = -1e4
    #initialize all predecessors of nodes other than source to -1
    for i in range (1, sink+1):
        result[1][i] = -1

    #return the path
    max_length_path = DAG_path(edges, weights, q, result, s, sink, source)

    #get the max weight from the table
    max_length = result[0][sink]

    file = open("DAGPathOutput.txt", "w")
    file.write(str(max_length) + "\n")
    file.write(str(max_length_path))
    file.close()

if __name__=="__main__":
    main()
