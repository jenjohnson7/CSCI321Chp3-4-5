#Jen Johnson
#CSCI321
#Problem 21 GreedyMotif

from greedyMotifPseudo import greedy_motif_pseudo

def main():
    """ reads input file, returns the best motifs, and writes the output file"""
    f = open("GreedyMotifPseudoInput.txt")

    integers = next(f)
    split_integers = integers.split()
    k = int(split_integers[0])
    t = int(split_integers[1])

    sequences = []

    while True:
        sequence = f.readline().strip()
        sequences.append(sequence)
        if not sequence:
            break
        #gets a list of sequences with the last element ' '

    #call greedy_motif_pseudo on the list of sequences without the ' '
    #call with pseudoount == 0
    result = greedy_motif_pseudo(k, t, sequences[:-1], 0)

    file = open("greedyMotifPseudoOutput.txt", "w")
    for sequence in result:
        file.write(str(sequence) + "\n")
    file.close()

if __name__ == "__main__":
  main()
