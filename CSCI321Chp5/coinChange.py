#Jen Johnson
#CSCI321
#Problem 1 coinChange

import sys

def DPChange(target, denoms, d):
    "recursive top-down approach for min num coins to make change for target"
    #uses a dictionary to avoid redundant recursive calls

    #base case
    if target==0:
        return 0

    #initialize a result that will always be larger than any other result
    result = target

    #for each denom that is less than the target, call DPChange on target-denom.
    for i in range (0, len(denoms)):
        if denoms[i]<=target:
            #if next denom less than target

            if (target-denoms[i]) in d:
                #if already in dictionary
                current = d.get(target-denoms[i])
            else:
                current = DPChange(target-denoms[i], denoms, d)
                d[target-denoms[i]] = current
                #else put it in the dictionary

            #find minimum result out of all denoms
            if current+1<result:
                result = current+1
    return result

def main():
    "reads input file-->data, calls DPChange, and writes output file"
    f= open("coinChangeInput.txt")
    targetStr = f.readline()
    targetInt = int(targetStr)

    denomStr = f.next()
    noCommas = denomStr.replace(",", " ")
    denomsList = noCommas.split()
    denomsArray = [int(i) for i in denomsList]

    #initialize dictionary to use in DPChange
    d = {}

    sys.setrecursionlimit(25000)
    #got a runtime exceeded error because max for python is 999
    #set it higher here

    #initial call to DPChange
    result = DPChange(targetInt, denomsArray, d)

    file = open("coinChangeOutput.txt", "w")
    file.write(str(result))
    file.close()

if __name__=="__main__":
    main()
