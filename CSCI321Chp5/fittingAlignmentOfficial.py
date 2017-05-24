#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 5H

@author: mlinderman
"""

import rosalind5E
import sys
from enum import IntEnum
import numpy as np
import itertools

class Back(IntEnum):
    """Enum of edges"""
    MAT=1
    VRT=2
    HRZ=3
    END=4  # Edge from beginning or to end

def fitting_alignment(seqV, seqW, scoring, indel):
    """Print fitting alignment with score
    
    Args:
        seqV, seqW: Sequence strings
        scoring: SubstitutionMatrix
        indel: Indel score (negative is penalty)
    """
    n, m = len(seqV)+1, len(seqW)+1
    scores = np.zeros((n,m), dtype=np.int)
    back = np.full((n,m), Back.END, dtype=np.int)
    
    # Local alignment along i-axis, and it will only take taxi edge
    
    for j in range(1, m):
        scores[0,j] = scores[0,j-1] + indel
        back[0,j] = Back.HRZ
            
    for i in range(1, n):
        for j in range(1, m):
            incoming = (scores[i-1,j-1] + scoring[seqV[i-1], seqW[j-1]],
                        scores[i-1,j] + indel, 
                        scores[i,j-1] + indel 
                        )
            index = np.argmax(incoming) 

            back[i, j] = index + 1  # To account for enums starting at 1
            scores[i, j] = incoming[index]
      
    j = len(seqW)
    i = np.argmax(scores[:,j])  # Look for max along right-most column       
    
    print(scores[i, j])
    
    alignV, alignW = "", ""   
    while i > 0 or j > 0:
        if back[i, j] == Back.MAT:
            alignV = seqV[i-1] + alignV
            alignW = seqW[j-1] + alignW
            i -= 1
            j -= 1
        elif back[i, j] == Back.VRT:
            alignV = seqV[i-1] + alignV
            alignW = "-" + alignW
            i -= 1
        elif back[i, j] == Back.HRZ:
            alignV = "-" + alignV
            alignW = seqW[j-1] + alignW
            j -= 1
        elif back[i, j] == Back.END:
            break
                
    print(alignV)
    print(alignW)

# Create DNA substitition matrix as specified in problem
DNA = "ACGT"
fitting_distance_matrix = {}
for key in itertools.product(DNA, DNA):
    if key[0] == key[1]:
        fitting_distance_matrix[key] = 1
    else:
        fitting_distance_matrix[key] = -1        

#fitting_alignment("GTAGGCTTAAGGTTA", "TAGATA", fitting_distance_matrix, -1)

if __name__ == "__main__":
    seq1, seq2 = rosalind5E.read5E(sys.argv[1])
    fitting_alignment(seq1, seq2, fitting_distance_matrix, -1)