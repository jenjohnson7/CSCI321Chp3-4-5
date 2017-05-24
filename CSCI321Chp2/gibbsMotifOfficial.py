#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 2G

@author: michaellinderman
"""

# 60 minutes

import sys
import math
import random
import numpy as np
import rosalind2D

DNA = rosalind2D.DNA

def read2G(filename):
    """Read problem 2G input"""
    with open(filename, "r") as file:
        k, t, n = file.readline().split()
        sequences = file.readlines()
        return int(k), int(t), int(n), [seq.strip() for seq in sequences]

def profile_randomly_generated(sequence, profile):
    """Determine profile randomly generated string assuming
    k-mer probabilities where multinomial

    Args:
        sequence: String to search for motif
        profile: 4xk Numpy float profile array

    Returns:
        Most probable motif of length k in sequence
    """
    k = profile.shape[1]   # Determine k from input
    probs = np.zeros(len(sequence)-k+1, dtype=np.float_)
    for i in range(len(probs)):
        kmer = sequence[i:i+k]
        prob = 1.0
        for j in range(k):
            prob *= profile[DNA.find(kmer[j]),j]  # Use constant to map char to index
        probs[i] = prob

    # Normalize probabilities of each k-mer
    probs /= np.sum(probs)

    # Could also potentially use
    # np.random.multinomial(1, probs, size=1)
    # to randomly select index according to probabilities, or
    # np.random.choice(range(len(probs)), 1, p=probs)
    idx = np.digitize(np.random.random(), np.cumsum(probs))
    return sequence[idx:idx+k]

def gibbs_sampler(sequences, k, repeat, pseudo):
    # Randomly generate initial motifs
    motifs = []
    for seq in sequences:
        idx = random.randrange(0, len(seq)-k+1)
        motifs.append(seq[idx:idx+k])

    best_score = rosalind2D.score_motifs(motifs, k)
    best_motifs = motifs

    for i in range(repeat):
        idx = random.randrange(0, len(sequences))

        # motifs (excluding motif[idx]) -> profile -> motifs
        profile = rosalind2D.calculate_profile(motifs[:idx] + motifs[idx+1:], k, pseudo)
        motifs[idx] = profile_randomly_generated(sequences[idx], profile)

        score = rosalind2D.score_motifs(motifs, k)
        #print(score)
        if score < best_score:
            best_score = score
            best_motifs = motifs

    return (best_motifs, best_score)

def gibbs_restart(sequences, k, repeat, restarts, pseudo=1):
    best_score = math.inf
    for i in range(restarts):
        motifs, score = gibbs_sampler(sequences, k, repeat, pseudo)
        if score < best_score:
            best_score = score
            best_motifs = motifs
    return best_motifs


# print(gibbs_sampler([\
# "CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA",\
# "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG",\
# "TAGTACCGAGACCGAAAGAAGTATACAGGCGT",\
# "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",\
# "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"\
# ], 8, 100, pseudo=1))


#print(gibbs_restart([\
#"CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA",\
#"GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG",\
#"TAGTACCGAGACCGAAAGAAGTATACAGGCGT",\
#"TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",\
#"AATCCACCAGCTCCACGTGCAATGTTGGCCTA"\
#], 8, 100, 20))

if __name__ == "__main__":
    k, t, n, sequences= read2G(sys.argv[1])
    motifs = gibbs_restart(sequences, k, n, 20)
    for motif in motifs:
        print(motif)
