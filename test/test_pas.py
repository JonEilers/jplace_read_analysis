from src.pas import tree_splitter, edge_counter, totalEdgeCount, internalCount, leafCount

node_dict = {'tree':'(bob{1},bill|c|{3})'
}

def test_tree_splitter():
    print(tree_splitter(node_dict))
    assert tree_splitter(node_dict) == ['','bob{1}','bill|c|{3}','']

def test_edge_counter():

    results = edge_counter(node_dict)
    assert results['totalEdgeCount'] == 1 # subtract one for the root of the tree
    assert results['leafCount'] == 1
    assert results['internalCount'] == 1
    assert results['leafEdges'] == [3]
    assert results['internalEdges'] == [1]


# internalEdges, internalCount, leafCount, leafEdges, totalEdgeCount
