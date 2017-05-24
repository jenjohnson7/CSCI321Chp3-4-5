#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 5G

@author: mlinderman
"""

import rosalind5E

import sys
import itertools

# Build a substitution matrix that implements edit distance
AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"
edit_distance_matrix = {}
for key in itertools.product(AMINO_ACIDS, AMINO_ACIDS):
    if key[0] == key[1]:
        # Matches have 0 edits
        edit_distance_matrix[key] = 0
    else:
        # Everything else is -1
        edit_distance_matrix[key] = -1

def edit_distance(seq1, seq2):
    """Compute the edit distance
    
    Compute the edit distance using a global alignment and
    precisely defined substitution
    
    Args:
        seq1, seq2: Amino acid sequences to compare
    
    Returns:
        Edit distance
    """
    
    # Also use -1 for indel penalty
    score, align1, align2 = rosalind5E.global_alignment(seq1, seq2, edit_distance_matrix, -1)
    return -score  # Need to invert since score is negative edit distance


#print(edit_distance("PLEASANTLY","MEANLY"))

if __name__ == "__main__":
    seq1, seq2 = rosalind5E.read5E(sys.argv[1])    
    print(edit_distance(seq1, seq2))