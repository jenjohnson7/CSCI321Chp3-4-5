#Jen Johnson
#CSCI321
#Problem 5 globalStrAlign

import sys
import numpy as np
from blosum62 import blosum62
#obtained blosum as .py dictionary of dictionaries from http://histo.ucsf.edu/BMS270/BMS270b_2013/index.htm

def global_str_align(str1, str2, sequence_value, n, m):
    "uses a DP approach to return the optimal global alignment string for 2 sequences"

    #initialize backtrack array
    backtrack = np.zeros((m+1, n+1), dtype=np.int)

    #base cases that only have 1 incoming edge per node
    for i in range (1, n+1):
        sequence_value[0][i]=sequence_value[0][i-1]-5

    for j in range (1, m+1):
        sequence_value[j][0]=sequence_value[j-1][0]-5

    #fill the arrays
    for x in range (1, m+1):
        for y in range(1, n+1):
            amino_acid_1 = str1[y-1]
            amino_acid_2 = str2[x-1]
            match_mismatch_value = sequence_value[x-1][y-1] + blosum62[amino_acid_1][amino_acid_2]
            insert_value = sequence_value[x-1][y]-5
            delete_value = sequence_value[x][y-1]-5
            sequence_value[x][y]= max( match_mismatch_value, insert_value, delete_value)

            #fill the backtrack array
            if sequence_value[x][y]==match_mismatch_value:
                backtrack[x][y]=1
            if sequence_value[x][y]==insert_value:
                backtrack[x][y]=2
            if sequence_value[x][y]==delete_value:
                backtrack[x][y]=3

    col, row = n, m
    result_one = ""
    result_two = ""

    #output the alignment in reverse order using backtrack
    current = backtrack[row][col]

    while current!=0:
        if current==1:
            #if char is included in optimal
            result_one+=str1[col-1]
            result_two+=str2[row-1]
            row-=1
            col-=1
            current = backtrack[row][col]
        elif current==2:
            result_one+="-"
            result_two+=str2[row-1]
            row-=1
            current = backtrack[row][col]
        elif current==3:
            result_one+=str1[col-1]
            result_two+="-"
            col-=1
            current = backtrack[row][col]

    #add the first character
    if row == 0 and col == 0:
        result_one+=str1[0]
        result_two+=str2[0]
    if row == 0 and not col ==0:
        result_one+=str1[0]
        result_two+="-"
    else: #col==0
        result_one+="-"
        result_two+=str2[0]

    #reverse the string
    result_one = result_one[::-1]
    result_two = result_two[::-1]

    result = result_one + "\n" + result_two

    return result

def main():
    "reads input file-->data, calls globalStrAlign on the input strings, and writes output file"
    f= open("globalStrAlignInput.txt")
    str1 = f.next().strip()
    str2 = f.next().strip()

    n = len(str1)
    m = len(str2)

    #initialize array outside of DAG function so that we can return both the max value and the alignment
    sequence_value = np.zeros((m+1, n+1), dtype=np.int)

    #initial call to return the path
    result = global_str_align(str1, str2, sequence_value, n, m)

    file = open("globalStrAlignOutput.txt", "w")
    file.write(str(sequence_value[m][n])+ "\n")
    file.write(result)
    file.close()

if __name__=="__main__":
    main()
