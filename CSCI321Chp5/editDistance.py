#Jen Johnson
#CSCI321
#Problem 7 editDistance

#Bug: matches the A in MEANLY to both As in PLEASANTLY
#use a current counter to avoid counting this A twice?

import sys
import numpy as np

def editDistance(str1, str2):
    "uses a DP approach to find the editDistance of 2 input strings"

    n = len(str1)
    m = len(str2)

    #initialize array
    min_distance = np.zeros((m+1, n+1), dtype=np.int)

    #base cases
    for i in range (1, n+1):
        if str1[i-1]==str2[0]:
            min_distance[1][i]=min_distance[1][i-1]
        else:
            min_distance[1][i]=min_distance[1][i-1]+1

    for j in range (1, m+1):
        if str2[j-1]==str1[0]:
            min_distance[j][1]=min_distance[j-1][1]
        else:
            min_distance[j][1]=min_distance[j-1][1]+1

    #fill the array
    for row in range (2, m+1):
        for col in range(2, n+1):
            #if chars match
            if str1[col-1]==str2[row-1]:
                min_distance[row][col] = min( min_distance[row-1][col-1], min_distance[row-1][col], min_distance[row][col-1])
            else: #if chars don't match, increase edit distance
                min_distance[row][col] = min( min_distance[row-1][col-1]+1, min_distance[row-1][col]+1, min_distance[row][col-1]+1)

    print(min_distance)
    return min_distance[m][n]

def main():
    "reads input file-->data, calls editDistance on input strings, and writes output file"
    f= open("editDistanceInput.txt")
    str1 = f.next().strip()
    str2 = f.next().strip()

    result = editDistance(str1, str2)

    file = open("editDistanceOutput.txt", "w")
    file.write(str(result))
    file.close()

if __name__=="__main__":
    main()
