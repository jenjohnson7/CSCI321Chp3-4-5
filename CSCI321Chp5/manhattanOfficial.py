#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosalind.info Problem 5B

@author: michaellinderman
"""
import sys
import numpy as np

def read5B(filename):
    """Read inputs for Rosalind 5B"""
    with open(filename, "r") as file:
        n, m = [int(x) for x in file.readline().split(sep=" ", maxsplit=2)]        
        down  = np.genfromtxt(filename, dtype="i4", skip_header=1, skip_footer=n+2)
        right = np.genfromtxt(filename, dtype="i4", skip_header=n+2)
        return down, right

def manhattan_tourist(down, right):
    """Compute largest path for Manhattan tourist problem
    
    Args:
        down: Weights for down edges as an (n x m-1) matrix
        right: Weights for right edges as an (n-1 x m) matrix
    
    Returns:
        Largest path
    """
    n, m = down.shape[0], right.shape[1]       
    
    # Grid is n+1, m+1
    grid = np.zeros((n+1, m+1), dtype=np.int)
    for r in range(1,n+1):    
        grid[r, 0] = grid[r-1, 0] + down[r-1, 0]
    for c in range(1, m+1):    
        grid[0, c] = grid[0, c-1] + right[0, c-1] 
    for r in range(1, n+1):
        for c in range(1, m+1):
            grid[r, c] = max(grid[r-1, c] + down[r-1, c], grid[r, c-1] + right[r, c-1])
    
    return grid[n, m]

if __name__ == "__main__":
    down, right = read5B(sys.argv[1])
    print(manhattan_tourist(down, right))