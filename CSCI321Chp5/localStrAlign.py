#Jen Johnson
#CSCI321
#Problem 6 localStrAlign
#timed out before result was computed
#Cython?

import sys
import numpy as np
from PAM250 import PAM250
#obtained pam250 as .py dictionary of dictionaries from https://gist.githubusercontent.com/skyfox/5123558/raw/ebbcee55524ec88c2eff5d148ff421aaa8fb52e3/gistfile1.py

def local_str_align(str1, str2, sequence_value, n, m):
    "uses a DP approach to find the optimal local alignment for 2 sequences"

    #initialize backtrack array
    backtrack = np.zeros((m+1, n+1), dtype=np.int)

    #base cases
    for i in range (1, n+1):
        skip_value = sequence_value[0][i-1]-5
        sequence_value[0][i] = max(0, skip_value)

        #base cases for backtrack
        if sequence_value[0][i]==skip_value:
            backtrack[0][i]=2
        if sequence_value[0][i]==0:
            backtrack[0][i]=1

    for j in range (1, m+1):
        skip_value = sequence_value[j-1][0]-5
        sequence_value[j][0] = max(0, skip_value)

        if sequence_value[j][0]==skip_value:
            backtrack[j][0]=2
        if sequence_value[j][0]==0:
            backtrack[j][0]=1

    #fill the array
    for x in range (1, m+1):
        for y in range(1, n+1):
            amino_acid_1 = str1[y-1]
            amino_acid_2 = str2[x-1]
            match_mismatch_value = sequence_value[x-1][y-1] + PAM250[amino_acid_1][amino_acid_2]
            insert_value = sequence_value[x-1][y]-5
            delete_value = sequence_value[x][y-1]-5
            sequence_value[x][y]= max( match_mismatch_value, insert_value, delete_value, 0)

            #fill the backtrack array
            if sequence_value[x][y]==match_mismatch_value:
                backtrack[x][y]=5
            if sequence_value[x][y]==0:
                backtrack[x][y]=1
            if sequence_value[x][y]==insert_value:
                backtrack[x][y]=3
            if sequence_value[x][y]==delete_value:
                backtrack[x][y]=4

    currentStr1, currentStr2 = n, m
    result_one = ""
    result_two = ""

    #find the optimal sink node where score is max
    max_index = sequence_value.argmax()

    #find location/indices of this node as ending point
    row = max_index / m
    col = max_index % m

    #output the alignment in reverse order from max_index using backtrack
    current = backtrack[row][col]

    while current!=1:
        if current==5:
            #if char is included in optimal
            result_one+=str1[col-1]
            result_two+=str2[row-1]
            row-=1
            col-=1
            current = backtrack[row][col]
        elif current==3:
            #if char in str2 is included in optimal
            result_one+="-"
            result_two+=str2[row-1]
            row-=1
            current = backtrack[row][col]
        elif current==4:
            #if char in str1 is included in optimal
            result_one+=str1[col-1]
            result_two+="-"
            col-=1
            current = backtrack[row][col]

    #reverse the string
    result_one = result_one[::-1]
    result_two = result_two[::-1]

    result = result_one + "\n" + result_two

    return result

def main():
    "reads input file-->data, calls localStrAlign on the input strings, and writes output file"
    f= open("localStrAlignInput.txt")
    str1 = f.next().strip()
    str2 = f.next().strip()

    n = len(str1)
    m = len(str2)

    #initialize array so that we can return both the max value and the alignment
    sequence_value = np.zeros((m+1, n+1), dtype=np.int)

    result = local_str_align(str1, str2, sequence_value, n, m)

    max_value = sequence_value.max()

    file = open("localStrAlignOutput.txt", "w")
    file.write(str(max_value))
    file.write("\n" +result)
    file.close()

if __name__=="__main__":
    main()
