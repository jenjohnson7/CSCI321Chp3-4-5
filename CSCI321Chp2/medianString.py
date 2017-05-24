#Jen Johnson
#CSCI321
#Problem 19 MedianString

from itertools import product
from math import inf

def median_string(k, kmers):
    """  enumerates all possible patterns using itertools product
        compares each of the possible patterns using distance_pattern_to_kmers
        goal is to minimise the score
        returns the median string as a tuple """

    min_pattern_to_kmers = inf
    median_string = ""

    all_patterns = list(product("ACTG", repeat = k))
    for pattern in all_patterns:
        current = distance_pattern_to_kmers(pattern, kmers, k)
        if min_pattern_to_kmers > current:
            min_pattern_to_kmers = current
            median_string = pattern

    return median_string

def distance_pattern_to_kmers(pattern, kmers, k):
    """ computes the minimum score of a pattern to a set of kmers
        uses kmers_of_a_string to enumerate substrings of each kmer
        uses edit_distance to score each substring with the pattern
        returns minimum score for all kmers """

    total = 0
    for kmer in kmers:
        current = inf
        substrings = kmers_of_a_string(kmer, k)
        for substring in substrings:
            if current > edit_distance(pattern, substring, k):
                current = edit_distance(pattern, substring, k)
            total += current
    return total

def kmers_of_a_string(string, k):
    """ enumerates the substrings of a string """

    result = []
    current_start = 0
    while current_start + k <= len(string):
        kmer = ""
        for i in range (0, k):
            kmer+=string[current_start+i]
        result.append(kmer)
        current_start+=1
    return result

def edit_distance(pattern, substring, k):
    """ used to compare two strings """
    count = 0
    for i in range (0, k):
        if pattern[i] != substring[i]:
            count+=1
    return count

def main():
    """ reads input file, finds the median string, and writes the output file"""
    f = open("medianStringInput.txt")

    k = int(next(f))

    kmers = []

    while True:
        kmer = f.readline().strip()
        kmers.append(kmer)
        if not kmer:
            break

    result_tuple = median_string(k, kmers[:-1])

    result_string = ""
    for i in result_tuple:
        result_string+=i

    file = open("medianStringOutput.txt", "w")
    file.write(str(result_string))
    file.close()

if __name__ == "__main__":
  main()
