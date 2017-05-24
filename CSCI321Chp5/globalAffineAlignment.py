#Jen Johnson
#CSCI321
#Problem 9 globalAffineAlignment

import sys
import numpy as np
from enum import IntEnum
from blosum62 import blosum62

class Back(IntEnum):
    """Enum of edges"""
    MAT = 1
    CLOSEUPP = 2
    CLOSELOW = 3
    OPENUPP = 4
    OPENLOW = 5
    EXTUPP = 6
    EXTLOW = 7

def global_affine_alignment(str1, str2):
    """Compute global alignment with affine gap penalties using DP"""

    n = len(str1)+1
    m = len(str2)+1

    #initialize arrays
    middle = np.zeros((n,m), dtype=np.int)
    upper = np.zeros((n,m), dtype=np.int)
    lower = np.zeros((n,m), dtype=np.int)

    backtrack_middle = np.zeros((n,m), dtype=np.int)
    backtrack_upper = np.zeros((n,m), dtype=np.int)
    backtrack_lower = np.zeros((n,m), dtype=np.int)

    #base cases: negative infinity for edges w/o incoming nodes
    for i in range (0, n):
        upper[i][0] = -1e4
    for j in range (0, m):
        lower[0][j] = -1e4

    #fill arrays
    for i in range(1, n):
        for j in range(1, m):

            #lower
            incoming = (-np.inf,
                        -np.inf,
                        -np.inf,
                        -np.inf,
                        middle[i-1][j]-11,
                        -np.inf,
                        lower[i-1][j]-1)
            index = np.argmax(incoming)

            backtrack_lower[i, j] = index + 1
            lower[i, j] = incoming[index]

            #upper
            incoming = (-np.inf,
                        -np.inf,
                        -np.inf,
                        middle[i][j-1]-11,
                        -np.inf,
                        upper[i][j-1]-1,
                        -np.inf)
            index = np.argmax(incoming)

            backtrack_upper[i, j] = index + 1
            upper[i, j] = incoming[index]

            #middle
            incoming = (middle[i-1,j-1] + blosum62[str1[i-1]][str2[j-1]],
                        upper[i][j],
                        lower[i][j],
                        -np.inf,
                        -np.inf,
                        -np.inf,
                        -np.inf)
            index = np.argmax(incoming)

            backtrack_middle[i, j] = index + 1
            middle[i, j] = incoming[index]

    #get the max score
    choices = (lower[n-1][m-1], middle[n-1][m-1], upper[n-1][m-1])
    max_score = max(choices)

    current_array = np.argmax(choices)

    #get alignment from backtrack
    result_one, result_two = "", ""
    i, j = n-1, m-1

    while i > 0 or j > 0:

        if current_array == 1: #middle
            if backtrack_middle[i, j] == Back.MAT:
                result_one = str1[i-1] + result_one
                result_two = str2[j-1] + result_two
                i -= 1
                j -= 1
            elif backtrack_middle[i,j] == Back.CLOSEUPP:
                result_one = str1[i-1] + result_one
                result_two = "-" + result_two
                current_array += 1
            elif backtrack_middle[i,j] == Back.CLOSELOW:
                result_one = "-" + result_one
                result_two = str2[j-1] + result_two
                current_array -= 1
        elif current_array == 2: #upper
            if backtrack_upper[i,j] == Back.OPENUPP:
                result_one = str1[i-1] + result_one
                result_two = "-" + result_two
                j-=1
                current_array -= 1
            elif backtrack_upper[i,j] == Back.EXTUPP:
                result_one = str1[i-1] + result_one
                result_two = "-" + result_two
                j-=1
        elif current_array == 0: #lower
            if backtrack_lower[i,j] == Back.OPENLOW:
                result_one = "-" + result_one
                result_two = str2[j-1] + result_two
                i-=1
                current_array +=1
            elif backtrack_lower[i,j] == Back.EXTLOW:
                result_one = "-" + result_one
                result_two = str2[j-1] + result_two
                i-=1

    return max_score, result_one, result_two

def main():
    """reads input file-->data, calls global_affine_alignment on input strings,
    and writes output file"""

    f= open("globalAffineAlignmentInput.txt")
    str1 = f.next().strip()
    str2 = f.next().strip()

    score, result_one, result_two = global_affine_alignment(str1, str2)

    result = result_one + "\n" + result_two

    file = open("globalAffineAlignmentOutput.txt", "w")
    file.write(str(score) + "\n")
    file.write(result)
    file.close()

if __name__=="__main__":
    main()
