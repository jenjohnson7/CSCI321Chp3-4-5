#Jen Johnson
#CSCI321
#Problem 13 str to DB graph

import sys
import numpy as np
from kmersOfString import kmers_of_string
from overlap import overlap_graph
from collections import OrderedDict

def str_DBGraph(kmers, graph):
    """ turns an overlap graph into DB graph by gluing identical nodes"""

    result = OrderedDict()
    #keys = nodes, values = set of followers based on prefix/suffix matching

    for i in range (0, len(kmers)):
        # for each kmer, look for repeats in graph
        if result.has_key(kmers[i]):
            #if there are repeats, merge the adj list of followers into a set to prevent repeats
            current_followers_set = set(result[kmers[i]])
            for j in range (0, len(graph[i])):
                current_followers_set.add(graph[i][j])
            result[kmers[i]] = current_followers_set
        else:
            # if there are no repeats, add the followers into a set to prevent repeats
            current_followers_set = set(graph[i])
            result[kmers[i]] = current_followers_set

    keys = result.keys()
    return result, keys

def main():
    """ reads input file-->data, makes a DB Graph from the string
    and writes output file """

    f= open("strDBGraphInput.txt")
    k = int(f.next())
    string = f.next().strip()

    #put the kmers on the edges instead
    kmers = kmers_of_string(string, k-1)
    graph = overlap_graph(kmers)

    #result is a dictionary of nodes with values = non-redundant lists of followers
    #keys is the list of keys in the dictionary so printing is easier
    result, keys = str_DBGraph(kmers, graph)

    file = open("strDBGraphOutput.txt", "w")

    for j in range (0, len(keys)):
        if len(result[keys[j]]) != 0:
            # if the node has followers
            file.write(str(keys[j])+ " -> ")

            count = 0
            size = len(result[keys[j]])
            #print the followers
            for elt in result[keys[j]]:
                count+=1
                if count == size:
                    # if last follower, no comma
                    file.write(str(elt))
                else:
                    # else, need a comma
                    file.write(str(elt) + ",")
            # new line for each entry
            file.write("\n")

    file.close()

if __name__=="__main__":
    main()
