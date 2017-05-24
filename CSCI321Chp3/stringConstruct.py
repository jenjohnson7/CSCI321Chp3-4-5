#Jen Johnson
#CSCI321
#Problem 11 string_construct

import sys
import numpy as np

def string_construct(kmers):
    result = kmers[0]
    for i in range (1, len(kmers)):
        result += kmers[i][-1]
    return result

def main():
    """ reads input file-->data, constructs string from input strings,
    and writes output file """

    f = open("stringConstructInput.txt")

    #get num_lines to make reading in data easier
    num_lines = sum(1 for line in open('stringConstructInput.txt'))

    kmers = []

    for i in range(0, num_lines):
        next_str = f.next().strip()
        kmers.append(next_str)

    result = string_construct(kmers)

    file = open("stringConstructOutput.txt", "w")
    file.write(result)
    file.close()

if __name__=="__main__":
    main()
