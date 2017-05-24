#Jen Johnson
#CSCI321
#Problem 17 kmer to genome

from kmerDBGraph import kmer_DBGraph
from EPath import E_Path, make_degree_dict
from stringConstruct import string_construct

def main():
    """ reads input file-->data, constructs string from input strings,
    and writes output file """

    f = open("kmerToGenomeInput.txt")

    k = f.next()
    #get num_lines to make reading in data easier
    num_lines = sum(1 for line in open('kmerToGenomeInput.txt'))-1

    kmers = []
    for i in range(0, num_lines):
        next_str = f.next().strip()
        kmers.append(next_str)

    # make the graph in the form of a dictionary adj list
    result, keys = kmer_DBGraph(kmers)
    #result is adj_list as dictionary

    num_edges = 0

    for entry in result:
        num_edges+=len(result[entry])

    #get the degrees
    degree_dict = {}
    degree_dict = make_degree_dict(result, degree_dict)

    #call E_Path
    ordered_kmers = E_Path(degree_dict, result, num_edges, num_lines)

    final_path = string_construct(ordered_kmers)

    file = open("kmerToGenomeOutput.txt", "w")
    file.write(final_path)
    file.close()

if __name__=="__main__":
    main()
