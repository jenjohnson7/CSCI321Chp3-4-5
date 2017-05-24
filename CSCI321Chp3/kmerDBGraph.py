#Jen Johnson
#CSCI321
#Problem 14 kmer DBGraph

import sys
import numpy as np
from overlap import overlap_graph
from strDBGraph import str_DBGraph

def kmer_DBGraph(kmers):
    """  makes a dictionary where key == prefix, and value == suffix """
    result_dict = dict()

    for i in range (0, len(kmers)):
        prefix_key = kmers[i][:-1]
        suffix_value = kmers[i][1:]
        if prefix_key not in result_dict:
            result_dict[prefix_key] = [suffix_value]
        else: #already in dict, update
            existing_suffix = result_dict[prefix_key]
            temp = existing_suffix + [suffix_value]
            result_dict[prefix_key] = temp

    keys = result_dict.keys()

    return result_dict, keys

def main():
    """ reads input file-->data, constructs graph from kmers,
    and writes output file """

    f = open("kmerDBGraphInput.txt")

    #get num_lines to make reading in data easier
    num_lines = sum(1 for line in open('kmerDBGraphInput.txt'))

    #read the input
    kmers = []

    for i in range(0, num_lines):
        next_str = f.next().strip()
        kmers.append(next_str)

    #get k for use in printing
    k = len(kmers[0])

    # make the graph in the form of a dictionary adj list
    result, keys = kmer_DBGraph(kmers)

    file = open("kmerDBGraphOutput.txt", "w")
    for j in range (0, len(keys)):
        if len(result[keys[j]]) != 0:
            # if the node has followers
            file.write(str(keys[j])+ " -> ")

            # neighbors = result[keys[j]]
            # # if only 1 neighbor, combine the k-1 elements into a single index
            # if len(neighbors[0])==1:
            #     first_node = ""
            #     for i in range (0, k-1):
            #         #add each char to get the k-1-mer back
            #         first_node += neighbors[i]
            #     temp = []
            #     temp.append(first_node)
            #     result[keys[j]] = temp

            count = 0
            size = len(result[keys[j]])
            #print the list of followers
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
