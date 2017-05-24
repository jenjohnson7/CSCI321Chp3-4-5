#Jen Johnson
#CSCI321
#Problem 10 kmers_of_string

import sys
import numpy as np

def kmers_of_string(string, k):
    """ returns the set of kmers of length k from the string in the string's order"""
    result = []
    current_start = 0
    while current_start + k <= len(string):
        kmer = ""
        for i in range (0, k):
            kmer+=string[current_start+i]
        result.append(kmer)
        current_start+=1
    return result

def main():
    """ reads input file-->data, calls kmers on input string,
    and writes output file """
    f= open("kmersOfStringInput.txt")
    k = int(f.next())
    str = f.next().strip()

    result = kmers_of_string(str, k)

    file = open("kmersOfStringOutput.txt", "w")
    for string in result:
        file.write(string + "\n")
    file.close()

if __name__=="__main__":
    main()
