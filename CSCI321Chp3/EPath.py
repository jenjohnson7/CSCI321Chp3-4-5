#Jen Johnson
#CSCI321
#Problem 16 EPath

import sys
import numpy as np
from ECycle import E_cycle

def make_degree_dict(adj_dict, degree_dict):
    """ uses the adj_dict to calculate degree of each node """
    #getting the outdegrees
    for entry in adj_dict:
        degree_dict[entry]=len(adj_dict[entry])

    #getting the indegrees
    for entry in adj_dict:
        for neighbor in adj_dict[entry]:
            if neighbor in degree_dict:
                current = degree_dict[neighbor]
                current +=1
                degree_dict[neighbor] = current
            else:
                degree_dict[neighbor]=1

    return degree_dict

def read_input (adj_dict):
    """ reads the input file in the form of an adj list into a dictionary of nodes"""
    f = open("EPathInput.txt")

    #get num_lines to make reading in data easier
    num_lines = sum(1 for line in open('EPathInput.txt'))

    num_edges = 0 #used for the while loop condition to see if there are still unvisited edges

    for i in range(0, num_lines):
        next_str = f.next()
        split = next_str.split("-")
        source_node = int(split[0])

        #isolate the destination values
        dest_str = split[1][1:].strip()
        dest_values = dest_str.split(",")

        temp = []

        for i in range (0, len(dest_values)):
            dest = int(dest_values[i])
            temp.append(dest)
            num_edges+=1

        adj_dict[source_node] = temp

    return adj_dict, num_edges, num_lines

def E_Path(degree_dict, adj_dict, num_edges, num_lines):
    """ makes the graph balanced, calls E-Cycle, removes imaginary edge"""
    #get the unbalanced nodes that have odd degree
    unbalanced = []
    for entry in degree_dict:
        if degree_dict[entry]% 2 ==1:
            unbalanced.append(entry)

    outdegree = []
    #getting the outdegrees of unbalanced nodes
    for i in range (0, len(unbalanced)):
        node = unbalanced[i]
        if node in adj_dict:
            outdegree.append(len(adj_dict[node]))
        else:
            outdegree.append(0)

    indegree = []
    #getting the indegrees of unbalanced nodes
    for i in range (0, len(unbalanced)):
        indegree.append(degree_dict[unbalanced[i]]-outdegree[i])

    #add the missing edge to adj_dict based on out and indegrees
    for i in range (0, len(unbalanced)):
        if outdegree[i] < indegree[i]:
            source = unbalanced[i]
        else:
            sink = unbalanced[i]

    if source in adj_dict:
        temp = adj_dict[source]
        temp.append(sink)
        adj_dict[source] = temp
    else:
        adj_dict[source] = [sink]

    # call E_cycle on the new adj_dict with added edge
    cycle = E_cycle(adj_dict, num_edges+1, num_lines)

    start_index = 0

    # find the imaginary edge
    if outdegree[0] < outdegree[1]:
        for i in range (0, len(cycle)):
            if cycle[i] == unbalanced[0] and cycle[i+1] == unbalanced[1]:
                start_index = i
    if outdegree[1] < outdegree[0]:
        for i in range (0, len(cycle)):
            if cycle[i] == unbalanced[1] and cycle[i+1] == unbalanced[0]:
                start_index = i

    final_path = []
    #get the path from the cycle by splicing the imaginary edge
    final_path += cycle[start_index+1:]
    final_path += cycle[1:start_index+1]

    return final_path

def main():
    """reads input file-->data, modifies the graph to make balanced and connected,
    and calls ECycle, and writes output file"""

    #reads the input file
    adj_dict = {}
    adj_dict, num_edges, num_lines = read_input(adj_dict)

    #get the degrees
    degree_dict = {}
    degree_dict = make_degree_dict(adj_dict, degree_dict)

    #call E_Path
    final_path = E_Path(degree_dict, adj_dict, num_edges, num_lines)

    print(final_path)

    size = len(final_path)
    current_size = 0

    file = open("EPathOutput.txt", "w")
    for node in final_path:
        if current_size != size-1:
            file.write(str(node) + "->")
            current_size+=1
        else:
            file.write(str(node))
    file.close()

if __name__=="__main__":
    main()
