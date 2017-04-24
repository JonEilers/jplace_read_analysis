#!/usr/bin/python3.5

try:
    import simplejson as json
except ImportError:  # pragma nocover
    import json  # simplejson has better feedback on parsing failures

import argparse
import re
import os
import pandas as pd

internal_count = 0
external_count = 0
total_placement_count = 0
totalEdgeCount = 0
leafCount = 0
internalCount = 0


def get_files(root_directory, extension='.jplace'):
    filtered_files = []
    extension_length = len(extension)
    for root, subdirList, files in os.walk(os.path.abspath(root_directory)):
        for name in files:
            if name[-extension_length:] == extension:
                filtered_files.append(os.path.join(root, name))
    return filtered_files


def tree_splitter(jplace):
    tree = jplace['tree']
    branches = re.split('[, ( )]',tree)  ##splitting at ')' '(' and ',' eliminates all delimiters that are not curly braces--
    # leaves either empty elements ex: u'' or elements withedge numbers/labels/lengths in each element of the list
    return branches


def edge_counter(tree):
    global totalEdgeCount, leafCount, internalCount
    totalEdgeCount -= 1
    leafEdges = []
    internalEdges = []
    branches = tree_splitter(tree)
    # i is integer index of each element in list
    # v is value (string) at each index
    for v in branches:
        if '{' in v:
            totalEdgeCount += 1
        if "|" in v:
            leafCount += 1
            leaf_edgeNum = int(v.split('{')[1].split('}')[0])
            leafEdges.append(leaf_edgeNum)
        elif v != '':
            internal_edgeNum = int(v.split('{')[1].split('}')[0])
            internalCount += 1
            internalEdges.append(internal_edgeNum)
    return {"internalEdges": internalEdges, "internalCount": internalCount, "leafCount": leafCount,
            "leafEdges": leafEdges, 'totalEdgeCount':totalEdgeCount}


def number_of_placements(file):
    global total_placement_count
    placements = file['placements']
    for p in placements:
        total_placement_count += (p['nm'][-1])
    return total_placement_count

def edge_indice(file):
    fields = file["fields"]
    for index, items in enumerate(fields):
        if items == "edge_num":
            return index

def placement_location(file):
    internal_edge_list = edge_counter(file)["internalEdges"]
    leaf_edge_list = edge_counter(file)["leafEdges"]
    placements = file['placements']
    edge_index = edge_indice(file)
    for i in placements:
        placement_edge = i["p"][0][edge_index]
        if placement_edge in internal_edge_list:
            global internal_count
            internal_count += 1
        elif placement_edge in leaf_edge_list:
            global external_count
            external_count += 1
    return internal_count, external_count


def internal_vs_leaf(dir, out_file):
    jplace_files = get_files(dir)
    for file in jplace_files:
        with open(file) as json_data:
            jplace = json.load(json_data)
        placement_count_total = number_of_placements(jplace)
        placement_int_vs_ext = placement_location(jplace)
    ivl_dict = {'Leaf Count': external_count, 'Internal Count':internal_count, 'Total Number of Placements':total_placement_count}
    ivl_series = pd.Series(ivl_dict)
    output = ivl_series.to_csv(out_file)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of internal placements vs leaf placements on a phylogenetic tree. Takes .jplace files")
    parser.add_argument('-directory', help = 'directory with .jplace files', required = True)
    parser.add_argument('-out_file', help = 'output file (txt format)', required = True)
    args = parser.parse_args()

    internal_vs_leaf(dir = args.directory, out_file=args.out_file)



