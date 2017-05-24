#

import sys
from enum import IntEnum
import numpy as np
from Bio.SubsMat import MatrixInfo

from rosalind_common import *


def read5E(filename):
    """Read inputs for Rosalind 5E"""
    with open(filename, "r") as file:
        return file.readline().strip(), file.readline().strip()

class Back(IntEnum):
    """Enum of edges"""
    MAT=1
    VRT=2
    HRZ=3


def global_alignment(seqV, seqW, scoring, indel):
    """Compute global alignment with score

    Args:
        seq1, seq2: Strings of sequence to be aligned
        scoring: SubstitutionMatrix
        indel: Indel score (negative is penalty)

    Returns:
        Tuple of (score, aligned seqV, aligned seqW)
    """
    n, m = len(seqV)+1, len(seqW)+1
    scores = np.zeros((n,m), dtype=np.int)
    back = np.zeros((n,m), dtype=np.int)

    for i in range(1, n):
        scores[i,0] = scores[i-1,0] + indel
        back[i,0] = Back.VRT
    for j in range(1, m):
        scores[0,j] = scores[0,j-1] + indel
        back[0,j] = Back.HRZ

    for i in range(1, n):
        for j in range(1, m):
            # Needs to be in same order as Back enum above
            incoming = (scores[i-1,j-1] + scoring[seqV[i-1], seqW[j-1]],
                        scores[i-1,j] + indel,
                        scores[i,j-1] + indel
                        )
            index = np.argmax(incoming)

            back[i, j] = index + 1  # To account for enums starting at 1
            scores[i, j] = incoming[index]

    print(scores)
    alignV, alignW = "", ""
    i, j = n-1, m-1
    while i > 0 or j > 0:
        if back[i, j] == Back.MAT:
            alignV = seqV[i-1] + alignV
            alignW = seqW[j-1] + alignW
            i -= 1
            j -= 1
        elif (back[i,j] == Back.VRT):
            alignV = seqV[i-1] + alignV
            alignW = "-" + alignW
            i -= 1
        elif back[i,j] == Back.HRZ:
            alignV = "-" + alignV
            alignW = seqW[j-1] + alignW
            j -= 1


    return scores[n-1, m-1], alignV, alignW

#print(global_alignment("PLEASANTLY","MEANLY", SubstitutionMatrix(MatrixInfo.blosum62), -5))

#print(global_alignment( \
#"YAFDLGYTCMFPVLLGGGELHIVQKETYTAPDEIAHYIKEHGITYIKLTPSLFHTIVNTASFAFDANFESLRLIVLGGEKIIPIDVIAFRKMYGHTEFINHYGPTEATIGA", \
#"AFDVSAGDFARALLTGGQLIVCPNEVKMDPASLYAIIKKYDITIFEATPALVIPLMEYIYEQKLDISQLQILIVGSDSCSMEDFKTLVSRFGSTIRIVNSYGVTEACIDS", \
#SubstitutionMatrix(MatrixInfo.blosum62), -4))


if __name__ == "__main__":
    seqV, seqW = read5E(sys.argv[1])
    score, alignV, alignW = global_alignment(seqV, seqW, SubstitutionMatrix(MatrixInfo.blosum62), -5)
    print(score)
    print(alignV)
    print(alignW)
