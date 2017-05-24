#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 5C

@author: mlinderman
"""

import sys
import numpy as np
from enum import IntEnum

def read5C(filename):
    """Read inputs for Rosalind 5C"""
    with open(filename, "r") as file:
        seq1 = file.readline().strip()
        seq2 = file.readline().strip()
        return seq1, seq2


class Back(IntEnum):
    """Enum of edges"""
    MAT=1
    VRT=2
    HRZ=3

def lcs_backtrack(seq1, seq2):
    """Return longest common subsequence
    
    Args:
        seq1, seq2: Sequences as strings
    
    Returns:
        Longest common subsequence as string
    """
    v, w = len(seq1) + 1, len(seq2) + 1   
    grid = np.zeros((v, w), dtype=np.int)
    back = np.zeros((v, w), dtype=np.int)    
    
    for i in range(1, v):
        for j in range(1, w):                        
            match = seq1[i-1] == seq2[j-1]
            
            this_grid = np.iinfo(np.int).min
            if grid[i-1, j] > this_grid:
                this_grid = grid[i-1, j]
                this_back = Back.VRT
            if grid[i, j-1] > this_grid:
                this_grid = grid[i, j-1]
                this_back = Back.HRZ
            if match and (grid[i-1, j-1] + 1) > this_grid:
                this_grid = grid[i-1, j-1] + 1
                this_back = Back.MAT
             
            grid[i, j] = this_grid
            back[i, j] = this_back
            
            # Could also use np.argmax to find index of maximum value of list
            
    seq = ""    
    
    # Iterative, instead of recursive backtracking
    i, j = v - 1, w - 1    
    while i > 0 and j > 0: 
        if back[i, j] == Back.VRT:
            i -= 1
        elif back[i, j] == Back.HRZ:
            j -= 1
        else:
            seq = seq1[i - 1] + seq
            i -= 1
            j -= 1
    
    return seq

#print(lcs_backtrack("AACCTTGG","ACACTGTGA"))

if __name__ == "__main__":
    seq1, seq2 = read5C(sys.argv[1])
    print(lcs_backtrack(seq1, seq2))