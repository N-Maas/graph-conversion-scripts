#!/usr/bin/python3
import argparse

# Remaps the IDs of a graph in metis format and removes degree zero nodes.
# All neighborhoods are sorted.
# (Node or edge weights are currently not supported)

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument("output", type=str)

args = parser.parse_args()

current_id = 1
mapping = {}

def insertToMapping(node):
    global current_id
    if node not in mapping:
        mapping[node] = current_id
        current_id += 1

with open(args.input) as f, open(args.output, "w") as out:
    header = f.readline()
    while header.startswith("%"):
        header = f.readline()
    header_vals = header.strip().split(" ")
    n_nodes = int(header_vals[0])
    assert len(header_vals) < 3 or int(header_vals[2]) == 0, "weights are not supported"

    adjacency = [[] for _ in range(0, n_nodes)]
    index = 0
    for line in f:
        index += 1
        splitted = line.strip().split(" ")
        if splitted[0] != '':
            targets = list(map(int, splitted))
            insertToMapping(index)
            for t in targets:
                insertToMapping(t)
            mapped_ts = [mapping[t] for t in targets]
            mapped_ts.sort()
            adjacency[mapping[index] - 1] = mapped_ts

    out.write(f"{current_id - 1} {header_vals[1].strip()}\n")
    for targets in adjacency:
        if len(targets) > 0:
            out.write(f"{' '.join(map(str, targets))}\n")

