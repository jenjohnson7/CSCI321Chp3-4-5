#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 5J

@author: mlinderman
"""

import sys
from enum import IntEnum
import numpy as np
from Bio.SubsMat import MatrixInfo

from rosalind_common import *
import rosalind5E

class Back(IntEnum):
    """Enum of edges"""
    MAT=1
    OPN_VRT=2
    VRT=3
    CLS_VRT=4
    OPN_HRZ=5
    HRZ=6
    CLS_HRZ=7

def score_and_move(incoming, moves):
    """Return maximum score and associated move from indexable inputs"""
    index = np.argmax(incoming)
    return incoming[index], moves[index]
    
def affine_alignment(seqV, seqW, scoring, gap_open, gap_ext):
    """Print affine global alignment with score
    
    Args:
        seq1, seq2: Strings of sequence to be aligned
        scoring: SubstitutionMatrix
        gap_open: Gap open score (penalty should be negative)
        gap_ext: Gap extension score (penalty should be negative)
    """
    n, m = len(seqV)+1, len(seqW)+1
    
    # Initialize upper and lower to most negative integer          
    diag = np.zeros((n,m), dtype=np.int)  # middle
    vert = np.full((n,m), np.iinfo(np.int).min, dtype=np.int)  # lower
    horz = np.full((n,m), np.iinfo(np.int).min, dtype=np.int)  # upper
    
    diag_back = np.full((n,m), Back.MAT, dtype=np.int)
    vert_back = np.full((n,m), Back.VRT, dtype=np.int)
    horz_back = np.full((n,m), Back.HRZ, dtype=np.int)
    
    diag_moves = (Back.CLS_VRT, Back.CLS_HRZ, Back.MAT)
    vert_moves = (Back.VRT, Back.OPN_VRT)
    horz_moves = (Back.HRZ, Back.OPN_HRZ)                      
    
    for i in range(1, n):
        # Need to convert vert and horz to Python ints to avoid overflow
        vert[i, 0], vert_back[i, 0] = score_and_move(
                (int(vert[i-1,0]) + gap_ext, diag[i-1,0] + gap_open),
                 vert_moves
                 )
        diag[i, 0], diag_back[i, 0] = vert[i,0], Back.CLS_VRT
    
    for j in range(1, m):
        horz[0, j], horz_back[0, j] = score_and_move(
                (int(horz[0, j-1]) + gap_ext, diag[0, j-1] + gap_open),
                 horz_moves
                 )
        diag[0, j], diag_back[0, j] = horz[0,j], Back.CLS_HRZ
    
    for i in range(1, n):
        for j in range(1, m):          
            vert[i, j], vert_back[i, j] = score_and_move(
                (int(vert[i-1,j]) + gap_ext, diag[i-1,j] + gap_open),
                 vert_moves
                 ) 
            horz[i, j], horz_back[i, j] = score_and_move(
                (int(horz[i, j-1]) + gap_ext, diag[i, j-1] + gap_open),
                 horz_moves
                 )
            # Must compute diag after vert and horz
            diag[i, j], diag_back[i, j] = score_and_move(
                (vert[i,j], horz[i,j], diag[i-1,j-1] + scoring[seqV[i-1], seqW[j-1]]),
                 diag_moves
                 )
    
    print(diag[n-1, m-1])
    
    alignV, alignW = "", ""   
    i, j, back = n-1, m-1, diag_back
    while i > 0 or j > 0:
        if back[i, j] == Back.MAT:
            alignV = seqV[i-1] + alignV
            alignW = seqW[j-1] + alignW
            i -= 1
            j -= 1
        elif back[i, j] == Back.VRT or back[i, j] == Back.OPN_VRT:
            if back[i, j] == Back.OPN_VRT:  # Must have come from diag matrix
                back = diag_back 
            alignV = seqV[i-1] + alignV
            alignW = "-" + alignW
            i -= 1            
        elif back[i, j] == Back.HRZ or back[i, j] == Back.OPN_HRZ:
            if back[i, j] == Back.OPN_HRZ:
                back = diag_back
            alignV = "-" + alignV
            alignW = seqW[j-1] + alignW
            j -= 1
        elif back[i, j] == Back.CLS_VRT:  # Don't update position, just matrix
            back = vert_back
        elif back[i, j] == Back.CLS_HRZ:
            back = horz_back

                
    print(alignV)
    print(alignW) 

#affine_alignment("PRTEINS","PRTWPSEIN", SubstitutionMatrix(MatrixInfo.blosum62), -11, -1)

# Stop and Think, page 156
#affine_alignment( \
#"YAFDLGYTCMFPVLLGGGELHIVQKETYTAPDEIAHYIKEHGITYIKLTPSLFHTIVNTASFAFDANFESLRLIVLGGEKIIPIDVIAFRKMYGHTEFINHYGPTEATIGA", \
#"AFDVSAGDFARALLTGGQLIVCPNEVKMDPASLYAIIKKYDITIFEATPALVIPLMEYIYEQKLDISQLQILIVGSDSCSMEDFKTLVSRFGSTIRIVNSYGVTEACIDS", \
#SubstitutionMatrix(MatrixInfo.blosum62), -4, -4)


if __name__ == "__main__":
    seq1, seq2 = rosalind5E.read5E(sys.argv[1])
    affine_alignment(seq1, seq2, SubstitutionMatrix(MatrixInfo.blosum62), -11, -1)

   