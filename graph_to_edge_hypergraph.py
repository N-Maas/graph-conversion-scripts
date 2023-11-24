#!/usr/bin/python3
import argparse

# Converts a graph (in metis format) into a hypergraph (in hmetis format)
# by interpreting nodes as hyperedges and edges as nodes. A hyperedge
# connects all edges of the original graph that are incident to the same node.

# Each node in the resulting hypergraph has degree 2. Further, a vertex
# partition of the hypergraph corresponds to an edge partition of the original
# graph.

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument("hypergraph", type=str)

args = parser.parse_args()

current_id = 1
mapping = {}

def insertToMapping(u, v):
    global current_id
    assert u != v
    key = (min(u, v), max(u, v))
    if key in mapping:
        return mapping[key]
    else:
        mapping[key] = current_id
        current_id += 1
        return current_id - 1

with open(args.input) as f, open(args.hypergraph, "w") as out:
    header = f.readline()
    while header.startswith("%"):
        header = f.readline()
    header_vals = header.strip().split(" ")
    n_nodes = int(header_vals[0])
    n_edges = int(header_vals[1])
    assert len(header_vals) < 3 or int(header_vals[2]) == 0, "weights are not supported"

    # in hmetis format, number of hyperedges comes first
    out.write(f"{n_nodes} {n_edges}\n")
    index = 0
    for line in f:
        index += 1
        splitted = line.strip().split(" ")
        if splitted[0] == '':
            out.write("\n")
        else:
            targets = list(map(int, splitted))
            mapped_ts = [insertToMapping(index, t) for t in targets]
            mapped_ts.sort()
            out.write(f"{' '.join(map(str, mapped_ts))}\n")
