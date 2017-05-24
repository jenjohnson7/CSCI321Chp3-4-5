#Jen Johnson
#CSCI321
#Problem 23 RandomMotif

from random import randint
from greedyMotifPseudo import make_profile
from medianString import distance_pattern_to_kmers
from profileMostProbable import profile_most_probable
import math

def initialize_best(k ,t, sequences, pseudocount):
    """ initialize best_motifs randomly and get best/global scores to beat """
    len_of_sequence = len(sequences[0])
    best_motifs = []

    #initialize motifs in each string randomly
    for sequence in sequences:
        kmer_starting_index = randint(0, len_of_sequence-k)
        kmer_ending_index = kmer_starting_index + k
        kmer = sequence[ kmer_starting_index : kmer_ending_index ]
        best_motifs.append(kmer)

    #initialize global best score/profile
    best_consensus, best_profile = make_profile(best_motifs, pseudocount, k)
    initial_global_score = distance_pattern_to_kmers(best_consensus, best_motifs, k)

    return best_motifs, best_consensus, best_profile, initial_global_score

def change_kmers(sequences, k, profile, pseudocount):
    """ chooses profile most probable kmer from each sequence based on profile and updates score"""
    current_motifs = []

    for sequence in sequences:
        # modify ALL kmers using profile_most_probable
        motif_to_add = profile_most_probable(sequence, k , profile)
        current_motifs.append(motif_to_add)

    current_consensus, current_profile = make_profile(current_motifs, pseudocount, k)
    current_score = distance_pattern_to_kmers(current_consensus, current_motifs, k)

    return current_motifs, current_consensus, current_profile, current_score

def random_motif(k, t, sequences, pseudocount):
    """ runs random motif search until score is max """

    #initialize best_motifs randomly and get best/global scores to beat
    best_motifs, best_consensus, best_profile, global_score = initialize_best(k, t, sequences, pseudocount)

    current_profile = best_profile

    #loop until the score is min
    while True:
        current_motifs, current_consensus, current_profile, current_score = change_kmers(sequences, k, current_profile, pseudocount)

        if current_score < global_score:
            #improved score, keep going
            global_score = current_score
            best_consensus = current_consensus
            best_motifs = current_motifs
        else: #found local or global min, return
            return best_motifs, global_score

def main():
    """ reads input file, returns the best motifs, and writes the output file"""
    f = open("randomMotifInput.txt")

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

    best_score = math.inf
    best_motifs = []

    for i in range (0, 1000):
        #call random_motif on the list of sequences without the ' '
        result, score = random_motif(k, t, sequences[:-1], 1)
        if score < best_score:
            best_score = score
            best_motifs = result

    file = open("randomMotifOutput.txt", "w")
    for sequence in best_motifs:
        file.write(str(sequence) + "\n")
    file.close()

if __name__ == "__main__":
  main()
