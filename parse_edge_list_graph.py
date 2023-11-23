#!/usr/bin/python3
import argparse

# Converts a graph (not hypergraph!) given in an hmetis-like format without header,
# i.e. one edge per line, into an actual hgr file in hmetis format.
# Supports edge deduplication, 0 or 1 as first index and ' ' and ',' as separator.
#
# Note: You might want to convert into metis format in a second step.

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument("hypergraph", type=str)

args = parser.parse_args()


max_node = 0
starts_at_zero = False
hyperedges = set()
with open(args.input) as f:
    first = True
    separator = " "
    for line in f:
        if line.startswith("%") or line.strip() == "":
            continue

        if first and "," in line:
            separator = ","
        first = False
        [source, target] = line.strip().split(separator)
        u = int(source)
        v = int(target)
        max_node = max(u, max_node)
        max_node = max(v, max_node)
        if u == 0 or v == 0:
            starts_at_zero = True
        if u < v:
            hyperedges.add((u, v))
        elif u > v:
            hyperedges.add((v, u))

hyperedges = list(hyperedges)

if starts_at_zero:
    max_node += 1
    for i in range(0, len(hyperedges)):
        e = hyperedges[i]
        hyperedges[i] = (e[0] + 1, e[1] + 1)

with open(args.hypergraph, "w") as out:
    out.write(f"{len(hyperedges)} {max_node}\n")
    for e in hyperedges:
        out.write(f"{e[0]} {e[1]}\n")

