#Jen Johnson
#CSCI321
#Problem 22 GreedyMotifPseudo

import numpy as np
from medianString import kmers_of_a_string, distance_pattern_to_kmers
from profileMostProbable import profile_most_probable

def greedy_motif_pseudo(k, t, sequences, pseudocount):
    """ calls greedy motif algorithm on the input
    returns the set of strings with lowest score/difference """

    best_motifs = []
    for sequence in sequences:
        best_motifs.append(sequence[0:k])

    best_consensus, best_profile = make_profile(best_motifs, pseudocount, k)

    initial_global_score = distance_pattern_to_kmers(best_consensus, best_motifs, k)

    #gets all kmers in the first strings
    #assumption: the implanted kmer is in the first string
    first_string_subsequences = kmers_of_a_string(sequences[0], k)

    for subsequence in first_string_subsequences:
        current_motifs = []
        current_motifs.append(subsequence)
        for i in range (1, t):
            #add the profile most probable kmer from each string in motifs
            current_consensus, current_profile = make_profile(current_motifs, pseudocount, k)
            motif_to_add = profile_most_probable(sequences[i], k , current_profile)
            current_motifs.append(motif_to_add)

        #once all motifs added, compare the distance to the global distance
        current = distance_pattern_to_kmers(current_consensus, current_motifs, k)
        if current < distance_pattern_to_kmers(best_consensus, best_motifs, k):
            best_consensus = current_consensus
            best_motifs = current_motifs

    return best_motifs

def make_profile(motifs, pseudocount, k):
    """ makes count and probability profiles given a set of motifs
    returns the profile and the consensus string of that profile"""

    count = np.zeros((4, k), dtype = "int")
    for i in range (0, len(motifs)):
        # print("i" +str(i))
        for j in range (0, k):
            # print("j" + str(j))
            char = motifs[i][j]
            # print (motifs[i][j])
            index = char_to_index(char)
            count[index][j]+=1

    profile = np.zeros((4, k), dtype = "float")

    for x in range (0, 4):
        for y in range (0, k):
            #profile[x][y] = count[x][y]/k + pseudocount
            profile[x][y] = (count[x][y]+pseudocount)/((len(motifs)+4)*pseudocount)
            #La Place's Rule for pseudocounts

    index_of_max_in_col = np.argmax(profile, axis = 0)

    consensus = ""
    for index in index_of_max_in_col:
        consensus += index_to_char(index)

    return consensus, profile

def char_to_index(letter):
    index = -1
    if letter == "A":
        index = 0
    elif letter == "C":
        index = 1
    elif letter == "G":
        index = 2
    elif letter == "T":
        index = 3
    return index

def index_to_char(index):
    char = "T"
    if index == 0:
        char = "A"
    elif index == 1:
        char = "C"
    elif index == 2:
        char = "G"
    elif index == 3:
        char == "T"
    return char

def main():
    """ reads input file, returns the best motifs, and writes the output file"""
    f = open("GreedyMotifPseudoInput.txt")

    integers = next(f)
    split_integers = integers.split()
    k = int(split_integers[0])
    t = int(split_integers[1])

    sequences = []

    while True:
        sequence = f.readline().strip()
        sequences.append(sequence)
        if not sequence:
            break
        #gets a list of sequences with the last element ' '

    #call greedy_motif_pseudo on the list of sequences without the ' '
    result = greedy_motif_pseudo(k, t, sequences[:-1], 1)

    file = open("greedyMotifPseudoOutput.txt", "w")
    for sequence in result:
        file.write(str(sequence) + "\n")
    file.close()

if __name__ == "__main__":
  main()
