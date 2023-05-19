import networkx as nx
import kdegree as kd
import time
import sys
import getopt
from os import path

def difference(S, R):
    DIF = nx.create_empty_copy(R)
    DIF.name ="Difference of (%s and %s)" % (S.name, R.name)
    if set(S) != set(R):
        raise nx.NetworkXError("Node sets of graphs is not equal")

    r_edges = set(R.edges())
    s_edges = set(S.edges())

    # I'm not sure what the goal is: the difference, or the edges that are in R but not in S
    # In case it is the difference:
    diff_edges = r_edges.symmetric_difference(s_edges)

    # In case its the edges that are in R but not in S:
    # diff_edges = r_edges - s_edges

    DIF.add_edges_from(diff_edges)

    return DIF


def main(argv):
    input_file = None
    output_file = None
    k = None
    noise = None

    try:
        opts, args = getopt.getopt(argv, "i:o:k:n:")
    except getopt.GetoptError:
        sys.exit("run_k_anon.py -i <inputfile> -o <outputfile> -k <k-anonymity level> -n <noise>")
    for opt, arg in opts:
        if opt == '-i':
            input_file = arg
        elif opt == '-o':
            output_file = arg
        elif opt == '-k':
            k = int(arg)
        elif opt == '-n':
            noise = int(arg)

    error = False
    if input_file is None:
        print("Please specify an input file")
        error = True
    if output_file is None:
        print("Please specify an output file")
        error = True
    if error:
        sys.exit("Syntax: run_k_anon.py -i <inputfile> -o <outputfile> -k <k-anonymity level> -n <noise>")

    if k is None:
        k = 2
        print("Using default k = 2")
    if noise is None:
        noise = 1
        print("Using default n = 1")

    if not path.exists(input_file):
        sys.exit("Cannot find the input file")

    log = open(output_file + '.log', 'w')
    sys.stdout = log

    G = nx.read_edgelist(input_file, nodetype=int)

    start = time.time()
    Ga = kd.graph_anonymiser(G, k=k, noise=noise, with_deletions=True)
    print("Total execution time =", time.time() - start)

    H = nx.intersection(G, Ga)

    num_edges_in_G = len(set(G.edges()))
    num_edges_in_both = len(set(H.edges()))

    print("Edges overlap = " + str(100 * num_edges_in_both / num_edges_in_G) + "%")
    print("Num edges original graph = " + str(nx.number_of_edges(G)))
    print("Num edges anonymised graph = " + str(nx.number_of_edges(Ga)))

    print(difference(G, Ga).edges())
    print("differ edge:", len(difference(G, Ga).edges()))

    nx.write_edgelist(Ga, output_file, data=False)


if __name__ == "__main__":
    main(sys.argv[1:])
