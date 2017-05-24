#Jen Johnson
#CSCI321
#Problem 20 profileMostProbable

import numpy as np
from medianString import kmers_of_a_string

def profile_most_probable(string, k, profile):
    """ finds a substring in the input string with highest probability of occuring from the given profile
    goal is to maximise probability/max_prob
    returns a kmer that has this max_prob """
    substrings = kmers_of_a_string(string, k)
    product_kmer = substrings[0] #not an empty string
    #initialize to first substring for greedy motif w/o pseudocounts
    #prevent the addition of an empty string
    #instead, even if all probs are 0, it will add something
    max_prob = 0
    for substring in substrings:
        current_prob = prob(substring, profile)
        if current_prob > max_prob:
            max_prob = current_prob
            product_kmer = substring
    return product_kmer

def prob(substring, profile):
    """ calculates the probability that a substring occurrs given a profile """
    prob = 1
    for i in range (0, len(substring)):
        char_index = char_to_index(substring[i])
        prob *= profile[char_index][i]
    return prob

def char_to_index(letter):
    if letter == "A":
        index = 0
    elif letter == "C":
        index = 1
    elif letter == "G":
        index = 2
    else: #letter == T
        index = 3
    return index

def main():
    """ reads input file, finds the profile most probable kmer in the string, and writes the output file"""
    f = open("profileMostProbableInput.txt")

    string = next(f)
    k = int(next(f))

    profile = np.zeros((4, k), dtype = "float")

    row = 0

    while True:
        line = f.readline().strip()
        floats = line.split()
        for i in range (0, len(floats)):
            profile[row][i] = floats[i]
        row+=1
        if not line:
            break

    result = profile_most_probable(string, k, profile)

    file = open("profileMostProbableOutput.txt", "w")
    file.write(str(result))
    file.close()

if __name__ == "__main__":
  main()
