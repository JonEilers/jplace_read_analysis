from src.pas import tree_splitter, edge_counter, number_of_placements, placement_location, internal_count, external_count, edge_indice

fake_tree = {'tree': '(bob{1},bill|c|{3})',
             'placements':[
                           {"p":[[123, 345, 3, 678, 987, 753, 321, 111]],"nm":[['read1','read2','read3', 3]]},
                           {"p":[[23,24,1,33,44,55,66,7]],"nm":[['read4',1]]}
                           ],
             "fields":["classification", "distal_length", "edge_num", "like_weight_ratio", "likelihood", "marginal_like", "pendant_length", "post_prob"]
}

def test_tree_splitter():
    print(tree_splitter(fake_tree))
    assert tree_splitter(fake_tree) == ['', 'bob{1}', 'bill|c|{3}', '']

def test_edge_counter():
    results = edge_counter(fake_tree)
    assert results['totalEdgeCount'] == 1 # subtract one for the root of the tree
    assert results['leafCount'] == 1
    assert results['internalCount'] == 1
    assert results['leafEdges'] == [3]
    assert results['internalEdges'] == [1]

def test_number_of_placements():
    results = number_of_placements(fake_tree)
    #print(number_of_placements(fake_tree))
    assert results == 4

def test_edge_indice():
    result = edge_indice(fake_tree)
    assert result == 2

def test_placement_location():
    results = placement_location(fake_tree)
    assert results[internal_count] == 1
    assert results[external_count] == 1

#def test_internal_vs_leaf():


