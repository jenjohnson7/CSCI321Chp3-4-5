#Jen Johnson
#CSCI321
#Problem 3 LCS

import sys
import numpy as np

def LCS(str1, str2, n, m):
    "uses a DP approach to find the LCS of 2 input strings"

    #initialize arrays
    maxLength = np.zeros((n+1, m+1), dtype=np.int)
    backtrack = np.zeros((n+1, m+1), dtype=np.int)

    #fill the rest of the cells
    for i in range(1, n+1):
         for j in range(1, m+1):
             if str1[i-1] == str2[j-1]: #if the chars match
                 a = maxLength[i-1][j-1]+1
                 b = maxLength[i-1][j]
                 c = maxLength[i][j-1]
                 maxLength[i][j]= max (a, b, c)
             else: #if chars do not match
                 b = maxLength[i-1][j]
                 c = maxLength[i][j-1]
                 maxLength[i][j]= max (b, c)

             #record the result in backtrack
             if maxLength[i][j]==maxLength[i-1][j]:
                 backtrack[i][j]=1
             if maxLength[i][j]==maxLength[i][j-1]:
                 backtrack[i][j]=2
             if maxLength[i][j]==maxLength[i-1][j-1]+1 and str1[i-1]==str2[j-1]:
                 backtrack[i][j]=3

    #output the path in reverse order using backtrack
    currentStr1, currentStr2 = n, m
    result = ""

    while currentStr2 > 0:
        if backtrack[currentStr1][currentStr2]==1:
            currentStr1-=1
        elif backtrack[currentStr1][currentStr2]==2:
            currentStr2-=1
        elif backtrack[currentStr1][currentStr2]==3:
            currentStr1-=1
            currentStr2-=1
            result+=str2[currentStr2]
        else: #backtrack==0
            break

    #reverse the string
    result = result[::-1]

    return result

def main():
    "reads input file-->data, calls LCS on the input strings, and writes output file"
    f= open("LCSInput.txt")

    str1 = f.next().strip()
    str2 = f.next().strip()

    n = len(str1)
    m = len(str2)

    result = LCS(str1, str2, n, m)

    file = open("LCSOutput.txt", "w")
    file.write(result)
    file.close()

if __name__=="__main__":
    main()
