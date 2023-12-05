#!/usr/bin/python3
import argparse

# Converts a graph (in metis format) into a hypergraph (in hmetis format)
# by interpreting the adjacency matrix in the row-net model. Concretely,
# this means that each node is mapped to one hyperedge which contains the
# neighborhood of this node.
# The resulting hypergraph has the same number of hyperedges and hypernodes.

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument("hypergraph", type=str)

args = parser.parse_args()

with open(args.input) as f, open(args.hypergraph, "w") as out:
    header = f.readline()
    while header.startswith("%"):
        header = f.readline()
    header_vals = header.strip().split(" ")
    n_nodes = int(header_vals[0])
    n_edges = int(header_vals[1])
    assert len(header_vals) < 3 or int(header_vals[2]) == 0, "weights are not supported"

    out.write(f"{n_nodes} {n_nodes}\n")
    index = 0
    for line in f:
        if index < n_nodes:
            index += 1
            splitted = line.strip().split(" ")
            neighborhood = [index]
            if splitted[0] != '':
                neighborhood.extend(map(int, splitted))
                neighborhood.sort()
            out.write(f"{' '.join(map(str, neighborhood))}\n")
        else:
            assert line.strip() == "", f"unexpected line {index + 1}"
