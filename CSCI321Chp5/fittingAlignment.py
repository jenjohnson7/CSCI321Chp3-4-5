#Jen Johnson
#CSCI321
#Problem 8 fitting Alignment

import sys
import numpy as np
from enum import IntEnum

class Back(IntEnum):
    """Enum of edges"""
    MAT=1
    MM=2
    VRT=3
    HRZ=4
    END=5

def fitting_alignment(seqV, seqW):
    """computes fitting alignment with score using a DP approach"""

    n = len(seqV)+1
    m = len(seqW)+1

    #initialize the arrays
    score = np.zeros((n,m), dtype=np.int)
    backtrack = np.zeros((n,m), dtype=np.int)

    #base cases for backtrack
    for i in range(1, n):
        backtrack[i, 0] = Back.END
    for j in range(1, m):
        backtrack[0, j] = Back.HRZ
        #taken from solutions to acct for taxi edges on the shorter str
        score[0,j] = score[0,j-1] -1

    #fill the arrays
    for i in range(1, n):
        for j in range(1, m):
            if seqV[i-1] == seqW[j-1]:
                incoming = (score[i-1,j-1] + 1,
                            -np.inf,
                            score[i-1,j] -1,
                            score[i,j-1] -1,
                            )
            elif seqV[i-1] != seqW[j-1]:
                incoming = (-np.inf,
                            score[i-1,j-1] -1,
                            score[i-1,j] -1,
                            score[i,j-1] -1,
                            )

            index = np.argmax(incoming)
            backtrack[i, j] = index + 1  #enums start at 1
            score[i, j] = incoming[index]

    #get max score and index.
    #max score must be in last column because all of w must be aligned
    j = len(seqW)
    #indices_of_maxes =
    i = np.argmax(score[:,j]) #score.argmax(axis = 0)
    #returns indices of max for each col
    #i = indices_of_maxes[j]
    #get the last col max
    max_score = score[i][j]

    print(score)

    #get alignment from backtrack
    alignV, alignW = "", ""

    while i > 0 or j > 0:
        if backtrack[i, j] == Back.MAT:
            alignV = seqV[i-1] + alignV
            alignW = seqW[j-1] + alignW
            i -= 1
            j -= 1
        elif backtrack[i, j] == Back.MM:
            alignV = seqV[i-1] + alignV
            alignW = seqW[j-1] + alignW
            i -= 1
            j -= 1
        elif (backtrack[i,j] == Back.VRT):
            alignV = seqV[i-1] + alignV
            alignW = "-" + alignW
            i -= 1
        elif backtrack[i,j] == Back.HRZ:
            alignV = "-" + alignV
            alignW = seqW[j-1] + alignW
            j -= 1
        elif backtrack[i, j] == Back.END:
            break

    return max_score, alignV, alignW

def main():
    """reads input file-->data, calls fittingAlignment on input strings,
    and writes output file"""

    f= open("fittingAlignmentInput.txt")
    v = f.next().strip()
    w = f.next().strip()

    score, result_one, result_two = fitting_alignment(v, w)

    result = result_one + "\n" + result_two

    file = open("fittingAlignmentOutput.txt", "w")
    file.write(str(score) + "\n")
    file.write(result)
    file.close()

if __name__=="__main__":
    main()
