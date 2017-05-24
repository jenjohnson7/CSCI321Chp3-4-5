#Jen Johnson
#CSCI321
#Problem 24 GibbsMotif

from random import randint, random
import math
from randomMotif import initialize_best
from greedyMotifPseudo import make_profile
from medianString import kmers_of_a_string, distance_pattern_to_kmers
from profileMostProbable import prob
import numpy as np

def gibbs_motif(k, t, sequences, n, pseudocount):
    """ runs gibbs motif search for n iterations """

    # initialize current_motifs randomly
    current_motifs, current_consensus, current_profile, current_score = initialize_best(k, t, sequences, pseudocount)

    best_motifs = current_motifs
    global_score = current_score

    #run for n iterations
    for i in range (n):

        # randomly remove 1 sequence and its motif
        index_to_remove = randint(0, t-1)
        seq_to_remove = sequences[index_to_remove]
        motif_to_remove = current_motifs[index_to_remove]

        current_motifs.remove(motif_to_remove)

        # make profile from the rest of the motifs
        current_consensus, current_profile = make_profile(current_motifs, pseudocount, k)

        prob_of_each_substring = []
        substrings_of_seq_removed = kmers_of_a_string(seq_to_remove, k)

        # for each substring in removed sequence...
        for substring in substrings_of_seq_removed:
            # ...calculate prob of that substring given profile
            p = prob(substring, current_profile)
            prob_of_each_substring.append(p)

        # normalize using the denominator
        prob_of_each_substring /= np.sum(prob_of_each_substring)

        # use cum sum and digitize to get the index of the substring to add
        random_float = np.random.random()
        bins = np.cumsum(prob_of_each_substring)
        index_of_substring_to_reinsert = np.digitize(random_float, bins)

        # reinsert new motif and update current_score
        motif_to_reinsert = substrings_of_seq_removed[index_of_substring_to_reinsert]

        current_motifs.insert(index_to_remove, motif_to_reinsert)

        current_consensus, current_profile = make_profile(current_motifs, pseudocount, k)
        current_score = distance_pattern_to_kmers(current_consensus, current_motifs, k)

        if current_score < global_score:
            #improved score, update
            global_score = current_score
            best_consensus = current_consensus
            best_motifs = current_motifs[:]

    return best_motifs, global_score

def main():
    """ reads input file, returns the best motifs, and writes the output file"""
    f = open("gibbsMotifInput.txt")

    integers = next(f)
    split_integers = integers.split()
    k = int(split_integers[0])
    t = int(split_integers[1])
    n = int(split_integers[2]) #number of iterations for each run

    sequences = []

    while True:
        sequence = f.readline().strip()
        sequences.append(sequence)
        if not sequence:
            break
        #gets a list of sequences with the last element ' '

    best_score = math.inf
    best_motifs = []

    #20 random starts
    for i in range (0, 20):
        #call gibbs_motif on the list of sequences without the ' '
        result, score = gibbs_motif(k, t, sequences[:-1], n, 1)
        if score < best_score:
            best_score = score
            best_motifs = result

    file = open("gibbsMotifOutput.txt", "w")
    for sequence in best_motifs:
        file.write(str(sequence) + "\n")
    file.close()

if __name__ == "__main__":
  main()
