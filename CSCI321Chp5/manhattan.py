#Jen Johnson
#CSCI321
#Problem 2 manhattan

import sys
import numpy as np

def manhattan(n, m, down, right):
    "uses DP tabulation approach to find the longest path through the city"

    #initialize array to hold max weight path up to that location
    maxLenArray = np.zeros((n+1, m+1), dtype=np.int)

    #base cases
    for i in range(1, n+1):
        maxLenArray[i][0]=maxLenArray[i-1][0]+down[i-1][0]
    for j in range(1, m+1):
        maxLenArray[0][j]=maxLenArray[0][j-1]+right[0][j-1]

    #fill the rest of the cells
    for j in range(1, m+1):
         for i in range(1, n+1):
             maxLenArray[i][j]=max( maxLenArray[i-1][j] + down[i-1][j], maxLenArray[i][j-1] + right[i][j-1])

    return maxLenArray[n][m]

def main():
    "reads input file-->data, calls manhattan on the input arrays, and writes output file"
    f= open("manhattanInput.txt")
    sizesStr = f.next()
    sizes = sizesStr.split()
    n = int(sizes[0])
    m = int(sizes[1])

    #initialize down array
    down = np.zeros((n, m+1), dtype=np.int)

    #fill down array
    for row in range (0, n):
        rowString = f.next()
        rowList = rowString.split()
        down[row] = [int(i) for i in rowList]

    #arrays separated by a -
    x = f.next()

    #initialize right array
    right = np.zeros((n+1, m), dtype=np.int)

    #fill right array
    for col in range (0, n+1):
        colString = f.next()
        colList = colString.split()
        right[col] = [int(i) for i in colList]

    result = manhattan(n, m, down, right)

    file = open("manhattanOutput.txt", "w")
    file.write(str(result))
    file.close()

if __name__=="__main__":
    main()
