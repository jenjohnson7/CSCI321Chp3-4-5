#Jen Johnson
#CSCI321
#Problem 15 Ecycle

import sys
import numpy as np
import Queue

def E_cycle(adj_dict, num_edges, num_lines):
    """ finds an Eulerean cycle, given that the graph input is balanced and well connected"""

    #current_node = 0 #arbitrarily choose node 0 to start

    #set current_node as key in adj_dict when using strings instead of node numbers
    keys = adj_dict.keys()
    current_node = keys[0]

    path = []
    seen_edges = 0
    seen_and_extra_edges = [] #for backtracking

    while seen_edges != num_edges:
        if len(adj_dict[current_node]) != 0:
            #if there is another outgoing edge
            path.append(current_node)
            next_node = adj_dict[current_node][0] #get the next unseen edge
            adj_dict[current_node].remove(next_node)
            #remove edge so that it won't be visited twice
            if len(adj_dict[current_node]) !=0:
                #if there is another outgoing edge, add it to backtracking list
                seen_and_extra_edges.append(current_node)
            seen_edges +=1
            current_node = next_node
        else:
            #made a bad choice, need to start a new sub-cycle
            #print(seen_and_extra_edges)
            #print(path)
            current_node = seen_and_extra_edges[0]
            seen_and_extra_edges.remove(current_node)

            #put the previous sub-cycle into the path
            temp_path = []
            new_start = path.index(current_node)
            temp_path = path[new_start:] #from the restart node to the end
            temp_path += path[:new_start] #from the beginning to the restart node
            path = temp_path

    #append the last elt
    source = path[0]
    path+=[source]
    return path

def main():
    "reads input file-->data, calls DAG Path on the input arrays, and writes output file"
    f = open("ECycleInput.txt")

    #get num_lines to make reading in data easier
    num_lines = sum(1 for line in open('ECycleInput.txt'))

    adj_dict = dict() #splitting each line and entering it into adj list
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

    # print("ECycle")
    # print(adj_dict)

    cycle = E_cycle(adj_dict, num_edges, num_lines)
    # print("ECycle")
    # print(cycle)

    size = len(cycle)
    current_size = 0

    file = open("ECycleOutput.txt", "w")
    for node in cycle:
        if current_size != size-1:
            file.write(str(node) + "->")
            current_size+=1
        else:
            file.write(str(node))
    file.close()

if __name__=="__main__":
    main()
