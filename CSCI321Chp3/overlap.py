#Jen Johnson
#CSCI321
#Problem 12 overlap graph

import sys
import numpy as np

def overlap_graph(kmers):
    """returns an adj matrix for an overlap graph based on prefixes and suffixes"""

    result = []

    for i in range (0, len(kmers)):
        suffix = kmers[i][1:]
        followers = []
        for j in range (0, len(kmers)):
            prefix = kmers[j][:-1]
            if prefix == suffix:
                followers.append(kmers[j])
        result.append(followers)

    return result

def main():
    """ reads input file-->data, generates overlap graph,
    and writes output file """

    f = open("overlapInput.txt")

    #get num_lines to make reading in data easier
    num_lines = sum(1 for line in open('overlapInput.txt'))

    kmers = []

    for i in range(0, num_lines):
        next_str = f.next().strip()
        kmers.append(next_str)

    result = overlap_graph(kmers)

    file = open("overlapOutput.txt", "w")

    for j in range (0, len(result)):
        for i in range (0, len(result[j])):
            file.write(kmers[j] + " -> " + str(result[j][i]) + "\n")

    file.close()

if __name__=="__main__":
    main()
