#!/usr/bin/python3.5

'''
Abreviations
ff = functional family
ivl = internal vs leaf

To-do list
- add function to count the number of cogs in each family
	-then normalize the data. as in, find which cogs spike the most when they all have the same number
- add function to determine which cogs have the most reads mapped to them
- low priority - add function to select branches or subsections of a jplace phylogenetic tree
- add function that accounts for what the sample depth was

'''

import json
import argparse
import re
import os
import pandas as pd


def get_files(root_directory, extension='.jplace'):
    filtered_files = []
    extension_length = len(extension)
    for root, subdirList, files in os.walk(os.path.abspath(root_directory)):
        for name in files:
            if name[-extension_length:] == extension:
                filtered_files.append(os.path.join(root, name))
    return filtered_files


def tree_splitter(jplace):
    tree = jplace["tree"]
    branches = re.split('[, ( )]',tree)  ##splitting at ')' '(' and ',' eliminates all delimiters that are not curly braces--
    # leaves either empty elements ex: u'' or elements withedge numbers/labels/lengths in each element of the list
    return branches


def edge_counter(split_tree):
    internalCount = -1
    totalEdgeCount = -1
    leafCount = 0
    leafEdges = []
    internalEdges = []
    branches = tree_splitter(split_tree)
    # i is integer index of each element in list
    # v is value (string) at each index
    for i, v in enumerate(branches):
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
            "leafEdges": leafEdges}

def number_of_placements(file):
    total_placement_count = 0
    placements = file['placements']
    for p in placements:
        total_placement_count += len(p['nm'])
    return total_placement_count

def edge_indice(file):
    fields = file["fields"]
    for index, items in enumerate(fields):
        if items == "edge_num":
            return index

def get_cog_metadata(file):
    cog_meta_df = pd.read_table(file, index_col = False)
    cog_ff = list(cog_meta_df['func'])
    for i in range(0,len(cog_ff)):
        if cog_ff[i] == '':
            cog_ff[i] = 'S'
        else:
            if len(cog_ff[i]) > 1:
                cog_ff[i] = cog_ff[i][0]
    cog_ff = pd.Series(cog_ff, name = 'Functional Family COG Count')
    return cog_meta_df, cog_ff.value_counts()

def get_cog_func_abv(file):
    func_pd = pd.read_table(file)
    func_fam_abv = func_pd['# Code']
    return func_fam_abv

def create_empty_pd(cog_func_abv_file):
    list = get_cog_func_abv(cog_func_abv_file)
    slength = len(list)
    empty_list = []
    for i in range(0,slength+1):
        empty_list.append(0)
    empty_dict = {"Internal":empty_list, "Leaf":empty_list, "Total":empty_list}
    func_abv = pd.DataFrame(list)
    empty_pd = pd.DataFrame(empty_dict)
    empty_df = pd.concat([func_abv,empty_pd], axis = 1)
    ivl_empty_df = empty_df.set_index('# Code')
    return ivl_empty_df

def get_cog_name(file):
    file_name = os.path.basename(file)
    cog_name = file_name.split('.')[0]  # name of gene is first part of file name
    return(cog_name)

def get_cog_ff(cog_name, cog_metadata): # I have very mixed feelings about panda right now.....
    cog_data = cog_metadata[cog_metadata['# COG'].isin([cog_name])]
    if cog_data.empty:
        cog_ff = 'S'
    else:
        cog_ff = list(cog_data['func'])[0]
        if len(cog_ff) > 1:
            cog_ff = cog_ff[0]
    return cog_ff

def placement_location(file):
    external_count = 0
    internal_count = 0
    internal_edge_list = edge_counter(file)["internalEdges"]
    leaf_edge_list = edge_counter(file)["leafEdges"]
    placements = file['placements']
    edge_index = edge_indice(file)
    for i in placements:
        placement_edge = i["p"][0][edge_index]
        if placement_edge in internal_edge_list:
            internal_count += 1
        elif placement_edge in leaf_edge_list:
            external_count += 1
    return internal_count, external_count

def get_json_contents(file_name):
    f = open(file_name)
    json_data = None
    try:
        json_data = json.load(f)
    except Exception as e:  # pragma nocover
        print('json error with file %s - skipping\n%s' % (f.name, e.message))
    finally:
        f.close()
    return json_data

def internal_vs_leaf(dir, out_file):
    cog_metadata = get_cog_metadata('cognames2003-2014.tab')
    #cog_ff_counts = get_cog_metadata('cognames2003-2014.tab')[1]
    dataframe = create_empty_pd('fun2003-2014.tab')
    jplace_files = get_files(dir)
    for file in jplace_files:
        jplace = get_json_contents(file)
        cog_name = get_cog_name(file)
        cog_ff = get_cog_ff(cog_name, cog_metadata[0])
        dataframe.loc[cog_ff,'Total'] += number_of_placements(jplace) #total # of placements
        dataframe.loc[cog_ff,'Internal'] += placement_location(jplace)[0] #internal placements
        dataframe.loc[cog_ff,'Leaf'] += placement_location(jplace)[1]#  and leaf placements
    dataframe = pd.concat([dataframe, cog_metadata[1]], axis = 1)
    return dataframe.to_csv(out_file)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of internal placements vs leaf placements on a phylogenetic tree. Takes .jplace files")
    parser.add_argument('-directory', help = 'directory with .jplace files', required = True)
    parser.add_argument('-out_file', help = 'output file (txt formart)', required = True)
    args = parser.parse_args()

    internal_vs_leaf(dir = args.directory, out_file=args.out_file)
    print(get_cog_metadata('cognames2003-2014.tab')[1])


